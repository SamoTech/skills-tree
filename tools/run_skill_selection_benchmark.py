#!/usr/bin/env python3
"""Run the deterministic capability-based skill-selection benchmark."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path

from registry.runtime import UniversalRegistry
from registry.skill_selection import SkillSelectionEngine
from tools.architect import SkillsGraph


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", default="benchmarks/selection/capability-selection-v1.json")
    parser.add_argument("--registry", default="registry/universal_registry.json")
    parser.add_argument("--graph", default="data/SKILLS_GRAPH.json")
    parser.add_argument("--output", default="skill-selection-benchmark-result.json")
    args = parser.parse_args()

    dataset_path = Path(args.dataset)
    cases = json.loads(dataset_path.read_text(encoding="utf-8"))["cases"]
    engine = SkillSelectionEngine(UniversalRegistry(args.registry), SkillsGraph(args.graph))

    rows = []
    passed = 0
    for case in cases:
        if "failed_skill" in case:
            observed = engine.next_after_failure(
                case["task"], case["required_capabilities"], case["candidates"],
                case["failed_skill"], case.get("completed_skills"), case.get("failed_skills")
            )
        else:
            observed = engine.select(
                case["task"], case["required_capabilities"], case["candidates"],
                case.get("completed_skills")
            )
        observed_id = observed["selected_skill"]["id"] if observed["selected_skill"] else None
        next_type = observed["next_action"]["type"]
        ok = (
            observed_id == case["expected_selected_skill"]
            and observed["status"] == case["expected_status"]
            and next_type == case["expected_next_action"]
        )
        passed += int(ok)
        rows.append({
            "id": case["id"],
            "pass": ok,
            "expected": {
                "selected_skill": case["expected_selected_skill"],
                "status": case["expected_status"],
                "next_action": case["expected_next_action"],
            },
            "observed": {
                "selected_skill": observed["selected_skill"],
                "status": observed["status"],
                "next_action": observed["next_action"],
            },
        })

    deterministic = True
    for case in cases:
        if "failed_skill" in case:
            first = engine.next_after_failure(
                case["task"], case["required_capabilities"], case["candidates"],
                case["failed_skill"], case.get("completed_skills")
            )
            second = engine.next_after_failure(
                case["task"], case["required_capabilities"], case["candidates"],
                case["failed_skill"], case.get("completed_skills")
            )
        else:
            first = engine.select(
                case["task"], case["required_capabilities"], case["candidates"],
                case.get("completed_skills")
            )
            second = engine.select(
                case["task"], case["required_capabilities"], case["candidates"],
                case.get("completed_skills")
            )
        if first != second:
            deterministic = False
            break

    n = len(cases)
    accuracy = passed / n if n else 0.0
    status = "PASS" if accuracy == 1.0 and deterministic else "OBSERVED_FAILURE"
    result = {
        "schema_version": "1.0",
        "benchmark_id": "benchmark/skill-selection-v1",
        "benchmark_version": "1.0",
        "status": status,
        "recorded_at": datetime.now(timezone.utc).isoformat(),
        "repository_commit": os.environ.get("GITHUB_SHA", "local"),
        "dataset_sha256": sha256(dataset_path),
        "metrics": {
            "cases": n,
            "accuracy": round(accuracy, 4),
            "deterministic_replay": deterministic,
        },
        "cases": rows,
        "interpretation": "Measures deterministic capability-to-skill selection, prerequisite routing, and failure terminal behavior. It does not claim general semantic task understanding or autonomous-agent success.",
    }
    Path(args.output).write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
