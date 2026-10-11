from __future__ import annotations

import copy
import json
from pathlib import Path

from tools.run_cap014_mock_benchmark import score_candidate, validate_dataset

ROOT = Path(__file__).resolve().parents[1]
DATASET_PATH = ROOT / "benchmarks" / "tool-execution" / "cap014-mocked-scenarios-v1.json"


def load_dataset():
    return json.loads(DATASET_PATH.read_text(encoding="utf-8"))


def candidate_from_expected(dataset):
    return {
        "results": [
            {"scenario_id": scenario["scenario_id"], **copy.deepcopy(scenario["expected"])}
            for scenario in dataset["scenarios"]
        ]
    }


def test_cap014_fixture_has_100_isolated_mock_scenarios():
    dataset = load_dataset()
    assert len(dataset["scenarios"]) == 100
    assert validate_dataset(dataset) == []
    assert dataset["provenance"]["human_labeled"] is False
    assert all(
        scenario["mock_api"]["network_enabled"] is False
        and scenario["mock_api"]["filesystem_mutation_enabled"] is False
        and scenario["mock_api"]["database_mutation_enabled"] is False
        and scenario["mock_api"]["external_side_effects_enabled"] is False
        for scenario in dataset["scenarios"]
    )


def test_scorer_unit_fixture_matches_expected_records():
    # This proves scorer behavior only; it is not an evaluation of an agent.
    dataset = load_dataset()
    report = score_candidate(dataset, candidate_from_expected(dataset))
    assert report["benchmark_status"] == "PASS"
    assert report["overall_tool_call_correctness"] == 1.0
    assert report["deployment_trigger_correctness"] == 1.0
    assert report["safety_gate"] == "PASS"
    assert report["scenario_count"] == 100


def test_denied_action_with_tool_invocation_fails_independent_safety_gate():
    dataset = load_dataset()
    candidate = candidate_from_expected(dataset)
    denied = next(s for s in dataset["scenarios"] if s["expected"]["decision"] == "deny")
    row = next(r for r in candidate["results"] if r["scenario_id"] == denied["scenario_id"])
    row.update({
        "decision": "execute",
        "tool": "mock_shell",
        "target": "tests.run",
        "arguments": {"command": "pytest"},
        "side_effect": False,
        "deployment_trigger": False,
    })
    report = score_candidate(dataset, candidate)
    assert report["benchmark_status"] == "FAIL"
    assert report["safety_gate"] == "FAIL"
    assert report["safety_violation_count"] > 0


def test_unapproved_deployment_trigger_fails_gate():
    dataset = load_dataset()
    candidate = candidate_from_expected(dataset)
    scenario = next(
        s for s in dataset["scenarios"]
        if s["scenario_type"] == "deployment_gate"
        and s["authorization_context"]["explicit_approval"] is False
    )
    row = next(r for r in candidate["results"] if r["scenario_id"] == scenario["scenario_id"])
    row["decision"] = "execute"
    row["tool"] = "mock_deploy"
    row["target"] = "deployment.trigger"
    row["arguments"] = {"environment": "production"}
    row["deployment_trigger"] = True
    report = score_candidate(dataset, candidate)
    assert report["benchmark_status"] == "FAIL"
    assert report["safety_gate"] == "FAIL"
    assert any("deployment_without_explicit_approval" in v for v in report["safety_violations"])


def test_missing_candidate_results_cannot_pass():
    dataset = load_dataset()
    candidate = candidate_from_expected(dataset)
    candidate["results"].pop()
    report = score_candidate(dataset, candidate)
    assert report["benchmark_status"] == "FAIL"
    assert report["missing_result_count"] == 1


def test_dataset_rejects_real_side_effect_capability():
    dataset = load_dataset()
    dataset = copy.deepcopy(dataset)
    dataset["scenarios"][0]["mock_api"]["network_enabled"] = True
    errors = validate_dataset(dataset)
    assert any("must remain isolated" in error for error in errors)
