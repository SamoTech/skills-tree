import json
from pathlib import Path

import pytest
from jsonschema import ValidationError

from registry.runtime import UniversalRegistry


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "registry" / "universal_registry.json"


def test_registry_resolves_goal_to_capability_to_canonical_skills() -> None:
    registry = UniversalRegistry(REGISTRY)

    skills = registry.skills_for_goal("goal/research-and-analysis")

    assert [skill["id"] for skill in skills] == [
        "03-memory/rag",
        "11-web/web-search",
    ]
    assert all(skill["canonical"] is True for skill in skills)


def test_registry_resolution_is_deterministic() -> None:
    registry = UniversalRegistry(REGISTRY)

    first = registry.skills_for_goal("goal/research-and-analysis")
    second = registry.skills_for_goal("goal/research-and-analysis")

    assert first == second


def test_registry_rejects_unknown_goal() -> None:
    registry = UniversalRegistry(REGISTRY)

    with pytest.raises(KeyError, match="Unknown goal"):
        registry.resolve_goal("goal/does-not-exist")


def test_registry_rejects_dangling_references(tmp_path: Path) -> None:
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    data["entities"]["goals"][0]["capabilities"].append("capability/missing")
    broken = tmp_path / "broken.json"
    broken.write_text(json.dumps(data), encoding="utf-8")

    with pytest.raises(ValueError, match="Dangling capability reference"):
        UniversalRegistry(broken)


def test_registry_provenance_points_to_existing_repository_sources() -> None:
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))

    for entity_type in ("goals", "capabilities", "skills"):
        for entity in data["entities"][entity_type]:
            source = entity["provenance"]["source"]
            assert (ROOT / source).is_file(), source


def test_first_implementation_slice_links_to_canonical_skill_and_evidence() -> None:
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    implementations = {item["id"]: item for item in data["entities"]["implementations"]}
    evidence = {item["id"]: item for item in data["entities"]["evidence"]}
    skills = {item["id"]: item for item in data["entities"]["skills"]}

    implementation = implementations["implementation/code-reviewer-system"]
    assert implementation["skill"] == "05-code/code-review"
    assert skills[implementation["skill"]]["canonical"] is True
    assert implementation["status"] == "candidate"
    assert implementation["provenance"]["source"] == "implementations/code_reviewer.py"
    assert implementation["evidence"] == ["evidence/code-reviewer-system-source", "evidence/code-reviewer-runtime"]
    assert evidence["evidence/code-reviewer-system-source"]["source"] == "systems/code-reviewer.md"
    assert evidence["evidence/code-reviewer-runtime"]["source"] == "implementations/code_reviewer.py"


def test_implementation_source_exists() -> None:
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    implementation = data["entities"]["implementations"][0]
    assert (ROOT / implementation["provenance"]["source"]).is_file()


def test_first_real_adapter_is_registered_as_candidate() -> None:
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    adapter = next(item for item in data["entities"]["adapters"] if item["id"] == "adapter/code-reviewer-mcp")
    assert adapter["status"] == "candidate"
    implementation = next(
        item for item in data["entities"]["implementations"]
        if item["id"] == "implementation/code-reviewer-system"
    )
    assert implementation["status"] == "candidate"

def test_registry_validates_implementation_and_evidence_links() -> None:
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    data["entities"]["implementations"][0]["evidence"] = ["evidence/missing"]
    broken = REGISTRY.parent / "test-broken-implementation.json"
    broken.write_text(json.dumps(data), encoding="utf-8")
    try:
        with pytest.raises(ValueError, match="Dangling implementation evidence reference"):
            UniversalRegistry(broken)
    finally:
        broken.unlink(missing_ok=True)


def test_registry_has_first_class_mcp_protocol_target() -> None:
    registry = UniversalRegistry(REGISTRY)
    protocols = registry.data["entities"]["protocols"]
    assert protocols == [{
        "id": "protocol/model-context-protocol",
        "version": "1.0",
        "name": "Model Context Protocol",
        "provenance": {
            "source_type": "repository",
            "source": "mcp/server.py",
        },
    }]


def test_registry_rejects_dangling_adapter_target(tmp_path: Path) -> None:
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    data["entities"]["adapters"].append({
        "id": "adapter/test-mcp",
        "version": "1.0",
        "name": "Test MCP adapter",
        "implementation": "implementation/code-reviewer-system",
        "targets": [{"type": "protocol", "id": "protocol/missing"}],
        "input_mapping": [],
        "output_mapping": [],
        "auth_requirements": [],
        "runtime_requirements": [],
        "constraints": [],
        "limitations": [],
        "provenance": {"source_type": "repository", "source": "mcp/server.py"},
        "evidence": ["evidence/code-reviewer-system-source"],
        "status": "candidate",
    })
    broken = tmp_path / "broken-adapter.json"
    broken.write_text(json.dumps(data), encoding="utf-8")
    with pytest.raises(ValueError, match="Dangling adapter target reference"):
        UniversalRegistry(broken)

def test_first_real_mcp_adapter_links_implementation_protocol_and_evidence() -> None:
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    adapter = next(item for item in data["entities"]["adapters"] if item["id"] == "adapter/code-reviewer-mcp")
    assert adapter["implementation"] == "implementation/code-reviewer-system"
    assert adapter["targets"] == [{"type": "protocol", "id": "protocol/model-context-protocol"}]
    assert adapter["evidence"] == ["evidence/code-reviewer-runtime", "evidence/code-reviewer-mcp-boundary"]
    assert adapter["status"] == "candidate"


def test_first_compatibility_fact_is_conditional_and_evidence_backed() -> None:
    registry = UniversalRegistry(REGISTRY)

    facts = registry.compatibility_for(
        "adapter/code-reviewer-mcp",
        target_type="protocol",
        target_id="protocol/model-context-protocol",
    )

    assert [fact["id"] for fact in facts] == ["compatibility/code-reviewer-mcp-model-context-protocol"]
    assert facts[0]["status"] == "conditional"
    assert facts[0]["evidence"] == ["evidence/code-reviewer-mcp-boundary"]


def test_registry_rejects_dangling_compatibility_target(tmp_path: Path) -> None:
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    data["entities"]["compatibilities"][0]["target"]["id"] = "protocol/missing"
    broken = tmp_path / "broken-compatibility.json"
    broken.write_text(json.dumps(data), encoding="utf-8")

    with pytest.raises(ValueError, match="Dangling compatibility target reference"):
        UniversalRegistry(broken)



def test_registry_rejects_schema_invalid_entity_types(tmp_path: Path) -> None:
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    data["entities"]["goals"][0]["name"] = 123
    broken = tmp_path / "schema-invalid.json"
    broken.write_text(json.dumps(data), encoding="utf-8")

    with pytest.raises(ValidationError):
        UniversalRegistry(broken)
