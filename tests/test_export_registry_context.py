from __future__ import annotations

from tools.export_skills import SKILL_SCHEMA, build_index


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
