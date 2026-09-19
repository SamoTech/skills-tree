"""Deterministic runtime access to the universal registry seed."""

from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
from typing import Any, TypedDict

from jsonschema import Draft202012Validator


class ImplementationRecord(TypedDict):
    """Normative runtime shape for a registered Implementation."""
    id: str
    version: str
    name: str
    skill: str
    type: str
    provider: str | None
    interface: str
    inputs: list[str]
    outputs: list[str]
    requirements: list[str]
    constraints: list[str]
    limitations: list[str]
    provenance: dict[str, Any]
    evidence: list[str]
    status: str


class UniversalRegistry:
    """Read-only registry facade for Goal -> Capability -> Skill resolution."""

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self._data = json.loads(self.path.read_text(encoding="utf-8"))
        self._validate_integrity()
        self._validate_implementation_contracts()
        self._validate_adapter_contracts()
        self._validate_graph_contract()

    @property
    def data(self) -> dict[str, Any]:
        return deepcopy(self._data)

    def resolve_goal(self, goal_id: str) -> dict[str, Any]:
        matches = [g for g in self._data["entities"]["goals"] if g["id"] == goal_id]
        if not matches:
            raise KeyError(f"Unknown goal: {goal_id}")
        return deepcopy(matches[0])

    def skills_for_goal(self, goal_id: str) -> list[dict[str, Any]]:
        goal = self.resolve_goal(goal_id)
        capabilities = {item["id"]: item for item in self._data["entities"]["capabilities"]}
        skills = {item["id"]: item for item in self._data["entities"]["skills"]}
        result: dict[str, dict[str, Any]] = {}
        for capability_id in goal["capabilities"]:
            capability = capabilities[capability_id]
            for skill_id in capability["skills"]:
                result[skill_id] = skills[skill_id]
        return deepcopy([result[key] for key in sorted(result)])

    def resolve_implementation(self, implementation_id: str) -> ImplementationRecord:
        """Return one validated Implementation by canonical ID."""
        matches = [item for item in self._data["entities"]["implementations"] if item["id"] == implementation_id]
        if not matches:
            raise KeyError(f"Unknown implementation: {implementation_id}")
        return deepcopy(matches[0])

    def implementations_for_skill(self, skill_id: str) -> list[ImplementationRecord]:
        """Return validated implementations for a canonical Skill in deterministic order."""
        if not any(item["id"] == skill_id for item in self._data["entities"]["skills"]):
            raise KeyError(f"Unknown skill: {skill_id}")
        return deepcopy(sorted(
            [item for item in self._data["entities"]["implementations"] if item["skill"] == skill_id],
            key=lambda item: item["id"],
        ))

    def compatibility_for(self, subject_id: str, target_type: str | None = None, target_id: str | None = None) -> list[dict[str, Any]]:
        """Return deterministic compatibility facts for an entity."""
        records = [x for x in self._data["entities"].get("compatibilities", []) if x["subject"] == subject_id]
        if target_type is not None:
            records = [x for x in records if x["target"]["type"] == target_type]
        if target_id is not None:
            records = [x for x in records if x["target"]["id"] == target_id]
        return deepcopy(sorted(records, key=lambda x: x["id"]))

    def graph_edges(self) -> list[dict[str, Any]]:
        """Return validated typed universal-graph edges in deterministic order."""
        graph = getattr(self, "_graph_data", None)
        if graph is None:
            graph_path = self.path.parent.parent / "graph" / "universal_graph.json"
            graph = json.loads(graph_path.read_text(encoding="utf-8"))
        entities = self._data["entities"]
        collection_types = {
            "goals": "goal",
            "capabilities": "capability",
            "skills": "skill",
            "implementations": "implementation",
            "tools": "tool",
            "models": "model",
            "platforms": "platform",
            "frameworks": "framework",
            "protocols": "protocol",
            "runtimes": "runtime",
            "adapters": "adapter",
            "evidence": "evidence",
            "benchmarks": "benchmark",
            "architectures": "architecture",
            "compatibilities": "compatibility",
        }
        by_id = {
            record["id"]: collection_types[entity_type]
            for entity_type, records in entities.items()
            for record in records
        }
        edges = graph.get("edges", [])
        for edge in edges:
            if by_id.get(edge["source"]) != edge["source_type"] or by_id.get(edge["target"]) != edge["target_type"]:
                raise ValueError(f"Invalid typed graph endpoint: {edge['source']} -> {edge['target']}")
            if edge["source"] == edge["target"]:
                raise ValueError(f"Graph self-loop: {edge['source']}")
        return deepcopy(sorted(edges, key=lambda x: (x["source"], x["relationship_type"], x["target"])))

    def _validate_graph_contract(self) -> None:
        """Validate the typed universal graph against its normative JSON Schema."""
        graph_path = self.path.parent.parent / "graph" / "universal_graph.json"
        schema_path = self.path.parent.parent / "meta" / "universal-graph.schema.json"
        graph = json.loads(graph_path.read_text(encoding="utf-8"))
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        Draft202012Validator(schema).validate(graph)
        self._graph_data = graph

    def _validate_implementation_contracts(self) -> None:
        """Validate every registered Implementation against the normative contract."""
        schema_path = self.path.parent.parent / "meta" / "implementation-contract.schema.json"
        contract = json.loads(schema_path.read_text(encoding="utf-8"))
        validator = Draft202012Validator(contract)
        evidence = {item["id"]: item for item in self._data["entities"]["evidence"]}
        for implementation in self._data["entities"]["implementations"]:
            validator.validate({"contract_version": "1.0", "implementation": implementation})
            if implementation["status"] != "verified":
                continue
            if not implementation["evidence"]:
                raise ValueError(f"Verified implementation requires evidence: {implementation['id']}")
            if not implementation["provenance"].get("source"):
                raise ValueError(f"Verified implementation requires traceable provenance source: {implementation['id']}")
            unsupported = [
                evidence_id
                for evidence_id in implementation["evidence"]
                if implementation["id"] not in evidence[evidence_id].get("supports", [])
            ]
            if unsupported:
                raise ValueError(
                    f"Verified implementation evidence does not support implementation {implementation['id']}: "
                    + ", ".join(sorted(unsupported))
                )

    def _validate_adapter_contracts(self) -> None:
        """Validate every registered Adapter against the normative contract."""
        schema_path = self.path.parent.parent / "meta" / "adapter-contract.schema.json"
        contract = json.loads(schema_path.read_text(encoding="utf-8"))
        validator = Draft202012Validator(contract)
        evidence = {item["id"]: item for item in self._data["entities"]["evidence"]}
        for adapter in self._data["entities"]["adapters"]:
            validator.validate({"contract_version": "1.0", "adapter": adapter})
            unsupported = [
                evidence_id
                for evidence_id in adapter["evidence"]
                if adapter["id"] not in evidence[evidence_id].get("supports", [])
            ]
            if unsupported:
                raise ValueError(
                    f"Adapter evidence does not support adapter {adapter['id']}: "
                    + ", ".join(sorted(unsupported))
                )

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
                provenance = record["provenance"]
                if not isinstance(provenance, dict) or not provenance.get("source"):
                    raise ValueError(f"Missing traceable provenance source: {entity_id}")

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
        implementations = {x["id"]: x for x in entities["implementations"]}
        evidence = {x["id"]: x for x in entities["evidence"]}
        adapters = {x["id"]: x for x in entities["adapters"]}
        compatibilities = {x["id"]: x for x in entities.get("compatibilities", [])}

        for skill in skills.values():
            if skill.get("canonical") is not True:
                raise ValueError(f"Registry skills must be canonical: {skill['id']}")
            for capability_id in skill["capabilities"]:
                if capability_id not in capabilities:
                    raise ValueError(f"Dangling skill capability reference: {capability_id}")
            for implementation_id in skill.get("implementations", []):
                if implementation_id not in implementations:
                    raise ValueError(f"Dangling skill implementation reference: {implementation_id}")

        for capability in capabilities.values():
            for implementation_id in capability.get("implementations", []):
                if implementation_id not in implementations:
                    raise ValueError(f"Dangling capability implementation reference: {implementation_id}")
                implementation_skill = implementations[implementation_id].get("skill")
                if implementation_skill not in capability.get("skills", []):
                    raise ValueError(
                        f"Capability/implementation linkage is not symmetric: "
                        f"{capability['id']} -> {implementation_id}"
                    )
            for adapter_id in capability.get("adapters", []):
                if adapter_id not in adapters:
                    raise ValueError(f"Dangling capability adapter reference: {adapter_id}")
                adapter_implementation = adapters[adapter_id].get("implementation")
                if adapter_implementation not in implementations:
                    raise ValueError(f"Dangling adapter implementation reference: {adapter_implementation}")
                adapter_skill = implementations[adapter_implementation].get("skill")
                if adapter_skill not in capability.get("skills", []):
                    raise ValueError(
                        f"Capability/adapter linkage is not symmetric: "
                        f"{capability['id']} -> {adapter_id}"
                    )

        for implementation in implementations.values():
            skill_id = implementation.get("skill")
            if skill_id not in skills:
                raise ValueError(f"Dangling implementation skill reference: {skill_id}")
            if implementation["id"] not in skills[skill_id].get("implementations", []):
                raise ValueError(
                    f"Implementation/skill linkage is not symmetric: {implementation['id']} -> {skill_id}"
                )
            for evidence_id in implementation.get("evidence", []):
                if evidence_id not in evidence:
                    raise ValueError(f"Dangling implementation evidence reference: {evidence_id}")

        valid_compatibility_subject_types = {"skills", "implementations", "adapters"}
        valid_compatibility_target_types = {"platform", "framework", "model", "protocol", "runtime"}
        compatibility_target_collections = {
            "platform": "platforms",
            "framework": "frameworks",
            "model": "models",
            "protocol": "protocols",
            "runtime": "runtimes",
        }
        for compatibility in compatibilities.values():
            subject_id = compatibility.get("subject")
            if subject_id not in ids:
                raise ValueError(f"Dangling compatibility subject reference: {subject_id}")
            subject_type = next((kind for kind, records in entities.items() if any(x["id"] == subject_id for x in records)), None)
            if subject_type not in valid_compatibility_subject_types:
                raise ValueError(f"Invalid compatibility subject type: {subject_type}")
            target = compatibility.get("target", {})
            target_type = target.get("type")
            target_id = target.get("id")
            if target_type not in valid_compatibility_target_types:
                raise ValueError(f"Invalid compatibility target type: {target_type}")
            if target_id not in {x["id"] for x in entities.get(compatibility_target_collections[target_type], [])}:
                raise ValueError(f"Dangling compatibility target reference: {target_type}/{target_id}")
            if compatibility.get("status") not in {"compatible", "conditional", "incompatible", "unknown", "deprecated"}:
                raise ValueError(f"Invalid compatibility status: {compatibility.get('status')}")
            for evidence_id in compatibility.get("evidence", []):
                if evidence_id not in evidence:
                    raise ValueError(f"Dangling compatibility evidence reference: {evidence_id}")
                if compatibility["id"] not in evidence[evidence_id].get("supports", []):
                    raise ValueError(
                        f"Compatibility evidence does not support compatibility {compatibility['id']}: {evidence_id}"
                    )
        for evidence_item in evidence.values():
            for supported_id in evidence_item.get("supports", []):
                if supported_id not in ids:
                    raise ValueError(f"Dangling evidence support reference: {supported_id}")

        valid_target_types = {"platform", "framework", "model", "protocol", "runtime"}
        target_collections = {
            "platform": "platforms",
            "framework": "frameworks",
            "model": "models",
            "protocol": "protocols",
            "runtime": "runtimes",
        }
        for adapter in adapters.values():
            implementation_id = adapter.get("implementation")
            if implementation_id not in implementations:
                raise ValueError(f"Dangling adapter implementation reference: {implementation_id}")
            for target in adapter.get("targets", []):
                target_type = target.get("type")
                target_id = target.get("id")
                if target_type not in valid_target_types:
                    raise ValueError(f"Invalid adapter target type: {target_type}")
                collection = target_collections[target_type]
                if target_id not in {x["id"] for x in entities.get(collection, [])}:
                    raise ValueError(f"Dangling adapter target reference: {target_type}/{target_id}")
            for evidence_id in adapter.get("evidence", []):
                if evidence_id not in evidence:
                    raise ValueError(f"Dangling adapter evidence reference: {evidence_id}")
