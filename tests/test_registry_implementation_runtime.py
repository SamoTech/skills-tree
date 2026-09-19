"""Regression tests for typed Implementation runtime access."""

import json
from pathlib import Path

import pytest

from registry.runtime import UniversalRegistry

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "registry" / "universal_registry.json"


def test_resolve_implementation_returns_normative_record() -> None:
    registry = UniversalRegistry(REGISTRY_PATH)
    implementation = registry.resolve_implementation("implementation/code-reviewer-system")
    assert implementation["id"] == "implementation/code-reviewer-system"
    assert implementation["skill"] == "05-code/code-review"
    assert implementation["type"] == "composite"
    assert implementation["interface"] == "python-module"
    assert implementation["status"] == "candidate"


def test_implementations_for_skill_are_deterministic() -> None:
    registry = UniversalRegistry(REGISTRY_PATH)
    implementations = registry.implementations_for_skill("05-code/code-review")
    assert [item["id"] for item in implementations] == ["implementation/code-reviewer-system"]


def test_unknown_implementation_and_skill_are_rejected() -> None:
    registry = UniversalRegistry(REGISTRY_PATH)
    with pytest.raises(KeyError, match="Unknown implementation"):
        registry.resolve_implementation("implementation/missing")
    with pytest.raises(KeyError, match="Unknown skill"):
        registry.implementations_for_skill("05-code/missing")


def test_registry_initialization_validates_implementation_contract(tmp_path: Path) -> None:
    registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    registry["entities"]["implementations"][0].pop("interface")
    registry_path = tmp_path / "registry" / "universal_registry.json"
    registry_path.parent.mkdir()
    registry_path.write_text(json.dumps(registry), encoding="utf-8")
    contract = ROOT / "meta" / "implementation-contract.schema.json"
    contract_target = tmp_path / "meta" / "implementation-contract.schema.json"
    contract_target.parent.mkdir()
    contract_target.write_text(contract.read_text(encoding="utf-8"), encoding="utf-8")
    graph = ROOT / "graph" / "universal_graph.json"
    graph_target = tmp_path / "graph" / "universal_graph.json"
    graph_target.parent.mkdir()
    graph_target.write_text(graph.read_text(encoding="utf-8"), encoding="utf-8")
    graph_contract = ROOT / "meta" / "universal-graph.schema.json"
    graph_contract_target = tmp_path / "meta" / "universal-graph.schema.json"
    graph_contract_target.write_text(graph_contract.read_text(encoding="utf-8"), encoding="utf-8")
    adapter_contract = ROOT / "meta" / "adapter-contract.schema.json"
    adapter_contract_target = tmp_path / "meta" / "adapter-contract.schema.json"
    adapter_contract_target.write_text(adapter_contract.read_text(encoding="utf-8"), encoding="utf-8")
    with pytest.raises(Exception):
        UniversalRegistry(registry_path)


def test_verified_implementation_requires_evidence_and_traceable_provenance(tmp_path: Path) -> None:
    registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    implementation = registry["entities"]["implementations"][0]
    implementation["status"] = "verified"
    implementation["evidence"] = []
    registry_path = tmp_path / "registry" / "universal_registry.json"
    registry_path.parent.mkdir()
    registry_path.write_text(json.dumps(registry), encoding="utf-8")
    contract = ROOT / "meta" / "implementation-contract.schema.json"
    contract_target = tmp_path / "meta" / "implementation-contract.schema.json"
    contract_target.parent.mkdir()
    contract_target.write_text(contract.read_text(encoding="utf-8"), encoding="utf-8")
    graph = ROOT / "graph" / "universal_graph.json"
    graph_target = tmp_path / "graph" / "universal_graph.json"
    graph_target.parent.mkdir()
    graph_target.write_text(graph.read_text(encoding="utf-8"), encoding="utf-8")
    graph_contract = ROOT / "meta" / "universal-graph.schema.json"
    graph_contract_target = tmp_path / "meta" / "universal-graph.schema.json"
    graph_contract_target.write_text(graph_contract.read_text(encoding="utf-8"), encoding="utf-8")
    adapter_contract = ROOT / "meta" / "adapter-contract.schema.json"
    adapter_contract_target = tmp_path / "meta" / "adapter-contract.schema.json"
    adapter_contract_target.write_text(adapter_contract.read_text(encoding="utf-8"), encoding="utf-8")
    with pytest.raises(Exception, match="evidence"):
        UniversalRegistry(registry_path)


def test_verified_implementation_evidence_must_support_record(tmp_path: Path) -> None:
    registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    implementation = registry["entities"]["implementations"][0]
    implementation["status"] = "verified"
    evidence = registry["entities"]["evidence"][0]
    evidence["supports"] = []
    registry_path = tmp_path / "registry" / "universal_registry.json"
    registry_path.parent.mkdir()
    registry_path.write_text(json.dumps(registry), encoding="utf-8")
    contract = ROOT / "meta" / "implementation-contract.schema.json"
    contract_target = tmp_path / "meta" / "implementation-contract.schema.json"
    contract_target.parent.mkdir()
    contract_target.write_text(contract.read_text(encoding="utf-8"), encoding="utf-8")
    graph = ROOT / "graph" / "universal_graph.json"
    graph_target = tmp_path / "graph" / "universal_graph.json"
    graph_target.parent.mkdir()
    graph_target.write_text(graph.read_text(encoding="utf-8"), encoding="utf-8")
    graph_contract = ROOT / "meta" / "universal-graph.schema.json"
    graph_contract_target = tmp_path / "meta" / "universal-graph.schema.json"
    graph_contract_target.write_text(graph_contract.read_text(encoding="utf-8"), encoding="utf-8")
    adapter_contract = ROOT / "meta" / "adapter-contract.schema.json"
    adapter_contract_target = tmp_path / "meta" / "adapter-contract.schema.json"
    adapter_contract_target.write_text(adapter_contract.read_text(encoding="utf-8"), encoding="utf-8")
    with pytest.raises(ValueError, match="does not support implementation"):
        UniversalRegistry(registry_path)


def test_verified_implementation_with_supporting_evidence_passes(tmp_path: Path) -> None:
    registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    implementation = registry["entities"]["implementations"][0]
    implementation["status"] = "verified"
    registry_path = tmp_path / "registry" / "universal_registry.json"
    registry_path.parent.mkdir()
    registry_path.write_text(json.dumps(registry), encoding="utf-8")
    contract = ROOT / "meta" / "implementation-contract.schema.json"
    contract_target = tmp_path / "meta" / "implementation-contract.schema.json"
    contract_target.parent.mkdir()
    contract_target.write_text(contract.read_text(encoding="utf-8"), encoding="utf-8")
    graph = ROOT / "graph" / "universal_graph.json"
    graph_target = tmp_path / "graph" / "universal_graph.json"
    graph_target.parent.mkdir()
    graph_target.write_text(graph.read_text(encoding="utf-8"), encoding="utf-8")
    graph_contract = ROOT / "meta" / "universal-graph.schema.json"
    graph_contract_target = tmp_path / "meta" / "universal-graph.schema.json"
    graph_contract_target.write_text(graph_contract.read_text(encoding="utf-8"), encoding="utf-8")
    adapter_contract = ROOT / "meta" / "adapter-contract.schema.json"
    adapter_contract_target = tmp_path / "meta" / "adapter-contract.schema.json"
    adapter_contract_target.write_text(adapter_contract.read_text(encoding="utf-8"), encoding="utf-8")
    UniversalRegistry(registry_path)


def test_implementation_skill_linkage_must_be_symmetric(tmp_path: Path) -> None:
    registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    implementation = registry["entities"]["implementations"][0]
    skill = next(item for item in registry["entities"]["skills"] if item["id"] == implementation["skill"])
    skill["implementations"] = []
    registry_path = tmp_path / "registry" / "universal_registry.json"
    registry_path.parent.mkdir()
    registry_path.write_text(json.dumps(registry), encoding="utf-8")
    with pytest.raises(ValueError, match="not symmetric"):
        UniversalRegistry(registry_path)


def test_implementation_skill_linkage_accepts_symmetric_record() -> None:
    registry = UniversalRegistry(REGISTRY_PATH)
    implementation = registry.resolve_implementation("implementation/code-reviewer-system")
    skill = next(item for item in registry.data["entities"]["skills"] if item["id"] == implementation["skill"])
    assert implementation["id"] in skill["implementations"]


def test_read_only_facade_returns_independent_snapshots() -> None:
    registry = UniversalRegistry(REGISTRY_PATH)
    implementation_id = "implementation/code-reviewer-system"

    data = registry.data
    data["entities"]["implementations"][0]["status"] = "verified"
    assert registry.resolve_implementation(implementation_id)["status"] == "candidate"

    implementation = registry.resolve_implementation(implementation_id)
    implementation["evidence"].clear()
    assert registry.resolve_implementation(implementation_id)["evidence"]

    skills = registry.skills_for_goal("goal/software-engineering")
    skills[0]["implementations"].clear()
    assert registry.implementations_for_skill("05-code/code-review")

    compatibilities = registry.compatibility_for("adapter/code-reviewer-mcp")
    if compatibilities:
        compatibilities[0]["status"] = "incompatible"
        assert registry.compatibility_for("adapter/code-reviewer-mcp")[0]["status"] != "incompatible"

    edges = registry.graph_edges()
    if edges:
        edges[0]["relationship_type"] = "mutated"
        assert registry.graph_edges()[0]["relationship_type"] != "mutated"


def test_registry_initialization_validates_universal_graph_contract(tmp_path: Path) -> None:
    registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    registry_path = tmp_path / "registry" / "universal_registry.json"
    registry_path.parent.mkdir()
    registry_path.write_text(json.dumps(registry), encoding="utf-8")
    contract = ROOT / "meta" / "implementation-contract.schema.json"
    contract_target = tmp_path / "meta" / "implementation-contract.schema.json"
    contract_target.parent.mkdir()
    contract_target.write_text(contract.read_text(encoding="utf-8"), encoding="utf-8")
    graph = json.loads((ROOT / "graph" / "universal_graph.json").read_text(encoding="utf-8"))
    graph["edges"][0]["relationship_type"] = "not-a-real-relationship"
    graph_target = tmp_path / "graph" / "universal_graph.json"
    graph_target.parent.mkdir()
    graph_target.write_text(json.dumps(graph), encoding="utf-8")
    graph_contract_target = tmp_path / "meta" / "universal-graph.schema.json"
    graph_contract_target.write_text((ROOT / "meta" / "universal-graph.schema.json").read_text(encoding="utf-8"), encoding="utf-8")
    adapter_contract = ROOT / "meta" / "adapter-contract.schema.json"
    adapter_contract_target = tmp_path / "meta" / "adapter-contract.schema.json"
    adapter_contract_target.write_text(adapter_contract.read_text(encoding="utf-8"), encoding="utf-8")
    with pytest.raises(Exception):
        UniversalRegistry(registry_path)

def test_registry_initialization_requires_graph_provenance_source(tmp_path: Path) -> None:
    registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    registry_path = tmp_path / "registry" / "universal_registry.json"
    registry_path.parent.mkdir()
    registry_path.write_text(json.dumps(registry), encoding="utf-8")

    contract = ROOT / "meta" / "implementation-contract.schema.json"
    contract_target = tmp_path / "meta" / "implementation-contract.schema.json"
    contract_target.parent.mkdir()
    contract_target.write_text(contract.read_text(encoding="utf-8"), encoding="utf-8")

    graph = json.loads((ROOT / "graph" / "universal_graph.json").read_text(encoding="utf-8"))
    graph["edges"][0]["provenance"].pop("source")
    graph_target = tmp_path / "graph" / "universal_graph.json"
    graph_target.parent.mkdir()
    graph_target.write_text(json.dumps(graph), encoding="utf-8")

    graph_contract = ROOT / "meta" / "universal-graph.schema.json"
    graph_contract_target = tmp_path / "meta" / "universal-graph.schema.json"
    graph_contract_target.write_text(graph_contract.read_text(encoding="utf-8"), encoding="utf-8")
    adapter_contract = ROOT / "meta" / "adapter-contract.schema.json"
    adapter_contract_target = tmp_path / "meta" / "adapter-contract.schema.json"
    adapter_contract_target.write_text(adapter_contract.read_text(encoding="utf-8"), encoding="utf-8")

    with pytest.raises(Exception):
        UniversalRegistry(registry_path)


def test_registry_initialization_requires_entity_provenance_source(tmp_path: Path) -> None:
    registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    registry["entities"]["skills"][0]["provenance"].pop("source")
    registry_path = tmp_path / "registry" / "universal_registry.json"
    registry_path.parent.mkdir()
    registry_path.write_text(json.dumps(registry), encoding="utf-8")

    with pytest.raises(ValueError, match="traceable provenance source"):
        UniversalRegistry(registry_path)


def test_registry_initialization_requires_compatibility_evidence_support(tmp_path: Path) -> None:
    registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    evidence = registry["entities"]["evidence"][-1]
    evidence["supports"].remove("compatibility/code-reviewer-mcp-model-context-protocol")
    registry_path = tmp_path / "registry" / "universal_registry.json"
    registry_path.parent.mkdir()
    registry_path.write_text(json.dumps(registry), encoding="utf-8")
    contract = ROOT / "meta" / "implementation-contract.schema.json"
    contract_target = tmp_path / "meta" / "implementation-contract.schema.json"
    contract_target.parent.mkdir()
    contract_target.write_text(contract.read_text(encoding="utf-8"), encoding="utf-8")
    graph = ROOT / "graph" / "universal_graph.json"
    graph_target = tmp_path / "graph" / "universal_graph.json"
    graph_target.parent.mkdir()
    graph_target.write_text(graph.read_text(encoding="utf-8"), encoding="utf-8")
    graph_contract = ROOT / "meta" / "universal-graph.schema.json"
    graph_contract_target = tmp_path / "meta" / "universal-graph.schema.json"
    graph_contract_target.write_text(graph_contract.read_text(encoding="utf-8"), encoding="utf-8")
    adapter_contract = ROOT / "meta" / "adapter-contract.schema.json"
    adapter_contract_target = tmp_path / "meta" / "adapter-contract.schema.json"
    adapter_contract_target.write_text(adapter_contract.read_text(encoding="utf-8"), encoding="utf-8")
    with pytest.raises(ValueError, match="does not support compatibility"):
        UniversalRegistry(registry_path)


def test_registry_initialization_requires_adapter_evidence_support(tmp_path: Path) -> None:
    registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    evidence = next(
        item
        for item in registry["entities"]["evidence"]
        if item["id"] == "evidence/code-reviewer-mcp-boundary"
    )
    evidence["supports"].remove("adapter/code-reviewer-mcp")
    registry_path = tmp_path / "registry" / "universal_registry.json"
    registry_path.parent.mkdir()
    registry_path.write_text(json.dumps(registry), encoding="utf-8")

    for schema_name in (
        "implementation-contract.schema.json",
        "universal-graph.schema.json",
        "adapter-contract.schema.json",
    ):
        source = ROOT / "meta" / schema_name
        target = tmp_path / "meta" / schema_name
        target.parent.mkdir(exist_ok=True)
        target.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")

    graph = ROOT / "graph" / "universal_graph.json"
    graph_target = tmp_path / "graph" / "universal_graph.json"
    graph_target.parent.mkdir()
    graph_target.write_text(graph.read_text(encoding="utf-8"), encoding="utf-8")

    with pytest.raises(ValueError, match="does not support adapter"):
        UniversalRegistry(registry_path)
