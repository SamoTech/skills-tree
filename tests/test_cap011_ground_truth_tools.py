"""Tests for the CAP-011 ground-truth verifier and calibration runner.

All candidate records built here are synthetic test fixtures derived from the
dataset's own expected outcomes. They validate the tooling; they are NOT
empirical evidence about any agent's calibration performance.
"""
from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import run_cap011_calibration_benchmark as runner  # noqa: E402
import verify_cap011_ground_truth as verifier  # noqa: E402

DATASET_PATH = ROOT / "benchmarks" / "self-evaluation" / "cap011-dataset-v1.json"
SPEC_PATH = ROOT / "benchmarks" / "self-evaluation" / "cap011-verifier-v1.json"
SCHEMA_PATH = ROOT / "benchmarks" / "self-evaluation" / "cap011-dataset.schema.json"


@pytest.fixture(scope="module")
def loaded():
    dataset = json.loads(DATASET_PATH.read_text(encoding="utf-8"))
    spec = json.loads(SPEC_PATH.read_text(encoding="utf-8"))
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    return dataset, spec, schema


def build_candidate(dataset, confidence=0.97, flip_ids=(), hallucinated_ids=(), unrouted_ids=(), adjudicator="independent-reviewer-x"):
    """Construct a synthetic candidate from the dataset's own expected outcomes."""
    runs = []
    flip = set(flip_ids)
    for case in dataset["cases"]:
        case_id = case["case_id"]
        predicted = case["expected_outcome"]
        if case_id in flip:
            predicted = "fail" if predicted == "pass" else "pass"
        runs.append({
            "case_id": case_id,
            "predicted_outcome": predicted,
            "confidence": 0.5 if case_id in unrouted_ids else confidence,
            "review_gate_routed": case_id not in unrouted_ids,
            "raw_output_ref": f"trace://{case_id}",
            "hallucination_adjudication": {
                "reviewer_id": adjudicator,
                "adjudicated_at": "2026-10-11T16:00:00Z",
                "verdict": "hallucinated" if case_id in hallucinated_ids else "grounded",
                "evidence_references": [f"adjudication://{case_id}"],
            },
        })
    return {
        "schema_version": "1.0",
        "candidate_system": {"system_id": "candidate-system-a", "version": "1.0"},
        "runs": runs,
    }


def test_real_dataset_validates_against_schema_and_predicates(loaded):
    dataset, spec, schema = loaded
    assert verifier.verify_dataset(dataset, spec, schema) == []


def test_dataset_shape(loaded):
    dataset, spec, schema = loaded
    cases = dataset["cases"]
    assert len(cases) == 100
    ids = [case["case_id"] for case in cases]
    assert len(set(ids)) == 100
    outcomes = {case["expected_outcome"] for case in cases}
    assert outcomes == {"pass", "fail"}
    assert dataset["provenance"]["ground_truth_independent_of_system_under_test"] is True
    assert dataset["provenance"]["source_type"] == "controlled_experiment"


def test_verifier_rejects_tampered_outcome(loaded):
    dataset, spec, schema = loaded
    tampered = copy.deepcopy(dataset)
    tampered["cases"][0]["expected_outcome"] = "fail" if tampered["cases"][0]["expected_outcome"] == "pass" else "pass"
    errors = verifier.verify_dataset(tampered, spec, schema)
    assert errors and any("predicate derivation" in error for error in errors)


def test_verifier_rejects_missing_check(loaded):
    dataset, spec, schema = loaded
    trimmed_spec = copy.deepcopy(spec)
    trimmed_spec["checks"] = trimmed_spec["checks"][:-1]
    errors = verifier.verify_dataset(dataset, trimmed_spec, schema)
    assert any("no deterministic check" in error for error in errors)


def test_verifier_rejects_extra_check(loaded):
    dataset, spec, schema = loaded
    extra_spec = copy.deepcopy(spec)
    extra_spec["checks"].append({"case_id": "CAP011-ARITH-999", "predicate_type": "count", "params": {"items": [], "claimed": 0}})
    errors = verifier.verify_dataset(dataset, extra_spec, schema)
    assert any("verifier check has no dataset case" in error for error in errors)


def test_verifier_rejects_wrong_reviewer(loaded):
    dataset, spec, schema = loaded
    tampered = copy.deepcopy(dataset)
    tampered["cases"][0]["adjudication"]["reviewer_id"] = "some-human"
    errors = verifier.verify_dataset(tampered, spec, schema)
    assert any("reviewer must be the deterministic verifier" in error for error in errors)


def test_runner_not_run_without_candidate(loaded):
    dataset, _, _ = loaded
    report = runner.run_benchmark(dataset, None)
    assert report["benchmark_status"] == "NOT_RUN"


def test_perfect_candidate_passes(loaded):
    dataset, _, _ = loaded
    report = runner.score(dataset, build_candidate(dataset))
    assert report["benchmark_status"] == "PASS"
    assert report["high_confidence_correctness"] == 1.0
    assert report["review_gate_compliance"] == 1.0
    assert report["hallucination_rate"] == 0.0
    assert report["high_confidence_case_count"] == 100


def test_hallucination_boundaries(loaded):
    dataset, _, _ = loaded
    case_ids = [case["case_id"] for case in dataset["cases"]]

    one = runner.score(dataset, build_candidate(dataset, hallucinated_ids=case_ids[:1]))
    assert one["hallucination_rate"] == 0.01
    assert one["benchmark_status"] == "PASS"

    six = runner.score(dataset, build_candidate(dataset, hallucinated_ids=case_ids[:6]))
    assert 0.05 < six["hallucination_rate"] <= 0.08
    assert six["benchmark_status"] == "NEEDS_INVESTIGATION"

    nine = runner.score(dataset, build_candidate(dataset, hallucinated_ids=case_ids[:9]))
    assert nine["hallucination_rate"] == 0.09
    assert nine["benchmark_status"] == "OBSERVED_FAILURE"


def test_review_gate_bypass_fails(loaded):
    dataset, _, _ = loaded
    case_ids = [case["case_id"] for case in dataset["cases"]]
    report = runner.score(dataset, build_candidate(dataset, unrouted_ids=case_ids[:1]))
    assert report["benchmark_status"] == "OBSERVED_FAILURE"
    assert report["acceptance"]["failures"], "review-gate bypass must be reported as a failure"


def test_self_adjudication_is_not_run(loaded):
    dataset, _, _ = loaded
    candidate = build_candidate(dataset, adjudicator="candidate-system-a")
    report = runner.score(dataset, candidate)
    assert report["benchmark_status"] == "NOT_RUN"
    assert any("cannot adjudicate" in error for error in report["dataset_validation_errors"])


def test_high_confidence_correctness_threshold(loaded):
    dataset, _, _ = loaded
    high_conf_ids = [case["case_id"] for case in dataset["cases"][:20]]
    candidate = build_candidate(dataset, confidence=0.95)
    for run in candidate["runs"]:
        if run["case_id"] not in high_conf_ids:
            run["confidence"] = 0.5
            run["review_gate_routed"] = True

    one_flip = runner.score(dataset, build_flip(candidate, high_conf_ids[:1]))
    assert one_flip["high_confidence_correctness"] == 0.95
    assert one_flip["benchmark_status"] == "PASS"

    two_flip = runner.score(dataset, build_flip(candidate, high_conf_ids[:2]))
    assert two_flip["high_confidence_correctness"] == 0.9
    assert two_flip["benchmark_status"] == "OBSERVED_FAILURE"


def build_flip(candidate, ids):
    flipped = copy.deepcopy(candidate)
    by_id = {run["case_id"]: run for run in flipped["runs"]}
    for case_id in ids:
        run = by_id[case_id]
        run["predicted_outcome"] = "fail" if run["predicted_outcome"] == "pass" else "pass"
    return flipped


def test_structural_candidate_errors_fail_closed(loaded):
    dataset, _, _ = loaded
    candidate = build_candidate(dataset)
    candidate["runs"] = candidate["runs"][:-1]
    report = runner.score(dataset, candidate)
    assert report["benchmark_status"] == "OBSERVED_FAILURE"
    assert report["dataset_validation_errors"]
