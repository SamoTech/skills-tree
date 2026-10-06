#!/usr/bin/env python3
"""Measure skill activation/invocation from externally captured trace observations.

This tool does not simulate an agent, infer activation from prompt text, or claim
that a deterministic fixture is a real model-routing result. Observations must
contain explicit skill selection/execution events emitted by an agent runtime.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import defaultdict
from pathlib import Path


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_observations(path: Path) -> list[dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("schema_version") != "1.0":
        raise ValueError("unsupported observation schema_version")
    runs = data.get("runs")
    if not isinstance(runs, list):
        raise ValueError("observations.runs must be a list")
    return runs


def event_ids(run: dict, kind: str) -> set[str]:
    result = set()
    for event in run.get("events", []):
        if event.get("kind") == kind and event.get("skill_id"):
            result.add(event["skill_id"])
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", default="benchmarks/activation/skill-activation-v1.json")
    parser.add_argument("--observations", required=True)
    parser.add_argument("--output", default="skill-activation-benchmark-result.json")
    args = parser.parse_args()

    dataset_path = Path(args.dataset)
    observations_path = Path(args.observations)
    cases = json.loads(dataset_path.read_text(encoding="utf-8"))["cases"]
    runs = load_observations(observations_path)

    by_case: dict[str, list[dict]] = defaultdict(list)
    for run in runs:
        case_id = run.get("case_id")
        if case_id:
            by_case[case_id].append(run)

    rows = []
    activation_hits = 0
    invocation_hits = 0
    false_activations = 0
    observed_cases = 0
    variance_values = []

    for case in cases:
        case_runs = by_case.get(case["id"], [])
        case_activation = []
        case_invocation = []
        case_false = []
        for run in case_runs:
            selected = event_ids(run, "skill_selection")
            executed = event_ids(run, "skill_execution")
            expected_hit = case["expected_skill"] in selected
            invocation_hit = case["expected_skill"] in executed
            false_hit = bool(selected & set(case["must_not_activate"]))
            case_activation.append(expected_hit)
            case_invocation.append(invocation_hit)
            case_false.append(false_hit)

        observed = len(case_runs)
        if observed:
            observed_cases += 1
            activation_hits += sum(case_activation)
            invocation_hits += sum(case_invocation)
            false_activations += sum(case_false)
            variance_values.append(max(case_activation) - min(case_activation))

        rows.append({
            "id": case["id"],
            "observed_runs": observed,
            "expected_skill": case["expected_skill"],
            "activation_hits": sum(case_activation),
            "invocation_evidence_hits": sum(case_invocation),
            "false_activation_hits": sum(case_false),
            "activation_rate": round(sum(case_activation) / observed, 4) if observed else None,
            "invocation_evidence_rate": round(sum(case_invocation) / observed, 4) if observed else None,
            "activation_variance": (max(case_activation) - min(case_activation)) if observed else None,
            "status": "OBSERVED" if observed else "NO_OBSERVATIONS"
        })

    total_runs = sum(len(v) for v in by_case.values())
    result = {
        "schema_version": "1.0",
        "benchmark_id": "benchmark/skill-activation-v1",
        "benchmark_version": "1.0",
        "status": "OBSERVED" if observed_cases else "NO_OBSERVATIONS",
        "dataset_sha256": sha256(dataset_path),
        "observation_sha256": sha256(observations_path),
        "metrics": {
            "cases": len(cases),
            "observed_cases": observed_cases,
            "runs": total_runs,
            "expected_activation_rate": round(activation_hits / total_runs, 4) if total_runs else None,
            "false_activation_rate": round(false_activations / total_runs, 4) if total_runs else None,
            "invocation_evidence_rate": round(invocation_hits / total_runs, 4) if total_runs else None,
            "max_activation_variance": max(variance_values) if variance_values else None
        },
        "cases_detail": rows,
        "interpretation": "Measures observed routing/activation and explicit invocation evidence from runtime traces. It does not infer activation from prompt text, simulate model behavior, or claim general agent success. NO_OBSERVATIONS is not PASS."
    }
    Path(args.output).write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
