"""Regression tests for adapter contract enforcement at registry initialization."""

import json
from pathlib import Path

import pytest

from registry.runtime import UniversalRegistry

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "registry" / "universal_registry.json"


def test_registry_initialization_validates_adapter_contract(tmp_path: Path) -> None:
    registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    registry["entities"]["adapters"][0].pop("input_mapping")

    registry_path = tmp_path / "registry" / "universal_registry.json"
    registry_path.parent.mkdir()
    registry_path.write_text(json.dumps(registry), encoding="utf-8")

    for relative_path in (
        "meta/implementation-contract.schema.json",
        "meta/adapter-contract.schema.json",
        "meta/universal-graph.schema.json",
    ):
        source = ROOT / relative_path
        target = tmp_path / relative_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")

    with pytest.raises(Exception):
        UniversalRegistry(registry_path)
