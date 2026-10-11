from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator, FormatChecker, ValidationError

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "benchmarks" / "self-evaluation" / "cap011-dataset.schema.json"


def load_schema():
    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


def reviewed_fixture(count: int = 100):
    # Synthetic schema fixture only. It is not an empirical dataset and must
    # never be used to claim CAP-011 performance.
    return {
        "schema_version": "1.0",
        "benchmark_id": "cap011-self-evaluation-v1",
        "dataset_status": "ground_truth_reviewed",
        "provenance": {
            "source_type": "human_reviewed",
            "created_at": "2026-10-11T00:00:00Z",
            "label_protocol": "Synthetic schema test fixture, not actual human labels.",
            "source_references": ["fixture://cap011-schema-test"],
            "ground_truth_independent_of_system_under_test": True,
            "double_adjudication_fraction": 0.0,
            "limitations": ["synthetic test data; not benchmark evidence"],
        },
        "cases": [
            {
                "case_id": f"CAP011-TEST-{i:03d}",
                "task_input": f"Synthetic schema test case {i}",
                "evidence_context": [f"fixture evidence {i}"],
                "expected_outcome": "pass" if i % 2 == 0 else "fail",
                "adjudication": {
                    "reviewer_id": "schema-test-fixture",
                    "reviewed_at": "2026-10-11T00:00:00Z",
                    "evidence_references": [f"fixture://case/{i}"],
                    "rationale": "Synthetic rationale used only to test schema acceptance.",
                },
            }
            for i in range(1, count + 1)
        ],
    }


def test_cap011_schema_is_valid_and_accepts_100_case_shape():
    schema = load_schema()
    Draft202012Validator.check_schema(schema)
    dataset = reviewed_fixture()
    Draft202012Validator(schema, format_checker=FormatChecker()).validate(dataset)
    assert len(dataset["cases"]) == 100
    assert dataset["provenance"]["ground_truth_independent_of_system_under_test"] is True


def test_cap011_schema_rejects_fewer_than_100_cases():
    schema = load_schema()
    dataset = reviewed_fixture(99)
    with pytest.raises(ValidationError):
        Draft202012Validator(schema, format_checker=FormatChecker()).validate(dataset)


def test_cap011_schema_rejects_ground_truth_not_independent():
    schema = load_schema()
    dataset = reviewed_fixture()
    dataset["provenance"]["ground_truth_independent_of_system_under_test"] = False
    with pytest.raises(ValidationError):
        Draft202012Validator(schema, format_checker=FormatChecker()).validate(dataset)


def test_cap011_schema_rejects_missing_adjudication_evidence():
    schema = load_schema()
    dataset = reviewed_fixture()
    del dataset["cases"][0]["adjudication"]["evidence_references"]
    with pytest.raises(ValidationError):
        Draft202012Validator(schema, format_checker=FormatChecker()).validate(dataset)


def test_cap011_schema_rejects_unreviewed_template_as_empirical_dataset():
    schema = load_schema()
    dataset = reviewed_fixture()
    dataset["dataset_status"] = "template_only"
    with pytest.raises(ValidationError):
        Draft202012Validator(schema, format_checker=FormatChecker()).validate(dataset)
