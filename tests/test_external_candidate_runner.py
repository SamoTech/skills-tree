"""Tests for tools/run_external_candidate.py.

These are mechanical tests of the generalized external-candidate runner
(NDJSON adapter protocol, digest retention, copy guard, fail-closed aborts).
They are NOT evidence that any candidate passed a benchmark: the adapters
below are deterministic test stubs, never a candidate system run.
"""
from __future__ import annotations

import hashlib
import json
import shlex
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / "tools" / "run_external_candidate.py"
CAP014_DATASET = ROOT / "benchmarks" / "tool-execution" / "cap014-mocked-scenarios-v1.json"
CAP011_DATASET = ROOT / "benchmarks" / "self-evaluation" / "cap011-dataset-v1.json"

DENY_ADAPTER = """import json
import sys

for line in sys.stdin:
    served = json.loads(line)
    record = {
        "scenario_id": served["scenario_id"],
        "decision": "deny",
        "tool": None,
        "target": None,
        "arguments": None,
        "authorization_context": {"scopes": []},
        "side_effect": False,
        "deployment_trigger": False,
        "observed_rationale": "deterministic test stub: unconditional deny",
    }
    sys.stdout.write(json.dumps(record) + "\\n")
    sys.stdout.flush()
"""

CAP011_ADAPTER = """import json
import sys

for line in sys.stdin:
    served = json.loads(line)
    record = {
        "case_id": served["case_id"],
        "predicted_outcome": "pass",
        "confidence": 0.95,
        "review_gate_routed": True,
        "raw_output_ref": "raw://test-stub/" + served["case_id"],
        "hallucination_adjudication": {
            "verdict": "grounded",
            "reviewer_id": "independent-test-reviewer",
            "adjudicated_at": "2026-10-14T00:00:00Z",
            "evidence_references": ["test://stub"],
        },
    }
    sys.stdout.write(json.dumps(record) + "\\n")
    sys.stdout.flush()
"""

CHEAT_ADAPTER = """import json
import sys
from pathlib import Path

dataset = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
expected_by_id = {s["scenario_id"]: s["expected"] for s in dataset["scenarios"]}

for line in sys.stdin:
    served = json.loads(line)
    record = dict(expected_by_id[served["scenario_id"]])
    sys.stdout.write(json.dumps(record) + "\\n")
    sys.stdout.flush()
"""

CRASH_ADAPTER = """import sys

sys.stdin.readline()
sys.exit(3)
"""


def compact(obj: object) -> str:
    return json.dumps(obj, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def write_adapter(tmp_path: Path, body: str) -> str:
    script = tmp_path / "adapter.py"
    script.write_text(body, encoding="utf-8")
    return " ".join([sys.executable, shlex.quote(str(script))])


def run_runner(contract: str, adapter: str, tmp_path: Path, extra: list[str] | None = None) -> subprocess.CompletedProcess:
    cmd = [
        sys.executable,
        str(RUNNER),
        "--contract",
        contract,
        "--adapter",
        adapter,
        "--candidate-id",
        "test-candidate",
        "--operator",
        "ci",
        "--overlap-disclosure",
        "test stub adapter; not a candidate system run",
        "--executed-at",
        "2026-10-14T00:00:00Z",
        "--raw-outputs",
        str(tmp_path / "raw.json"),
        "--candidate-results",
        str(tmp_path / "candidate.json"),
        "--report",
        str(tmp_path / "report.json"),
    ]
    if extra:
        cmd.extend(extra)
    return subprocess.run(cmd, capture_output=True, text=True)


def test_cap014_deny_adapter_produces_scored_report(tmp_path: Path) -> None:
    result = run_runner("cap014", write_adapter(tmp_path, DENY_ADAPTER), tmp_path)
    assert result.returncode == 1, result.stdout + result.stderr
    report = json.loads((tmp_path / "report.json").read_text(encoding="utf-8"))
    assert report["benchmark_id"] == "cap014-tool-execution-mocked-v1"
    assert report["benchmark_status"] == "FAIL"
    assert report["scenario_count"] == 100
    assert report["candidate_result_count"] == 100

    raw = json.loads((tmp_path / "raw.json").read_text(encoding="utf-8"))
    assert len(raw["rows"]) == 100
    assert raw["candidate_system"]["overlap_disclosure"]
    dataset = json.loads(CAP014_DATASET.read_text(encoding="utf-8"))
    served = {k: v for k, v in dataset["scenarios"][0].items() if k != "expected"}
    assert raw["rows"][0]["served_payload_sha256"] == hashlib.sha256(compact(served).encode("utf-8")).hexdigest()

    candidate = json.loads((tmp_path / "candidate.json").read_text(encoding="utf-8"))
    assert candidate["candidate_system"]["system_id"] == "test-candidate"
    assert raw["rows"][0]["record_sha256"] == hashlib.sha256(compact(candidate["results"][0]).encode("utf-8")).hexdigest()
    assert "expected" not in json.loads(raw["rows"][0]["raw_output_line"])


def test_runner_is_reproducible_with_fixed_timestamp(tmp_path: Path) -> None:
    adapter = write_adapter(tmp_path, DENY_ADAPTER)
    first = run_runner("cap014", adapter, tmp_path)
    assert first.returncode == 1, first.stdout + first.stderr
    candidate_before = (tmp_path / "candidate.json").read_text(encoding="utf-8")
    raw_before = (tmp_path / "raw.json").read_text(encoding="utf-8")
    report_before = (tmp_path / "report.json").read_text(encoding="utf-8")
    second = run_runner("cap014", adapter, tmp_path)
    assert second.returncode == 1, second.stdout + second.stderr
    assert (tmp_path / "candidate.json").read_text(encoding="utf-8") == candidate_before
    assert (tmp_path / "raw.json").read_text(encoding="utf-8") == raw_before
    assert (tmp_path / "report.json").read_text(encoding="utf-8") == report_before


def test_cap011_adapter_pipeline_scores_all_cases(tmp_path: Path) -> None:
    result = run_runner("cap011", write_adapter(tmp_path, CAP011_ADAPTER), tmp_path)
    assert result.returncode in (0, 1), result.stdout + result.stderr
    report = json.loads((tmp_path / "report.json").read_text(encoding="utf-8"))
    dataset = json.loads(CAP011_DATASET.read_text(encoding="utf-8"))
    assert report["benchmark_id"] == "cap011-self-evaluation-v1"
    assert report["case_count"] == len(dataset["cases"])
    assert report["benchmark_status"] in {"PASS", "OBSERVED_FAILURE", "NEEDS_INVESTIGATION"}
    assert "overall_correctness" in report
    candidate = json.loads((tmp_path / "candidate.json").read_text(encoding="utf-8"))
    assert len(candidate["runs"]) == len(dataset["cases"])
    raw = json.loads((tmp_path / "raw.json").read_text(encoding="utf-8"))
    assert len(raw["rows"]) == len(dataset["cases"])


def test_copy_guard_aborts_on_expected_echo(tmp_path: Path) -> None:
    adapter = write_adapter(tmp_path, CHEAT_ADAPTER) + " " + shlex.quote(str(CAP014_DATASET))
    result = run_runner("cap014", adapter, tmp_path)
    assert result.returncode == 3, result.stdout + result.stderr
    assert "COPY_GUARD_FAIL" in result.stdout
    assert not (tmp_path / "report.json").exists()


def test_runner_aborts_fail_closed_on_adapter_crash(tmp_path: Path) -> None:
    result = run_runner("cap014", write_adapter(tmp_path, CRASH_ADAPTER), tmp_path)
    assert result.returncode == 2, result.stdout + result.stderr
    payload = json.loads(result.stdout)
    assert payload["run_status"] == "ABORTED"
    assert not (tmp_path / "report.json").exists()
    assert not (tmp_path / "candidate.json").exists()
