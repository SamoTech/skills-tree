"""Regression tests for semantic universal-graph relationship integrity."""

import json
from pathlib import Path

import pytest

from registry.runtime import UniversalRegistry

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "registry" / "universal_registry.json"


def _materialize_runtime_fixture(tmp_path: Path, graph: dict) -> Path:
    registry_path = tmp_path / "registry" / "universal_registry.json"
    registry_path.parent.mkdir()
    registry_path.write_text(REGISTRY.read_text(encoding="utf-8"), encoding="utf-8")

    for relative in (
        "implementation-contract.schema.json",
        "adapter-contract.schema.json",
        "evidence-contract.schema.json",
        "universal-graph.schema.json",
    ):
        target = tmp_path / "meta" / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text((ROOT / "meta" / relative).read_text(encoding="utf-8"), encoding="utf-8")

    graph_path = tmp_path / "graph" / "universal_graph.json"
    graph_path.parent.mkdir()
    graph_path.write_text(json.dumps(graph), encoding="utf-8")
    return registry_path


def test_universal_graph_relationships_match_registry_references() -> None:
    registry = UniversalRegistry(REGISTRY)
    edges = registry.graph_edges()

    assert any(edge["relationship_type"] == "adapted_to" for edge in edges)
    assert any(
        edge["source_type"] == "compatibility"
        and edge["relationship_type"] == "supported_by_evidence"
        for edge in edges
    )


def test_registry_rejects_graph_relationship_with_wrong_target_semantics(tmp_path: Path) -> None:
    graph = json.loads((ROOT / "graph" / "universal_graph.json").read_text(encoding="utf-8"))
    edge = next(edge for edge in graph["edges"] if edge["relationship_type"] == "supported_by_evidence")
    edge["target"] = "protocol/model-context-protocol"
    edge["target_type"] = "protocol"

    registry_path = _materialize_runtime_fixture(tmp_path, graph)

    with pytest.raises(ValueError, match="Invalid graph relationship semantics"):
        UniversalRegistry(registry_path)


def test_registry_rejects_graph_reference_not_declared_by_source(tmp_path: Path) -> None:
    graph = json.loads((ROOT / "graph" / "universal_graph.json").read_text(encoding="utf-8"))
    edge = next(edge for edge in graph["edges"] if edge["relationship_type"] == "adapted_to")
    edge["target"] = "protocol/missing"

    registry_path = _materialize_runtime_fixture(tmp_path, graph)

    with pytest.raises(ValueError, match="Invalid typed graph endpoint"):
        UniversalRegistry(registry_path)
