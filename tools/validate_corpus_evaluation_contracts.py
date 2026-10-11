#!/usr/bin/env python3
"""Validate generic capability evaluation mappings and scenario-specific corpus contracts.

A corpus requirement is scoped to one agent scenario. Its method and threshold
may differ from the generic capability baseline when they test a distinct
domain outcome; equality is deliberately not enforced. Referential integrity,
metric IDs, threshold types, and capability identity are enforced.
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CAPABILITY_PATH = ROOT / "intelligence" / "ontology" / "capability_ontology.json"
EVALUATION_PATH = ROOT / "intelligence" / "ontology" / "evaluation_ontology.json"
CORPUS_DIR = ROOT / "intelligence" / "corpus" / "entries"


def _index_unique(items: list[dict[str, Any]], key: str, label: str, errors: list[str]) -> dict[str, dict[str, Any]]:
    indexed: dict[str, dict[str, Any]] = {}
    for item in items:
        value = item.get(key)
        if not isinstance(value, str) or not value.strip():
            errors.append(f"{label}: missing {key}")
            continue
        if value in indexed:
            errors.append(f"{label}: duplicate {key} {value}")
            continue
        indexed[value] = item
    return indexed


def validate_contracts(
    capability_ontology: dict[str, Any],
    evaluation_ontology: dict[str, Any],
    corpus_entries: list[dict[str, Any]],
) -> list[str]:
    """Return contract integrity errors; an empty list means structurally valid."""
    errors: list[str] = []
    capabilities = _index_unique(
        capability_ontology.get("capabilities", []), "cap_id", "capability ontology", errors
    )
    mappings = _index_unique(
        evaluation_ontology.get("capability_evaluation_mappings", []),
        "cap_id",
        "evaluation ontology",
        errors,
    )
    metric_types = _index_unique(
        evaluation_ontology.get("evaluation_types", []),
        "evaluation_id",
        "evaluation types",
        errors,
    )

    for cap_id, mapping in mappings.items():
        canonical = capabilities.get(cap_id)
        if canonical is None:
            errors.append(f"[{cap_id}] evaluation mapping references unknown capability")
            continue
        if mapping.get("name") != canonical.get("name"):
            errors.append(
                f"[{cap_id}] evaluation mapping name {mapping.get('name')!r} "
                f"does not match canonical name {canonical.get('name')!r}"
            )
        if not str(mapping.get("validation_method", "")).strip():
            errors.append(f"[{cap_id}] generic evaluation mapping has no validation_method")
        threshold = mapping.get("minimum_required_score")
        if isinstance(threshold, bool) or not isinstance(threshold, (int, float)) or not math.isfinite(threshold) or not 0 <= threshold <= 1:
            errors.append(f"[{cap_id}] minimum_required_score must be a finite number in [0, 1]")
        metrics = mapping.get("primary_metrics", []) + mapping.get("secondary_metrics", [])
        if not mapping.get("primary_metrics"):
            errors.append(f"[{cap_id}] generic evaluation mapping has no primary_metrics")
        for metric_id in metrics:
            if metric_id not in metric_types:
                errors.append(f"[{cap_id}] references unknown evaluation metric {metric_id!r}")

    for corpus in corpus_entries:
        entry_id = corpus.get("entry_id", "<unknown-entry>")
        required = {
            cap.get("cap_id"): cap
            for cap in corpus.get("required_capabilities", [])
            if isinstance(cap, dict) and isinstance(cap.get("cap_id"), str)
        }
        requirements = corpus.get("evaluation_requirements", [])
        if not isinstance(requirements, list) or not requirements:
            errors.append(f"[{entry_id}] evaluation_requirements must be a non-empty list")
            continue
        for index, requirement in enumerate(requirements):
            label = f"[{entry_id}] evaluation_requirements[{index}]"
            if not isinstance(requirement, dict):
                errors.append(f"{label} must be an object")
                continue
            cap_id = requirement.get("capability")
            if not isinstance(cap_id, str) or not cap_id.strip():
                errors.append(f"{label} missing capability reference")
                continue
            if cap_id not in required:
                errors.append(f"{label} references {cap_id}, which is not in required_capabilities")
            if cap_id not in capabilities:
                errors.append(f"{label} references unknown canonical capability {cap_id}")
            if cap_id not in mappings:
                errors.append(f"{label} has no generic evaluation mapping for {cap_id}")
            method = requirement.get("eval_method")
            if not isinstance(method, str) or not method.strip():
                errors.append(f"{label} missing eval_method")
            threshold = requirement.get("pass_threshold")
            if isinstance(threshold, bool) or not isinstance(threshold, (int, float)) or not math.isfinite(threshold) or not 0 <= threshold <= 1:
                errors.append(f"{label} pass_threshold must be a finite number in [0, 1]")
            priority = requirement.get("priority")
            if priority not in {"required", "recommended"}:
                errors.append(f"{label} priority must be 'required' or 'recommended'")
            scope = requirement.get("contract_scope")
            if scope not in {"scenario_specific", "generic_baseline"}:
                errors.append(f"{label} contract_scope must be 'scenario_specific' or 'generic_baseline'")
            elif scope == "generic_baseline" and cap_id in mappings:
                mapping = mappings[cap_id]
                if method != mapping.get("validation_method"):
                    errors.append(f"{label} generic_baseline eval_method must match the capability mapping")
                baseline = mapping.get("minimum_required_score")
                if isinstance(threshold, (int, float)) and not isinstance(threshold, bool) and isinstance(baseline, (int, float)) and threshold < baseline:
                    errors.append(f"{label} generic_baseline pass_threshold must meet the capability mapping minimum")

    return errors


def main() -> int:
    capability_ontology = json.loads(CAPABILITY_PATH.read_text(encoding="utf-8"))
    evaluation_ontology = json.loads(EVALUATION_PATH.read_text(encoding="utf-8"))
    corpus_entries = [
        json.loads(path.read_text(encoding="utf-8"))
        for path in sorted(CORPUS_DIR.rglob("*.json"))
    ]
    errors = validate_contracts(capability_ontology, evaluation_ontology, corpus_entries)
    if errors:
        print(f"FAILED: {len(errors)} evaluation contract integrity error(s)")
        for error in errors:
            print(f"  ERROR: {error}")
        return 1
    print(
        "PASSED: generic capability mappings, metric IDs, and "
        f"{sum(len(entry.get('evaluation_requirements', [])) for entry in corpus_entries)} "
        "scenario-specific corpus requirements are structurally aligned."
    )
    print(
        "Scenario-specific methods and thresholds are intentionally not required "
        "to equal generic capability baselines."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
