"""Base classes for all AgentForge skills."""
from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass
class SkillInput:
    data: dict[str, Any] = field(default_factory=dict)
    context: dict[str, Any] = field(default_factory=dict)


@dataclass
class SkillOutput:
    success: bool = True
    data: dict[str, Any] = field(default_factory=dict)
    error: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    # Convenience: flatten top-level keys as attributes
    def __getattr__(self, name: str) -> Any:
        if name in self.data:
            return self.data[name]
        raise AttributeError(name)


class BaseSkill(ABC):
    """Every skill must inherit this and implement `execute`."""
    name: str = ""
    description: str = ""
    category: str = "general"
    tags: list[str] = []
    level: str = "basic"          # basic | intermediate | advanced
    stability: str = "stable"     # stable | experimental | deprecated
    input_schema: dict = {}
    output_schema: dict = {}

    @abstractmethod
    async def execute(self, inp: SkillInput) -> SkillOutput:
        """Execute the skill. Must be async."""
        ...

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
            "category": self.category,
            "tags": self.tags,
            "level": self.level,
            "stability": self.stability,
            "input_schema": self.input_schema,
            "output_schema": self.output_schema,
        }

    def __repr__(self) -> str:
        return f"<Skill:{self.name}>"
