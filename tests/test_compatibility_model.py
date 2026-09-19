"""Tests for the standalone compatibility model contract."""

import json
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "meta" / "compatibility-model.schema.json"


def test_compatibility_schema_is_valid_and_versioned() -> None:
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    assert schema["properties"]["contract_version"]["const"] == "1.0"
    assert set(schema["properties"]["compatibility"]["required"]) == {
        "id", "version", "name", "subject", "target", "status", "evidence", "provenance"
    }
    assert schema["properties"]["compatibility"]["properties"]["evidence"]["minItems"] == 1
    assert schema["properties"]["compatibility"]["properties"]["provenance"]["required"] == ["source_type", "source"]


def test_compatibility_schema_accepts_conditional_fact() -> None:
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    instance = {
        "contract_version": "1.0",
        "compatibility": {
            "id": "compatibility/example",
            "version": "1.0",
            "name": "Example compatibility",
            "subject": "adapter/example",
            "target": {"type": "protocol", "id": "protocol/example"},
            "status": "conditional",
            "evidence": ["evidence/example"],
            "provenance": {"source_type": "repository", "source": "example.py"},
        },
    }
    errors = list(Draft202012Validator(schema).iter_errors(instance))
    assert errors == []
