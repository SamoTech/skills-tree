"""Deterministic runtime access to capability-linked ontology records."""

from __future__ import annotations

from copy import deepcopy
from typing import TYPE_CHECKING, Any, TypedDict

if TYPE_CHECKING:
    from .runtime import UniversalRegistry


class CapabilityRecord(TypedDict):
    """Normative runtime shape for a registered Capability."""
    id: str
    version: str
    name: str
    description: str
    skills: list[str]
    implementations: list[str]
    adapters: list[str]
    provenance: dict[str, Any]


class CapabilityRuntime:
    """Read-only deterministic access to Capability relationships."""

    def __init__(self, registry: UniversalRegistry) -> None:
        self.registry = registry

    def resolve_capability(self, capability_id: str) -> CapabilityRecord:
        """Return one validated Capability by canonical ID."""
        matches = [
            item
            for item in self.registry.data["entities"]["capabilities"]
            if item["id"] == capability_id
        ]
        if not matches:
            raise KeyError(f"Unknown capability: {capability_id}")
        return deepcopy(matches[0])

    def implementations_for_capability(self, capability_id: str) -> list[dict[str, Any]]:
        """Return Capability-linked Implementations in deterministic order."""
        capability = self.resolve_capability(capability_id)
        return deepcopy(
            sorted(
                (
                    self.registry.resolve_implementation(implementation_id)
                    for implementation_id in capability["implementations"]
                ),
                key=lambda item: item["id"],
            )
        )

    def adapters_for_capability(self, capability_id: str) -> list[dict[str, Any]]:
        """Return Capability-linked Adapters in deterministic order."""
        capability = self.resolve_capability(capability_id)
        return deepcopy(
            sorted(
                (
                    self.registry.resolve_adapter(adapter_id)
                    for adapter_id in capability["adapters"]
                ),
                key=lambda item: item["id"],
            )
        )
