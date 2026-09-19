"""Regression coverage for Capability-to-Adapter semantic linkage."""

import json
from pathlib import Path

import pytest

from registry.runtime import UniversalRegistry

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "registry" / "universal_registry.json"


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

    with pytest.raises(ValueError, match="Capability/adapter linkage is not symmetric"):
        UniversalRegistry(registry_path)
