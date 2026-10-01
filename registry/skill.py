"""Deterministic runtime access to canonical Skill ontology records."""

from __future__ import annotations

from copy import deepcopy
from typing import TYPE_CHECKING, Any, TypedDict

if TYPE_CHECKING:
    from .runtime import UniversalRegistry


class SkillRecord(TypedDict):
    """Normative runtime shape for a canonical Skill."""

    id: str
    version: str
    name: str
    description: str
    canonical: bool
    capabilities: list[str]
    implementations: list[str]
    provenance: dict[str, Any]


class SkillRuntime:
    """Read-only deterministic access to canonical Skill relationships."""

    def __init__(self, registry: UniversalRegistry) -> None:
        self.registry = registry

    def resolve_skill(self, skill_id: str) -> SkillRecord:
        """Return one validated canonical Skill by ID."""
        matches = [
            item
            for item in self.registry.data["entities"]["skills"]
            if item["id"] == skill_id
        ]
        if not matches:
            raise KeyError(f"Unknown skill: {skill_id}")
        skill = matches[0]
        if skill.get("canonical") is not True:
            raise ValueError(f"Non-canonical skill: {skill_id}")
        return deepcopy(skill)

    def capabilities_for_skill(self, skill_id: str) -> list[dict[str, Any]]:
        """Return linked Capabilities in deterministic order."""
        skill = self.resolve_skill(skill_id)
        capabilities = {
            item["id"]: item
            for item in self.registry.data["entities"]["capabilities"]
        }
        return deepcopy(
            sorted(
                (capabilities[capability_id] for capability_id in skill["capabilities"]),
                key=lambda item: item["id"],
            )
        )

    def implementations_for_skill(self, skill_id: str) -> list[dict[str, Any]]:
        """Return linked Implementations in deterministic order."""
        skill = self.resolve_skill(skill_id)
        return deepcopy(
            sorted(
                (
                    self.registry.resolve_implementation(implementation_id)
                    for implementation_id in skill["implementations"]
                ),
                key=lambda item: item["id"],
            )
        )
