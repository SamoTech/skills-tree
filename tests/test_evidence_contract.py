"""Regression tests for Evidence contract enforcement."""

import json
from pathlib import Path

import pytest

from registry.runtime import UniversalRegistry

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "registry" / "universal_registry.json"


def _copy_runtime_contracts(tmp_path: Path) -> None:
    for relative_path in (
        "meta/implementation-contract.schema.json",
        "meta/adapter-contract.schema.json",
        "meta/evidence-contract.schema.json",
        "meta/universal-graph.schema.json",
    ):
        source = ROOT / relative_path
        target = tmp_path / relative_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")
    graph_source = ROOT / "graph" / "universal_graph.json"
    graph_target = tmp_path / "graph" / "universal_graph.json"
    graph_target.parent.mkdir(parents=True, exist_ok=True)
    graph_target.write_text(graph_source.read_text(encoding="utf-8"), encoding="utf-8")


def test_registry_initialization_accepts_current_evidence_contract() -> None:
    registry = UniversalRegistry(REGISTRY_PATH)
    evidence = registry.data["entities"]["evidence"]
    assert evidence
    assert all(item["supports"] for item in evidence)
    assert all(item["provenance"].get("source") for item in evidence)


def test_registry_initialization_rejects_evidence_without_supports(tmp_path: Path) -> None:
    registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    registry["entities"]["evidence"][0]["supports"] = []

    registry_path = tmp_path / "registry" / "universal_registry.json"
    registry_path.parent.mkdir(parents=True)
    registry_path.write_text(json.dumps(registry), encoding="utf-8")
    _copy_runtime_contracts(tmp_path)

    with pytest.raises(Exception):
        UniversalRegistry(registry_path)


def test_registry_initialization_rejects_evidence_without_provenance_source(tmp_path: Path) -> None:
    registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    registry["entities"]["evidence"][0]["provenance"].pop("source")

    registry_path = tmp_path / "registry" / "universal_registry.json"
    registry_path.parent.mkdir(parents=True)
    registry_path.write_text(json.dumps(registry), encoding="utf-8")
    _copy_runtime_contracts(tmp_path)

    with pytest.raises(Exception):
        UniversalRegistry(registry_path)
