"""Deterministic capability-based skill selection runtime."""

from __future__ import annotations

from typing import Any

from registry.eligibility import EligibilityEngine
from registry.runtime import UniversalRegistry


class SkillSelectionEngine:
    """Select an executable canonical skill from explicit capability requirements."""

    def __init__(self, registry: UniversalRegistry, graph: Any | None = None) -> None:
        self.registry = registry
        self.graph = graph
        self.eligibility = EligibilityEngine(registry)

    def select(
        self,
        task: str,
        required_capabilities: list[str],
        candidates: list[str],
        completed_skills: list[str] | None = None,
        target: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        completed = set(completed_skills or [])
        required = set(required_capabilities)
        registered = {item["id"]: item for item in self.registry.data["entities"].get("skills", [])}

        unknown = sorted(set(candidates) - set(registered))
        if unknown:
            return {
                "status": "BLOCKED",
                "selected_skill": None,
                "required_prerequisites": [],
                "rejected_candidates": [{"id": x, "reasons": ["not_registered"]} for x in unknown],
                "next_action": {"type": "escalate", "reason": "unknown_candidate"},
                "evidence_requirements": ["canonical_registry_membership"],
                "task": task,
            }

        eligibility = self.eligibility.evaluate(sorted(set(candidates)), target=target)
        eligible = {x["id"] for x in eligibility["candidates"] if x["status"] == "eligible"}

        scored: list[dict[str, Any]] = []
        rejected: list[dict[str, Any]] = []
        for skill_id in sorted(set(candidates)):
            skill = registered[skill_id]
            capabilities = set(skill.get("capabilities", []))
            covered = sorted(required & capabilities)
            missing = sorted(required - capabilities)
            evidence_count = len(self.registry.evidence_for_entity(skill_id))
            freshness_score = 1 if self.registry.freshness_for_entity(skill_id) else 0

            if skill_id not in eligible:
                reasons = [
                    reason["code"]
                    for item in eligibility["candidates"]
                    if item["id"] == skill_id
                    for reason in item.get("reasons", [])
                ] or ["ineligible"]
                rejected.append({"id": skill_id, "reasons": sorted(set(reasons))})
                continue

            scored.append({
                "id": skill_id,
                "coverage": len(covered),
                "missing": missing,
                "evidence_count": evidence_count,
                "freshness_score": freshness_score,
                "canonical": bool(skill.get("canonical")),
            })

        scored.sort(
            key=lambda item: (
                -item["coverage"],
                bool(item["missing"]),
                -item["evidence_count"],
                -item["freshness_score"],
                not item["canonical"],
                item["id"],
            )
        )

        for item in scored[1:]:
            rejected.append({"id": item["id"], "reasons": ["lower_task_fit_than_selected"]})

        if not scored or scored[0]["coverage"] < len(required):
            rejected.extend(
                {"id": item["id"], "reasons": ["insufficient_capability_coverage"]}
                for item in scored[:1]
            )
            return {
                "status": "BLOCKED",
                "selected_skill": None,
                "required_prerequisites": [],
                "rejected_candidates": self._dedupe_rejections(rejected),
                "next_action": {"type": "escalate", "reason": "no_sufficient_skill"},
                "evidence_requirements": ["capability_coverage"],
                "task": task,
            }

        selected_id = scored[0]["id"]
        try:
            prerequisites = self._prerequisites(selected_id)
        except (KeyError, ValueError) as exc:
            return {
                "status": "BLOCKED",
                "selected_skill": None,
                "required_prerequisites": [],
                "rejected_candidates": self._dedupe_rejections(rejected),
                "next_action": {"type": "escalate", "reason": "invalid_prerequisite_graph"},
                "evidence_requirements": ["canonical_registry_membership", "dependency_graph_integrity"],
                "task": task,
                "dependency_error": str(exc),
            }
        pending = [item for item in prerequisites if item not in completed]

        if pending:
            return {
                "status": "CONTINUE",
                "selected_skill": {"id": selected_id, "version": registered[selected_id]["version"]},
                "required_prerequisites": pending,
                "rejected_candidates": self._dedupe_rejections(rejected),
                "next_action": {"type": "invoke_prerequisite", "skill_id": pending[0]},
                "evidence_requirements": ["prerequisite_success", "skill_invocation_outcome"],
                "task": task,
            }

        return {
            "status": "CONTINUE",
            "selected_skill": {"id": selected_id, "version": registered[selected_id]["version"]},
            "required_prerequisites": prerequisites,
            "rejected_candidates": self._dedupe_rejections(rejected),
            "next_action": {"type": "invoke", "skill_id": selected_id},
            "evidence_requirements": ["skill_invocation_outcome", "task_acceptance_criteria"],
            "task": task,
        }

    def next_after_failure(
        self,
        task: str,
        required_capabilities: list[str],
        candidates: list[str],
        failed_skill: str,
        completed_skills: list[str] | None = None,
    ) -> dict[str, Any]:
        alternatives = [item for item in candidates if item != failed_skill]
        if not alternatives:
            return {
                "status": "BLOCKED",
                "selected_skill": None,
                "required_prerequisites": [],
                "rejected_candidates": [{"id": failed_skill, "reasons": ["invocation_failed"]}],
                "next_action": {"type": "escalate", "reason": "no_recovery_candidate"},
                "evidence_requirements": ["failure_evidence"],
                "task": task,
            }
        result = self.select(task, required_capabilities, alternatives, completed_skills=completed_skills)
        result["failure_recovery"] = {"failed_skill": failed_skill, "reason": "invocation_failed"}
        return result

    def _prerequisites(self, skill_id: str) -> list[str]:
        """Return a deterministic transitive prerequisite execution plan."""
        if self.graph is None:
            return []

        registered = {
            item["id"]
            for item in self.registry.data["entities"].get("skills", [])
        }
        visiting: set[str] = set()
        visited: set[str] = set()
        ordered: list[str] = []

        def visit(node_id: str) -> None:
            if node_id in visited:
                return
            if node_id in visiting:
                raise ValueError(f"Prerequisite cycle detected: {node_id}")
            visiting.add(node_id)
            dependencies = sorted(
                item["id"]
                for item in self.graph.get_dependencies(node_id, "REQUIRES")
            )
            for dependency in dependencies:
                if dependency not in registered:
                    raise KeyError(f"Unregistered prerequisite: {node_id} -> {dependency}")
                visit(dependency)
                if dependency not in ordered:
                    ordered.append(dependency)
            visiting.remove(node_id)
            visited.add(node_id)

        visit(skill_id)
        return ordered

    @staticmethod
    def _dedupe_rejections(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
        merged: dict[str, set[str]] = {}
        for item in items:
            merged.setdefault(item["id"], set()).update(item["reasons"])
        return [{"id": x, "reasons": sorted(y)} for x, y in sorted(merged.items())]
