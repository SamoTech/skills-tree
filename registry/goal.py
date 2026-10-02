"""Deterministic runtime access to validated Goal ontology records."""

from __future__ import annotations

from copy import deepcopy
from typing import TYPE_CHECKING, Any, TypedDict

if TYPE_CHECKING:
    from .runtime import UniversalRegistry


class GoalRecord(TypedDict):
    """Normative runtime shape for a registered Goal."""
    id: str
    version: str
    name: str
    capabilities: list[str]
    provenance: dict[str, Any]


class GoalRuntime:
    """Read-only deterministic access to Goal relationships."""

    def __init__(self, registry: UniversalRegistry) -> None:
        self.registry = registry

    def resolve_goal(self, goal_id: str) -> GoalRecord:
        """Return one validated Goal by canonical ID."""
        matches = [item for item in self.registry.data["entities"]["goals"] if item["id"] == goal_id]
        if not matches:
            raise KeyError(f"Unknown goal: {goal_id}")
        return deepcopy(matches[0])

    def capabilities_for_goal(self, goal_id: str) -> list[dict[str, Any]]:
        """Return Capabilities linked to a Goal in deterministic order."""
        goal = self.resolve_goal(goal_id)
        return [
            self.registry.resolve_capability(capability_id)
            for capability_id in sorted(goal["capabilities"])
        ]

    def skills_for_goal(self, goal_id: str) -> list[dict[str, Any]]:
        """Return canonical Skills reachable from a Goal in deterministic order."""
        skill_ids = {
            skill_id
            for capability in self.capabilities_for_goal(goal_id)
            for skill_id in capability["skills"]
        }
        return [self.registry.resolve_skill(skill_id) for skill_id in sorted(skill_ids)]
