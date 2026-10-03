"""Universal-registry eligibility integration for the legacy recommender."""

from __future__ import annotations

from typing import Any

from registry.eligibility import EligibilityEngine
from registry.runtime import UniversalRegistry
from tools.architect import RecommendationEngine


class RegistryRecommendationEngine(RecommendationEngine):
    """Run registry eligibility before the existing ranking pipeline.

    The legacy recommendation algorithm remains authoritative for discovery,
    scoring, calibration inputs, and learning-path construction. Registry
    eligibility is an additive pre-ranking gate for candidates that are already
    represented in the universal registry. Unregistered legacy skills are left
    untouched so the existing corpus behavior is preserved.
    """

    def __init__(
        self,
        graph: Any,
        taxonomy: Any,
        benchmark_index_path: str | None = None,
        registry: UniversalRegistry | None = None,
    ) -> None:
        super().__init__(graph, taxonomy, benchmark_index_path)
        self.registry = registry
        self.eligibility = EligibilityEngine(registry) if registry is not None else None

    def recommend(
        self,
        goal_query: str,
        target: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        result = super().recommend(goal_query)
        if "error" in result or self.eligibility is None:
            return result

        registered_skills = self._registered_skill_ids()
        candidate_skills = [
            normalized_id
            for skill in result.get("required_skills", []) + result.get("optional_skills", [])
            for normalized_id in [self._normalize_skill_id(skill.get("id"))]
            if normalized_id is not None and normalized_id in registered_skills
        ]
        candidate_ids, candidate_to_skills = self._eligibility_candidates(candidate_skills, target)
        eligibility = self.eligibility.evaluate(candidate_ids, target=target)
        result["eligibility"] = eligibility

        ineligible_candidates = {
            item["id"]
            for item in eligibility["candidates"]
            if item["status"] == "ineligible"
        }
        ineligible_registry_skills = {
            skill_id
            for candidate_id in ineligible_candidates
            for skill_id in candidate_to_skills.get(candidate_id, {candidate_id})
            if all(
                candidate_status == "ineligible"
                for related_id in self._skill_candidates(skill_id, target)
                for candidate_status in self._candidate_statuses(related_id, eligibility)
            )
        }
        ineligible_skills = {
            skill["id"]
            for skill in result.get("required_skills", []) + result.get("optional_skills", [])
            if self._normalize_skill_id(skill.get("id")) in ineligible_registry_skills
        }
        if not ineligible_skills:
            return result

        result["required_skills"] = [
            skill for skill in result.get("required_skills", []) if skill["id"] not in ineligible_skills
        ]
        result["optional_skills"] = [
            skill for skill in result.get("optional_skills", []) if skill["id"] not in ineligible_skills
        ]

        # Preserve the legacy score ordering while making ranks contiguous after
        # an eligibility gate removes a candidate.
        for rank, skill in enumerate(result["required_skills"], start=1):
            skill["rank"] = rank
        for rank, skill in enumerate(result["optional_skills"], start=len(result["required_skills"]) + 1):
            skill["rank"] = rank
        return result

    def consumption_context_for_skill(self, skill_id: str) -> dict[str, Any] | None:
        """Return deterministic registry context for a recommended canonical skill."""
        if self.registry is None:
            return None
        normalized_id = self._normalize_skill_id(skill_id)
        if normalized_id is None:
            return None
        skill = self.registry.resolve_skill(normalized_id)
        evidence = self.registry.evidence_for_entity(normalized_id)
        implementations = self.registry.implementations_for_skill(normalized_id)
        implementation_evidence = {
            item["id"]: [
                {"id": evidence["id"], "type": evidence["type"], "source": evidence["source"]}
                for evidence in self.registry.evidence_for_entity(item["id"])
            ]
            for item in implementations
        }
        freshness = self.registry.freshness_for_entity(normalized_id)
        return {
            "canonical_id": normalized_id,
            "version": skill["version"],
            "canonical": skill["canonical"],
            "provenance": skill["provenance"],
            "evidence": [
                {"id": item["id"], "type": item["type"], "source": item["source"]}
                for item in evidence
            ],
            "freshness": freshness,
            "implementation_ids": [item["id"] for item in implementations],
            "implementation_evidence": implementation_evidence,
        }

    def _eligibility_candidates(
        self, skill_ids: list[str], target: dict[str, str] | None
    ) -> tuple[list[str], dict[str, set[str]]]:
        """Resolve target-aware compatibility through registered adapters."""
        if target is None:
            return skill_ids, {skill_id: {skill_id} for skill_id in skill_ids}

        entities = self.registry.data["entities"]
        adapters = entities.get("adapters", [])
        skills = {item["id"]: item for item in entities.get("skills", [])}

        candidate_ids: list[str] = []
        candidate_to_skills: dict[str, set[str]] = {}
        for skill_id in skill_ids:
            skill = skills[skill_id]
            implementation_ids = set(skill.get("implementations", []))
            adapter_ids = {
                adapter["id"]
                for adapter in adapters
                if adapter.get("implementation") in implementation_ids
            }
            if not adapter_ids:
                candidate_ids.append(skill_id)
                candidate_to_skills.setdefault(skill_id, set()).add(skill_id)
                continue
            for adapter_id in sorted(adapter_ids):
                candidate_ids.append(adapter_id)
                candidate_to_skills.setdefault(adapter_id, set()).add(skill_id)

        return sorted(set(candidate_ids)), candidate_to_skills

    def _skill_candidates(self, skill_id: str, target: dict[str, str] | None) -> list[str]:
        candidates, mapping = self._eligibility_candidates([skill_id], target)
        return [candidate_id for candidate_id in candidates if skill_id in mapping.get(candidate_id, set())]

    @staticmethod
    def _candidate_statuses(candidate_id: str, eligibility: dict[str, Any]) -> list[str]:
        return [
            item["status"]
            for item in eligibility.get("candidates", [])
            if item["id"] == candidate_id
        ]

    def _normalize_skill_id(self, skill_id: str | None) -> str | None:
        """Map legacy taxonomy skill IDs to unique canonical registry IDs."""
        if skill_id is None:
            return None
        registered = self._registered_skill_ids()
        if skill_id in registered:
            return skill_id
        matches = sorted(candidate for candidate in registered if candidate.rsplit("/", 1)[-1] == skill_id)
        if len(matches) == 1:
            return matches[0]
        return None

    def _registered_skill_ids(self) -> set[str]:
        return {skill["id"] for skill in self.registry.data["entities"].get("skills", [])}
