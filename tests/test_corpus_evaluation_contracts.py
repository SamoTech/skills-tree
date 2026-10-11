from __future__ import annotations

import copy
import json
from pathlib import Path

from tools.validate_corpus_evaluation_contracts import validate_contracts

ROOT = Path(__file__).resolve().parents[1]


def load_json(relative_path: str):
    return json.loads((ROOT / relative_path).read_text(encoding="utf-8"))


def current_contracts():
    capability_ontology = load_json("intelligence/ontology/capability_ontology.json")
    evaluation_ontology = load_json("intelligence/ontology/evaluation_ontology.json")
    corpus_entries = [
        json.loads(path.read_text(encoding="utf-8"))
        for path in sorted((ROOT / "intelligence/corpus/entries").rglob("*.json"))
    ]
    return capability_ontology, evaluation_ontology, corpus_entries


def test_current_corpus_evaluation_contracts_are_structurally_aligned():
    capability_ontology, evaluation_ontology, corpus_entries = current_contracts()
    assert all(
        requirement["contract_scope"] == "scenario_specific"
        for entry in corpus_entries
        for requirement in entry["evaluation_requirements"]
    )
    assert validate_contracts(capability_ontology, evaluation_ontology, corpus_entries) == []


def test_scenario_specific_method_and_threshold_may_differ_from_generic_baseline():
    capability_ontology, evaluation_ontology, corpus_entries = current_contracts()
    support = next(entry for entry in corpus_entries if entry["entry_id"] == "CORPUS-001")
    classification = next(item for item in support["evaluation_requirements"] if item["capability"] == "CAP-003")
    mapping = next(item for item in evaluation_ontology["capability_evaluation_mappings"] if item["cap_id"] == "CAP-003")
    assert classification["eval_method"] != mapping["validation_method"]
    assert classification["pass_threshold"] == mapping["minimum_required_score"]
    # Engineering's stricter classification threshold is also valid scenario-specific scope.
    engineering = next(entry for entry in corpus_entries if entry["entry_id"] == "CORPUS-002")
    failure_classification = next(item for item in engineering["evaluation_requirements"] if item["capability"] == "CAP-003")
    assert failure_classification["pass_threshold"] > mapping["minimum_required_score"]
    assert validate_contracts(capability_ontology, evaluation_ontology, corpus_entries) == []


def test_generic_baseline_requires_matching_method_and_minimum_threshold():
    capability_ontology, evaluation_ontology, corpus_entries = current_contracts()
    corpus_entries = copy.deepcopy(corpus_entries)
    support = next(entry for entry in corpus_entries if entry["entry_id"] == "CORPUS-001")
    requirement = next(item for item in support["evaluation_requirements"] if item["capability"] == "CAP-003")
    requirement["contract_scope"] = "generic_baseline"
    requirement["eval_method"] = "different_method"
    errors = validate_contracts(capability_ontology, evaluation_ontology, corpus_entries)
    assert any("generic_baseline eval_method must match" in error for error in errors)


def test_missing_generic_mapping_is_reported():
    capability_ontology, evaluation_ontology, corpus_entries = current_contracts()
    evaluation_ontology = copy.deepcopy(evaluation_ontology)
    evaluation_ontology["capability_evaluation_mappings"] = [
        item for item in evaluation_ontology["capability_evaluation_mappings"]
        if item["cap_id"] != "CAP-006"
    ]
    errors = validate_contracts(capability_ontology, evaluation_ontology, corpus_entries)
    assert any("no generic evaluation mapping for CAP-006" in error for error in errors)


def test_requirement_must_reference_a_declared_capability():
    capability_ontology, evaluation_ontology, corpus_entries = current_contracts()
    corpus_entries = copy.deepcopy(corpus_entries)
    engineering = next(entry for entry in corpus_entries if entry["entry_id"] == "CORPUS-002")
    engineering["evaluation_requirements"][0]["capability"] = "CAP-999"
    errors = validate_contracts(capability_ontology, evaluation_ontology, corpus_entries)
    assert any("which is not in required_capabilities" in error for error in errors)


def test_unknown_metric_id_is_reported():
    capability_ontology, evaluation_ontology, corpus_entries = current_contracts()
    evaluation_ontology = copy.deepcopy(evaluation_ontology)
    mapping = next(item for item in evaluation_ontology["capability_evaluation_mappings"] if item["cap_id"] == "CAP-003")
    mapping["primary_metrics"] = ["ET-999"]
    errors = validate_contracts(capability_ontology, evaluation_ontology, corpus_entries)
    assert any("unknown evaluation metric 'ET-999'" in error for error in errors)
