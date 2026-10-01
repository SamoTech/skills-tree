"""Regression tests for typed Goal runtime access."""

from pathlib import Path

import pytest

from registry.goal import GoalRuntime
from registry.runtime import UniversalRegistry

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "registry" / "universal_registry.json"


def test_resolve_goal_returns_normative_record() -> None:
    runtime = GoalRuntime(UniversalRegistry(REGISTRY_PATH))
    goal = runtime.resolve_goal("goal/software-engineering")
    assert goal["id"] == "goal/software-engineering"
    assert goal["capabilities"] == ["capability/code-quality"]


def test_skills_for_goal_is_deterministic() -> None:
    registry = UniversalRegistry(REGISTRY_PATH)
    first = registry.skills_for_goal("goal/research-and-analysis")
    second = registry.skills_for_goal("goal/research-and-analysis")
    assert [item["id"] for item in first] == sorted(item["id"] for item in first)
    assert first == second


def test_universal_registry_exposes_typed_goal_runtime_boundary() -> None:
    registry = UniversalRegistry(REGISTRY_PATH)
    goal = registry.resolve_goal("goal/software-engineering")
    assert goal["id"] == "goal/software-engineering"
    assert [item["id"] for item in registry.skills_for_goal("goal/software-engineering")] == [
        "05-code/code-review"
    ]


def test_unknown_goal_is_rejected() -> None:
    registry = UniversalRegistry(REGISTRY_PATH)
    with pytest.raises(KeyError, match="Unknown goal"):
        registry.resolve_goal("goal/missing")
    with pytest.raises(KeyError, match="Unknown goal"):
        registry.skills_for_goal("goal/missing")


def test_goal_runtime_returns_defensive_snapshots() -> None:
    runtime = GoalRuntime(UniversalRegistry(REGISTRY_PATH))
    goal = runtime.resolve_goal("goal/software-engineering")
    goal["capabilities"].clear()
    assert runtime.resolve_goal("goal/software-engineering")["capabilities"]
