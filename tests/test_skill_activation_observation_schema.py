import json
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "meta/skill-activation-observation.schema.json"


def test_activation_observation_schema_accepts_runtime_trace_shape():
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    payload = {
        "schema_version": "1.0",
        "runs": [
            {
                "run_id": "run-001",
                "case_id": "ACT-001",
                "trace_id": "trace-001",
                "events": [
                    {
                        "kind": "skill_selection",
                        "skill_id": "03-memory/rag",
                        "skill_version": "1.0",
                        "status": "selected",
                        "observed_at": "2026-10-06T10:00:00Z",
                    },
                    {
                        "kind": "skill_execution",
                        "skill_id": "03-memory/rag",
                        "skill_version": "1.0",
                        "status": "ok",
                        "observed_at": "2026-10-06T10:00:01Z",
                    },
                ],
            }
        ],
    }
    errors = list(Draft202012Validator(schema).iter_errors(payload))
    assert errors == []


def test_activation_observation_schema_rejects_inferred_activation_only():
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    payload = {
        "schema_version": "1.0",
        "runs": [
            {
                "run_id": "run-001",
                "case_id": "ACT-001",
                "events": [{"kind": "inferred_activation", "skill_id": "03-memory/rag"}],
            }
        ],
    }
    errors = list(Draft202012Validator(schema).iter_errors(payload))
    assert errors
