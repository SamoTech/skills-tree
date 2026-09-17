"""Deterministic runtime access to the universal registry seed."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class UniversalRegistry:
    """Read-only registry facade for Goal -> Capability -> Skill resolution."""

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self._data = json.loads(self.path.read_text(encoding="utf-8"))
        self._validate_integrity()

    @property
    def data(self) -> dict[str, Any]:
        return self._data

    def resolve_goal(self, goal_id: str) -> dict[str, Any]:
        matches = [g for g in self._data["entities"]["goals"] if g["id"] == goal_id]
        if not matches:
            raise KeyError(f"Unknown goal: {goal_id}")
        return matches[0]

    def skills_for_goal(self, goal_id: str) -> list[dict[str, Any]]:
        goal = self.resolve_goal(goal_id)
        capabilities = {item["id"]: item for item in self._data["entities"]["capabilities"]}
        skills = {item["id"]: item for item in self._data["entities"]["skills"]}
        result: dict[str, dict[str, Any]] = {}
        for capability_id in goal["capabilities"]:
            capability = capabilities[capability_id]
            for skill_id in capability["skills"]:
                result[skill_id] = skills[skill_id]
        return [result[key] for key in sorted(result)]

    def _validate_integrity(self) -> None:
        entities = self._data.get("entities")
        if not isinstance(entities, dict):
            raise ValueError("Registry must contain an entities object")

        ids: set[str] = set()
        for entity_type, records in entities.items():
            if not isinstance(records, list):
                raise ValueError(f"Entity collection must be a list: {entity_type}")
            for record in records:
                entity_id = record.get("id")
                if not isinstance(entity_id, str) or entity_id in ids:
                    raise ValueError(f"Invalid or duplicate entity id: {entity_id!r}")
                ids.add(entity_id)
                if "version" not in record or "provenance" not in record:
                    raise ValueError(f"Missing universal metadata: {entity_id}")

        capabilities = {x["id"]: x for x in entities["capabilities"]}
        skills = {x["id"]: x for x in entities["skills"]}
        goals = {x["id"]: x for x in entities["goals"]}
        for goal in goals.values():
            for capability_id in goal["capabilities"]:
                if capability_id not in capabilities:
                    raise ValueError(f"Dangling capability reference: {capability_id}")
        for capability in capabilities.values():
            for skill_id in capability["skills"]:
                if skill_id not in skills:
                    raise ValueError(f"Dangling skill reference: {skill_id}")
        for skill in skills.values():
            if skill.get("canonical") is not True:
                raise ValueError(f"Registry skills must be canonical: {skill['id']}")
            for capability_id in skill["capabilities"]:
                if capability_id not in capabilities:
                    raise ValueError(f"Dangling skill capability reference: {capability_id}")
