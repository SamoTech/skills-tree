"""Regression tests for typed Skill runtime access."""

from pathlib import Path

import pytest

from registry.runtime import UniversalRegistry
from registry.skill import SkillRuntime

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "registry" / "universal_registry.json"


def test_resolve_skill_returns_canonical_record() -> None:
    runtime = SkillRuntime(UniversalRegistry(REGISTRY_PATH))
    skill = runtime.resolve_skill("05-code/code-review")
    assert skill["id"] == "05-code/code-review"
    assert skill["canonical"] is True


def test_capabilities_for_skill_is_deterministic() -> None:
    runtime = SkillRuntime(UniversalRegistry(REGISTRY_PATH))
    first = runtime.capabilities_for_skill("05-code/code-review")
    second = runtime.capabilities_for_skill("05-code/code-review")
    assert [item["id"] for item in first] == sorted(item["id"] for item in first)
    assert first == second


def test_implementations_for_skill_is_deterministic() -> None:
    runtime = SkillRuntime(UniversalRegistry(REGISTRY_PATH))
    implementations = runtime.implementations_for_skill("05-code/code-review")
    assert [item["id"] for item in implementations] == sorted(item["id"] for item in implementations)


def test_unknown_skill_is_rejected() -> None:
    runtime = SkillRuntime(UniversalRegistry(REGISTRY_PATH))
    with pytest.raises(KeyError, match="Unknown skill"):
        runtime.resolve_skill("skill/does-not-exist")


def test_skill_runtime_returns_defensive_snapshots() -> None:
    runtime = SkillRuntime(UniversalRegistry(REGISTRY_PATH))
    skill = runtime.resolve_skill("05-code/code-review")
    original_capabilities = list(skill["capabilities"])
    skill["capabilities"].append("capability/mutated")
    assert runtime.resolve_skill("05-code/code-review")["capabilities"] == original_capabilities



def test_universal_registry_exposes_typed_skill_runtime_boundary() -> None:
    registry = UniversalRegistry(REGISTRY_PATH)
    skill = registry.resolve_skill("05-code/code-review")
    assert skill["canonical"] is True
    capabilities = registry.capabilities_for_skill("05-code/code-review")
    assert [item["id"] for item in capabilities] == sorted(item["id"] for item in capabilities)
    assert [item["id"] for item in registry.implementations_for_skill("05-code/code-review")] == [
        "implementation/code-reviewer-system"
    ]


def test_universal_registry_skill_boundary_rejects_unknown_skill() -> None:
    registry = UniversalRegistry(REGISTRY_PATH)
    with pytest.raises(KeyError, match="Unknown skill"):
        registry.resolve_skill("skill/does-not-exist")
    with pytest.raises(KeyError, match="Unknown skill"):
        registry.capabilities_for_skill("skill/does-not-exist")
    with pytest.raises(KeyError, match="Unknown skill"):
        registry.implementations_for_skill("skill/does-not-exist")
