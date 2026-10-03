from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator

from tools.export_skills import SKILL_SCHEMA, build_index

ROOT = Path(__file__).resolve().parent.parent


def test_registered_skill_gets_registry_context():
    skills = build_index()
    item = next(skill for skill in skills if skill["id"] == "code-review")
    context = item["registry_context"]

    assert context["canonical_id"] == "05-code/code-review"
    assert context["canonical"] is True
    assert context["capability_ids"] == ["capability/code-quality"]
    assert context["implementation_ids"] == ["implementation/code-reviewer-system"]
    assert context["evidence_ids"] == []
    assert context["provenance"]["source_type"] == "repository"


def test_unregistered_skill_has_no_registry_context():
    skills = build_index()
    item = next(skill for skill in skills if skill["id"] == "image-understanding")
    assert "registry_context" not in item


def test_registry_context_is_optional_in_export_schema():
    assert "registry_context" in SKILL_SCHEMA["properties"]
    assert "registry_context" not in SKILL_SCHEMA["required"]


def test_generated_registry_context_projection_matches_universal_registry():
    api = json.loads((ROOT / "docs/api/skills.json").read_text(encoding="utf-8"))
    schema = json.loads((ROOT / "docs/api/skills-schema.json").read_text(encoding="utf-8"))
    Draft202012Validator(schema).validate(api["skills"][0])

    contexts = {
        item["registry_context"]["canonical_id"]: item["registry_context"]
        for item in api["skills"]
        if "registry_context" in item
    }
    assert set(contexts) == {
        "03-memory/rag",
        "05-code/code-review",
        "11-web/web-search",
    }
    assert contexts["05-code/code-review"]["implementation_ids"] == [
        "implementation/code-reviewer-system"
    ]
    assert contexts["05-code/code-review"]["evidence_ids"] == []


def test_unregistered_generated_entries_do_not_get_invented_context():
    api = json.loads((ROOT / "docs/api/skills.json").read_text(encoding="utf-8"))
    item = next(skill for skill in api["skills"] if skill["id"] == "image-understanding")
    assert "registry_context" not in item
