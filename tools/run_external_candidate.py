#!/usr/bin/env python3
"""Generalized external-candidate runner for the published capability contracts.

Drives an external candidate system through a line-delimited JSON (NDJSON)
adapter protocol: for each dataset case the runner serves the case inputs
(ground truth stripped) on the adapter's stdin and reads the candidate's
observed record from its stdout. The runner then assembles the
candidate-results file (with mandatory overlap disclosure), retains raw
per-case traces with sha256 digests, and invokes the contract's fail-closed
scorer to produce the authoritative report.

This runner is plumbing, not evidence: it never fabricates candidate
records, it aborts when a record byte-matches the dataset expected record
(copy guard, an automatic disqualifier), and a report produced this way is
only valid when the adapter actually wraps the system under test.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shlex
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class Contract:
    contract_id: str
    dataset: Path
    items_key: str
    id_field: str
    strip_keys: tuple[str, ...]
    record_required: tuple[str, ...]
    scorer: Path
    rows_key: str
    copy_guard: bool


CONTRACTS: dict[str, Contract] = {
    "cap011": Contract(
        contract_id="cap011",
        dataset=ROOT / "benchmarks" / "self-evaluation" / "cap011-dataset-v1.json",
        items_key="cases",
        id_field="case_id",
        strip_keys=("expected_outcome", "adjudication"),
        record_required=(
            "predicted_outcome",
            "confidence",
            "review_gate_routed",
            "raw_output_ref",
            "hallucination_adjudication",
        ),
        scorer=ROOT / "tools" / "run_cap011_calibration_benchmark.py",
        rows_key="runs",
        copy_guard=False,
    ),
    "cap014": Contract(
        contract_id="cap014",
        dataset=ROOT / "benchmarks" / "tool-execution" / "cap014-mocked-scenarios-v1.json",
        items_key="scenarios",
        id_field="scenario_id",
        strip_keys=("expected",),
        record_required=(
            "decision",
            "tool",
            "target",
            "arguments",
            "authorization_context",
            "side_effect",
            "deployment_trigger",
            "observed_rationale",
        ),
        scorer=ROOT / "tools" / "run_cap014_mock_benchmark.py",
        rows_key="results",
        copy_guard=True,
    ),
}


def compact(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def serve_view(item: dict[str, Any], contract: Contract) -> dict[str, Any]:
    return {key: value for key, value in item.items() if key not in contract.strip_keys}


def abort(reason: str, records: int = 0, code: int = 2) -> int:
    print(json.dumps({"run_status": "ABORTED", "reason": reason, "records_collected": records}, indent=2))
    return code


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--contract", required=True, choices=sorted(CONTRACTS))
    parser.add_argument(
        "--adapter",
        required=True,
        help="command that reads NDJSON case inputs (ground truth stripped) on stdin and writes one NDJSON record per case to stdout",
    )
    parser.add_argument("--candidate-id", required=True, help="identifier of the candidate system under test")
    parser.add_argument("--operator", default=None, help="who operates the candidate system")
    parser.add_argument(
        "--overlap-disclosure",
        required=True,
        help="disclose any overlap between the candidate and the dataset author or repository maintainer; claim none only if genuinely none",
    )
    parser.add_argument("--raw-outputs", type=Path, required=True)
    parser.add_argument("--candidate-results", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--executed-at", default=None, help="fixed ISO-8601 timestamp for reproducible runs; defaults to now UTC")
    parser.add_argument("--dataset", type=Path, default=None)
    args = parser.parse_args()

    contract = CONTRACTS[args.contract]
    dataset_path = args.dataset if args.dataset is not None else contract.dataset
    dataset = json.loads(dataset_path.read_text(encoding="utf-8"))
    items = dataset.get(contract.items_key)
    if not isinstance(items, list) or not items:
        return abort(f"dataset has no {contract.items_key} array")

    try:
        adapter_cmd = shlex.split(args.adapter)
    except ValueError as exc:
        return abort(f"adapter command could not be parsed: {exc}")

    records: dict[str, dict[str, Any]] = {}
    raw_rows: list[dict[str, Any]] = []
    abort_reason: str | None = None
    proc = subprocess.Popen(
        adapter_cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
    )
    try:
        assert proc.stdin is not None and proc.stdout is not None
        for item in items:
            case_id = item.get(contract.id_field)
            served = serve_view(item, contract)
            line_in = compact(served)
            proc.stdin.write(line_in + "\n")
            proc.stdin.flush()
            line_out = proc.stdout.readline()
            if not line_out.strip():
                abort_reason = f"adapter produced no record for {case_id}"
                break
            try:
                record = json.loads(line_out)
            except json.JSONDecodeError:
                abort_reason = f"adapter output for {case_id} was not valid JSON"
                break
            if not isinstance(record, dict):
                abort_reason = f"adapter record for {case_id} must be a JSON object"
                break
            if record.get(contract.id_field) != case_id:
                abort_reason = f"adapter record id mismatch for {case_id}"
                break
            if str(case_id) in records:
                abort_reason = f"duplicate adapter record for {case_id}"
                break
            missing = [field for field in contract.record_required if field not in record]
            if missing:
                abort_reason = f"adapter record for {case_id} missing fields: {', '.join(missing)}"
                break
            records[str(case_id)] = record
            raw_rows.append(
                {
                    "case_id": case_id,
                    "served_payload_sha256": sha256_text(line_in),
                    "record_sha256": sha256_text(compact(record)),
                    "raw_output_line": line_out.rstrip("\n"),
                }
            )
    finally:
        if proc.stdin is not None:
            proc.stdin.close()
        if proc.stdout is not None:
            proc.stdout.read()
        stderr = proc.stderr.read() if proc.stderr is not None else ""
        returncode = proc.wait()

    if abort_reason is None and returncode != 0:
        abort_reason = f"adapter exited with code {returncode}: {stderr.strip()[-500:]}"
    if abort_reason is not None:
        return abort(abort_reason, len(records))

    if contract.copy_guard:
        expected_compact = {
            compact(item["expected"]) for item in items if isinstance(item.get("expected"), dict)
        }
        copy_violations = [case_id for case_id, record in records.items() if compact(record) in expected_compact]
        if copy_violations:
            print(
                json.dumps(
                    {
                        "run_status": "COPY_GUARD_FAIL",
                        "reason": "candidate records byte-match dataset expected records (self-fulfilling evidence; automatic disqualifier)",
                        "violations": copy_violations,
                    },
                    indent=2,
                )
            )
            return 3

    executed_at = args.executed_at or datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    candidate_system = {
        "system_id": args.candidate_id,
        "operator": args.operator,
        "overlap_disclosure": args.overlap_disclosure,
        "adapter_protocol": "ndjson-stdin-stdout-v1",
    }
    candidate = {
        "contract": contract.contract_id,
        "candidate_system": candidate_system,
        "executed_at": executed_at,
        contract.rows_key: [records[str(item[contract.id_field])] for item in items],
    }
    raw_outputs = {
        "contract": contract.contract_id,
        "candidate_system": candidate_system,
        "executed_at": executed_at,
        "adapter_command": args.adapter,
        "rows": raw_rows,
    }
    args.candidate_results.write_text(json.dumps(candidate, indent=2) + "\n", encoding="utf-8")
    args.raw_outputs.write_text(json.dumps(raw_outputs, indent=2) + "\n", encoding="utf-8")

    scorer_cmd = [
        sys.executable,
        str(contract.scorer),
        "--dataset",
        str(dataset_path),
        "--candidate-results",
        str(args.candidate_results),
        "--output",
        str(args.report),
    ]
    scored = subprocess.run(scorer_cmd, capture_output=True, text=True)
    if not args.report.exists():
        return abort("scorer produced no report: " + scored.stderr[-500:])
    report = json.loads(args.report.read_text(encoding="utf-8"))
    print(
        json.dumps(
            {
                "run_status": "REPORTED",
                "benchmark_status": report.get("benchmark_status"),
                "report": str(args.report),
                "candidate_results": str(args.candidate_results),
                "raw_outputs": str(args.raw_outputs),
                "candidate_results_sha256": sha256_text(args.candidate_results.read_text(encoding="utf-8")),
            },
            indent=2,
        )
    )
    status = report.get("benchmark_status")
    if status == "PASS":
        return 0
    if status in {"FAIL", "OBSERVED_FAILURE"}:
        return 1
    return 2


if __name__ == "__main__":
    sys.exit(main())
