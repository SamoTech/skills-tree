"""Regression tests for typed Capability runtime access."""

from pathlib import Path

import pytest

from registry.capability import CapabilityRuntime
from registry.runtime import UniversalRegistry

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "registry" / "universal_registry.json"


def test_resolve_capability_returns_normative_record() -> None:
    registry = UniversalRegistry(REGISTRY_PATH)
    runtime = CapabilityRuntime(registry)
    capability = runtime.resolve_capability("capability/code-quality")
    assert capability["id"] == "capability/code-quality"
    assert capability["implementations"] == ["implementation/code-reviewer-system"]
    assert capability["adapters"] == ["adapter/code-reviewer-mcp"]


def test_implementations_for_capability_are_deterministic() -> None:
    runtime = CapabilityRuntime(UniversalRegistry(REGISTRY_PATH))
    implementations = runtime.implementations_for_capability("capability/code-quality")
    assert [item["id"] for item in implementations] == ["implementation/code-reviewer-system"]


def test_adapters_for_capability_are_deterministic() -> None:
    runtime = CapabilityRuntime(UniversalRegistry(REGISTRY_PATH))
    adapters = runtime.adapters_for_capability("capability/code-quality")
    assert [item["id"] for item in adapters] == ["adapter/code-reviewer-mcp"]


def test_unknown_capability_is_rejected() -> None:
    runtime = CapabilityRuntime(UniversalRegistry(REGISTRY_PATH))
    with pytest.raises(KeyError, match="Unknown capability"):
        runtime.resolve_capability("capability/missing")
    with pytest.raises(KeyError, match="Unknown capability"):
        runtime.implementations_for_capability("capability/missing")
    with pytest.raises(KeyError, match="Unknown capability"):
        runtime.adapters_for_capability("capability/missing")


def test_capability_runtime_returns_independent_snapshots() -> None:
    runtime = CapabilityRuntime(UniversalRegistry(REGISTRY_PATH))
    capability = runtime.resolve_capability("capability/code-quality")
    capability["implementations"].clear()
    assert runtime.resolve_capability("capability/code-quality")["implementations"]

    implementations = runtime.implementations_for_capability("capability/code-quality")
    implementations[0]["status"] = "verified"
    assert runtime.implementations_for_capability("capability/code-quality")[0]["status"] == "candidate"

    adapters = runtime.adapters_for_capability("capability/code-quality")
    adapters[0]["status"] = "verified"
    assert runtime.adapters_for_capability("capability/code-quality")[0]["status"] == "candidate"



def test_universal_registry_exposes_typed_capability_runtime_boundary() -> None:
    registry = UniversalRegistry(REGISTRY_PATH)
    capability = registry.resolve_capability("capability/code-quality")
    assert capability["id"] == "capability/code-quality"
    assert [item["id"] for item in registry.implementations_for_capability("capability/code-quality")] == [
        "implementation/code-reviewer-system"
    ]
    assert [item["id"] for item in registry.adapters_for_capability("capability/code-quality")] == [
        "adapter/code-reviewer-mcp"
    ]


def test_universal_registry_capability_boundary_rejects_unknown_capability() -> None:
    registry = UniversalRegistry(REGISTRY_PATH)
    with pytest.raises(KeyError, match="Unknown capability"):
        registry.resolve_capability("capability/missing")
    with pytest.raises(KeyError, match="Unknown capability"):
        registry.implementations_for_capability("capability/missing")
    with pytest.raises(KeyError, match="Unknown capability"):
        registry.adapters_for_capability("capability/missing")
