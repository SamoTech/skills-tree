"""Empirical CAP-011 run evidence tests.

The committed candidate records (benchmarks/self-evaluation/cap011-candidate-results-v1.json)
are re-scored by the fail-closed benchmark runner on every push: CI is the
executor of record for the empirical run, and the committed report
(benchmarks/self-evaluation/cap011-benchmark-report-v1.json) must match the
runner output exactly with acceptance status PASS. The runner rejects
self-adjudication; hallucination verdicts must come from a reviewer other
than the candidate system (here: the deterministic verifier).
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BENCH = ROOT / "benchmarks" / "self-evaluation"
RUNNER = ROOT / "tools" / "run_cap011_calibration_benchmark.py"
DATASET = BENCH / "cap011-dataset-v1.json"
CANDIDATE = BENCH / "cap011-candidate-results-v1.json"
RAW_OUTPUTS = BENCH / "cap011-raw-outputs-v1.json"
REPORT = BENCH / "cap011-benchmark-report-v1.json"


def test_candidate_run_matches_committed_report(tmp_path):
    out = tmp_path / "report.json"
    proc = subprocess.run(
        [sys.executable, str(RUNNER), "--candidate-results", str(CANDIDATE), "--output", str(out)],
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    actual = json.loads(out.read_text(encoding="utf-8"))
    committed = json.loads(REPORT.read_text(encoding="utf-8"))
    assert actual == committed, "committed CAP-011 benchmark report drifted from the runner output"
    assert actual["benchmark_status"] == "PASS"
    assert actual["acceptance"]["status"] == "PASS"


def test_raw_outputs_are_retained_and_consistent_with_candidate_records():
    candidate = json.loads(CANDIDATE.read_text(encoding="utf-8"))
    raw = json.loads(RAW_OUTPUTS.read_text(encoding="utf-8"))
    dataset = json.loads(DATASET.read_text(encoding="utf-8"))
    runs = candidate["runs"]
    raw_by_id = {row["case_id"]: row for row in raw["raw_outputs"]}
    task_inputs = {case["case_id"]: case["task_input"] for case in dataset["cases"]}
    assert len(runs) == 100
    assert len(raw_by_id) == 100
    for run in runs:
        case_id = run["case_id"]
        expected_ref = "benchmarks/self-evaluation/cap011-raw-outputs-v1.json#case:" + case_id
        assert run["raw_output_ref"] == expected_ref
        row = raw_by_id[case_id]
        assert row["predicted_outcome"] == run["predicted_outcome"]
        assert row["confidence"] == run["confidence"]
        digest = hashlib.sha256(task_inputs[case_id].encode("utf-8")).hexdigest()
        assert row["task_input_sha256"] == digest


def test_candidate_system_disclosure_and_independent_adjudication():
    candidate = json.loads(CANDIDATE.read_text(encoding="utf-8"))
    system = candidate["candidate_system"]
    assert system["system_id"]
    assert "overlap" in system["overlap_disclosure"].lower()
    for run in candidate["runs"]:
        assert run["hallucination_adjudication"]["reviewer_id"] != system["system_id"]
        assert run["hallucination_adjudication"]["verdict"] in {"grounded", "hallucinated"}
