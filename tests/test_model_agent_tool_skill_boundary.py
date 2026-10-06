import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_model_agent_tool_skill_boundary_is_machine_and_doc_consistent():
    skill_schema = json.loads((ROOT / "meta/skill-schema.json").read_text(encoding="utf-8"))
    registry_schema = json.loads((ROOT / "meta/universal-registry.schema.json").read_text(encoding="utf-8"))
    glossary = (ROOT / "meta/glossary.md").read_text(encoding="utf-8")
    architecture = (ROOT / "docs/architecture/CURRENT_ARCHITECTURE.md").read_text(encoding="utf-8")

    assert "procedural guidance" in skill_schema["description"]
    assert "capability" in skill_schema["description"]
    assert "model" in skill_schema["description"]
    assert "tools/runtime" in skill_schema["description"]
    skill_description = registry_schema["$defs"]["skillDefinition"]["allOf"][0]["description"]
    assert "procedural guidance" in skill_description
    assert "models" in skill_description
    assert "tools" in skill_description
    assert "authorization" in skill_description

    for entity_type in ("capability", "skill", "tool", "model"):
        assert entity_type in registry_schema["entity_types"]

    assert "**Capability**" in glossary
    assert "**Model**" in glossary
    assert "**Skill**" in glossary
    assert "**Tool**" in glossary
    assert "Capability = what needs to be done" in architecture
    assert "Skill = reusable procedural guidance" in architecture
    assert "authorization remains a separate runtime/security concern" in architecture
