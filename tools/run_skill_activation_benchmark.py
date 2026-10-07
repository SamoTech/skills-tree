#!/usr/bin/env python3
"""Measure skill activation/invocation from externally captured trace observations.

This tool does not simulate an agent, infer activation from prompt text, or claim
that a deterministic fixture is a real model-routing result. Observations must
contain explicit skill selection/execution events emitted by an agent runtime.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import defaultdict
from pathlib import Path

from jsonschema import Draft202012Validator


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_observations(path: Path, schema_path: Path) -> list[dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    errors = sorted(Draft202012Validator(schema).iter_errors(data), key=lambda e: list(e.path))
    if errors:
        raise ValueError(f"observations do not match schema: {errors[0].message}")
    return data["runs"]



def validate_observation_integrity(runs: list[dict], cases: list[dict]) -> None:
    known_case_ids = {case["id"] for case in cases}
    seen_run_ids: set[str] = set()
    seen_trace_ids: set[str] = set()
    unknown_cases: list[str] = []

    for run in runs:
        run_id = run["run_id"]
        if run_id in seen_run_ids:
            raise ValueError(f"duplicate observation run_id: {run_id}")
        seen_run_ids.add(run_id)

        trace_id = run["trace_id"]
        if trace_id in seen_trace_ids:
            raise ValueError(f"duplicate observation trace_id: {trace_id}")
        seen_trace_ids.add(trace_id)

        case_id = run["case_id"]
        if case_id not in known_case_ids:
            unknown_cases.append(case_id)

    if unknown_cases:
        unknown = sorted(set(unknown_cases))
        raise ValueError(f"observation case_id is not present in selected dataset: {unknown}")

def event_ids(run: dict, kind: str) -> set[str]:
    result = set()
    for event in run.get("events", []):
        if event.get("kind") == kind and event.get("skill_id"):
            result.add(event["skill_id"])
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", default="benchmarks/activation/skill-activation-v1.json")
    parser.add_argument("--observations", required=True)
    parser.add_argument("--observation-schema", default="meta/skill-activation-observation.schema.json")
    parser.add_argument("--output", default="skill-activation-benchmark-result.json")
    args = parser.parse_args()

    dataset_path = Path(args.dataset)
    observations_path = Path(args.observations)
    cases = json.loads(dataset_path.read_text(encoding="utf-8"))["cases"]
    runs = load_observations(observations_path, Path(args.observation_schema))
    validate_observation_integrity(runs, cases)

    by_case: dict[str, list[dict]] = defaultdict(list)
    for run in runs:
        case_id = run.get("case_id")
        if case_id:
            by_case[case_id].append(run)

    rows = []
    activation_hits = 0
    invocation_hits = 0
    false_activations = 0
    observed_cases = 0
    variance_values = []

    for case in cases:
        case_runs = by_case.get(case["id"], [])
        case_activation = []
        case_invocation = []
        case_false = []
        for run in case_runs:
            selected = event_ids(run, "skill_selection")
            executed = event_ids(run, "skill_execution")
            expected_hit = case["expected_skill"] in selected
            invocation_hit = case["expected_skill"] in executed
            false_hit = bool(selected & set(case["must_not_activate"]))
            case_activation.append(expected_hit)
            case_invocation.append(invocation_hit)
            case_false.append(false_hit)

        required_repetitions = int(case.get("repetitions", 1))
        observed = len(case_runs)
        if observed:
            observed_cases += 1
            activation_hits += sum(case_activation)
            invocation_hits += sum(case_invocation)
            false_activations += sum(case_false)
            variance_values.append(max(case_activation) - min(case_activation))

        rows.append({
            "id": case["id"],
            "observed_runs": observed,
            "required_repetitions": required_repetitions,
            "completion_status": ("COMPLETE" if observed >= required_repetitions else ("PARTIAL" if observed else "NO_OBSERVATIONS")),
            "expected_skill": case["expected_skill"],
            "activation_hits": sum(case_activation),
            "invocation_evidence_hits": sum(case_invocation),
            "false_activation_hits": sum(case_false),
            "activation_rate": round(sum(case_activation) / observed, 4) if observed else None,
            "invocation_evidence_rate": round(sum(case_invocation) / observed, 4) if observed else None,
            "activation_variance": (max(case_activation) - min(case_activation)) if observed else None,
            "status": ("COMPLETE" if observed >= required_repetitions else ("PARTIAL" if observed else "NO_OBSERVATIONS"))
        })

    total_runs = sum(len(v) for v in by_case.values())
    complete_cases = sum(
        1 for case in cases if len(by_case.get(case["id"], [])) >= int(case.get("repetitions", 1))
    )
    partial_cases = sum(
        1 for case in cases if 0 < len(by_case.get(case["id"], [])) < int(case.get("repetitions", 1))
    )
    if not observed_cases:
        overall_status = "NO_OBSERVATIONS"
    elif complete_cases == len(cases):
        overall_status = "COMPLETE"
    else:
        overall_status = "PARTIAL"
    result = {
        "schema_version": "1.0",
        "benchmark_id": "benchmark/skill-activation-v1",
        "benchmark_version": "1.0",
        "status": overall_status,
        "dataset_sha256": sha256(dataset_path),
        "observation_sha256": sha256(observations_path),
        "metrics": {
            "cases": len(cases),
            "observed_cases": observed_cases,
            "complete_cases": complete_cases,
            "partial_cases": partial_cases,
            "required_runs": sum(int(case.get("repetitions", 1)) for case in cases),
            "runs": total_runs,
            "expected_activation_rate": round(activation_hits / total_runs, 4) if total_runs else None,
            "false_activation_rate": round(false_activations / total_runs, 4) if total_runs else None,
            "invocation_evidence_rate": round(invocation_hits / total_runs, 4) if total_runs else None,
            "max_activation_variance": max(variance_values) if variance_values else None
        },
        "cases_detail": rows,
        "interpretation": "Measures observed routing/activation and explicit invocation evidence from runtime traces. It does not infer activation from prompt text, simulate model behavior, or claim general agent success. NO_OBSERVATIONS and PARTIAL are not complete empirical corpora; COMPLETE requires every dataset case to meet its declared repetitions contract."
    }
    Path(args.output).write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    if not observed_cases:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
