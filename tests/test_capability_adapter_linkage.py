"""Regression coverage for Capability-to-Adapter semantic linkage."""

import json
from pathlib import Path

import pytest

from registry.runtime import UniversalRegistry

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "registry" / "universal_registry.json"


def _copy_runtime_contracts(tmp_path: Path) -> None:
    for schema_name in (
        "implementation-contract.schema.json",
        "adapter-contract.schema.json",
        "universal-graph.schema.json",
    ):
        target = tmp_path / "meta" / schema_name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(
            (ROOT / "meta" / schema_name).read_text(encoding="utf-8"),
            encoding="utf-8",
        )
    graph_target = tmp_path / "graph" / "universal_graph.json"
    graph_target.parent.mkdir(parents=True, exist_ok=True)
    graph_target.write_text(
        (ROOT / "graph" / "universal_graph.json").read_text(encoding="utf-8"),
        encoding="utf-8",
    )


def test_capability_adapter_linkage_must_be_symmetric(tmp_path: Path) -> None:
    registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    capability = next(
        item for item in registry["entities"]["capabilities"]
        if item["id"] == "capability/code-quality"
    )
    capability["skills"] = []

    registry_path = tmp_path / "registry" / "universal_registry.json"
    registry_path.parent.mkdir()
    registry_path.write_text(json.dumps(registry), encoding="utf-8")
    _copy_runtime_contracts(tmp_path)

    with pytest.raises(ValueError, match="Capability/adapter linkage is not symmetric"):
        UniversalRegistry(registry_path)
