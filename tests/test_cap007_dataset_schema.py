from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator, FormatChecker, ValidationError

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "benchmarks" / "retrieval" / "cap007-dataset.schema.json"

QUERY_TYPES = ["exact_match", "paraphrase", "multi_hop", "no_relevant_document"]


def load_schema():
    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


def labeled_fixture(count: int = 100):
    # Synthetic schema fixture only. It is not an empirical dataset and must
    # never be used to claim CAP-007 performance.
    cases = []
    for i in range(1, count + 1):
        query_type = QUERY_TYPES[(i - 1) % 4]
        cases.append(
            {
                "case_id": f"CAP007-TEST-{i:03d}",
                "query": f"Synthetic schema test support query {i}",
                "query_type": query_type,
                "expected_skill_ids": []
                if query_type == "no_relevant_document"
                else [f"07-tool-use/skill-{i}"],
                "labeling": {
                    "labeler_id": "schema-test-fixture",
                    "labeled_at": "2026-10-11T00:00:00Z",
                    "evidence_references": [f"fixture://case/{i}"],
                    "rationale": "Synthetic rationale used only to test schema acceptance.",
                },
            }
        )
    return {
        "schema_version": "1.0",
        "benchmark_id": "cap007-retrieval-human-v1",
        "dataset_status": "human_labeled",
        "provenance": {
            "source_type": "support_tickets",
            "created_at": "2026-10-11T00:00:00Z",
            "label_protocol": "Synthetic schema test fixture, not actual human labels.",
            "source_references": ["fixture://cap007-schema-test"],
            "labels_independent_of_retrieval_engine": True,
            "inter_labeler_agreement": 0.0,
            "limitations": ["synthetic test data; not benchmark evidence"],
        },
        "cases": cases,
    }


def validate(dataset, schema):
    Draft202012Validator(schema, format_checker=FormatChecker()).validate(dataset)


def test_cap007_schema_is_valid_and_accepts_100_case_shape():
    schema = load_schema()
    Draft202012Validator.check_schema(schema)
    dataset = labeled_fixture()
    validate(dataset, schema)
    assert len(dataset["cases"]) == 100
    assert dataset["provenance"]["labels_independent_of_retrieval_engine"] is True


def test_cap007_schema_rejects_fewer_than_100_cases():
    schema = load_schema()
    dataset = labeled_fixture(99)
    with pytest.raises(ValidationError):
        validate(dataset, schema)


def test_cap007_schema_requires_all_query_types():
    schema = load_schema()
    dataset = labeled_fixture()
    for case in dataset["cases"]:
        case["query_type"] = "exact_match"
        if not case["expected_skill_ids"]:
            case["expected_skill_ids"] = ["07-tool-use/skill-x"]
    with pytest.raises(ValidationError):
        validate(dataset, schema)


def test_cap007_schema_rejects_no_relevant_case_with_expected_skills():
    schema = load_schema()
    dataset = labeled_fixture()
    for case in dataset["cases"]:
        if case["query_type"] == "no_relevant_document":
            case["expected_skill_ids"] = ["07-tool-use/web-search"]
            break
    with pytest.raises(ValidationError):
        validate(dataset, schema)


def test_cap007_schema_rejects_relevant_case_without_expected_skills():
    schema = load_schema()
    dataset = labeled_fixture()
    for case in dataset["cases"]:
        if case["query_type"] != "no_relevant_document":
            case["expected_skill_ids"] = []
            break
    with pytest.raises(ValidationError):
        validate(dataset, schema)


def test_cap007_schema_rejects_labels_derived_from_engine():
    schema = load_schema()
    dataset = labeled_fixture()
    dataset["provenance"]["labels_independent_of_retrieval_engine"] = False
    with pytest.raises(ValidationError):
        validate(dataset, schema)


def test_cap007_schema_rejects_missing_labeler_evidence():
    schema = load_schema()
    dataset = labeled_fixture()
    del dataset["cases"][0]["labeling"]["evidence_references"]
    with pytest.raises(ValidationError):
        validate(dataset, schema)


def test_cap007_schema_rejects_unlabeled_template_as_empirical_dataset():
    schema = load_schema()
    dataset = labeled_fixture()
    dataset["dataset_status"] = "template_only"
    with pytest.raises(ValidationError):
        validate(dataset, schema)
