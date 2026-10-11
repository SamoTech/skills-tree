#!/usr/bin/env python3
"""Run the CAP-007 human-labeled retrieval benchmark against the canonical search runtime.

Fail-closed: the dataset must pass validation first; an invalid, unlabeled, or
missing dataset returns NOT_RUN, never PASS. Thresholds are quoted from the
CAP-007 mapping in intelligence/ontology/evaluation_ontology.json and are not
redefined here.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from cli.search_engine import search_documents
from validate_cap007_dataset import DEFAULT_SCHEMA, sha256, validate_dataset

QUERY_TYPES = ("exact_match", "paraphrase", "multi_hop", "no_relevant_document")
BENCHMARK_ID = "cap007-retrieval-human-v1"
PASS_CRITERIA = "Recall@5 >= 0.85 AND Precision@5 >= 0.75 AND p95 retrieval latency <= 5000ms"
FAIL_CRITERIA = "Recall@5 < 0.80 OR Precision@5 < 0.70 OR retrieval p95 latency > 5000ms"


def percentile_nearest_rank(sorted_values: list[float], pct: float) -> float:
    if not sorted_values:
        return 0.0
    rank = max(1, math.ceil(pct / 100 * len(sorted_values)))
    return float(sorted_values[rank - 1])


def compute_metrics(cases: list[dict], per_case: dict) -> dict:
    """Micro-averaged set-based Recall@5 / Precision@5 with per-query-type breakdown.

    per_case maps case_id -> (top5_ids, latency_ms).
    Recall@5 = total top-5 hits / total expected skills (relevant cases only).
    Precision@5 = total top-5 hits / total predicted IDs (five per case,
    including no_relevant_document cases, which can only add false positives).
    """
    total_expected = 0
    total_hits = 0
    total_predicted = 0
    per_type = {qt: {"cases": 0, "expected": 0, "hits": 0, "predicted": 0} for qt in QUERY_TYPES}
    rows: list[dict] = []

    for case in cases:
        top5, latency_ms = per_case[case["case_id"]]
        expected = list(case["expected_skill_ids"])
        hits = [skill_id for skill_id in top5 if skill_id in expected]
        total_expected += len(expected)
        total_hits += len(hits)
        total_predicted += len(top5)
        bucket = per_type[case["query_type"]]
        bucket["cases"] += 1
        bucket["expected"] += len(expected)
        bucket["hits"] += len(hits)
        bucket["predicted"] += len(top5)
        rows.append({
            "case_id": case["case_id"],
            "query_type": case["query_type"],
            "expected_skill_ids": expected,
            "top5": list(top5),
            "hits": hits,
            "latency_ms": round(latency_ms, 3),
        })

    recall_at_5 = total_hits / total_expected if total_expected else 0.0
    precision_at_5 = total_hits / total_predicted if total_predicted else 0.0
    latencies = sorted(ms for _, ms in per_case.values())

    return {
        "cases": len(cases),
        "recall_at_5": round(recall_at_5, 4),
        "precision_at_5": round(precision_at_5, 4),
        "latency_ms": {
            "p50": round(percentile_nearest_rank(latencies, 50), 3),
            "p95": round(percentile_nearest_rank(latencies, 95), 3),
        },
        "query_type_breakdown": {
            qt: {
                "cases": bucket["cases"],
                "recall_at_5": round(bucket["hits"] / bucket["expected"], 4) if bucket["expected"] else None,
                "precision_at_5": round(bucket["hits"] / bucket["predicted"], 4) if bucket["predicted"] else None,
            }
            for qt, bucket in per_type.items()
        },
        "cases_detail": rows,
    }


def decide_status(recall_at_5: float, precision_at_5: float, p95_ms: float, deterministic_replay: bool) -> str:
    if not deterministic_replay:
        return "OBSERVED_FAILURE"
    if recall_at_5 >= 0.85 and precision_at_5 >= 0.75 and p95_ms <= 5000:
        return "PASS"
    if recall_at_5 < 0.80 or precision_at_5 < 0.70 or p95_ms > 5000:
        return "OBSERVED_FAILURE"
    return "NEEDS_INVESTIGATION"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", required=True)
    parser.add_argument("--index", default="data/search-index.json")
    parser.add_argument("--schema", default=str(DEFAULT_SCHEMA))
    parser.add_argument("--skills-root", default="skills/")
    parser.add_argument("--output", default="cap007-result.json")
    args = parser.parse_args(argv)

    dataset_path = Path(args.dataset)
    index_path = Path(args.index)
    dataset = json.loads(dataset_path.read_text(encoding="utf-8"))
    schema = json.loads(Path(args.schema).read_text(encoding="utf-8"))

    validation = validate_dataset(dataset, schema, Path(args.skills_root))
    if validation["status"] != "VALID":
        result = {
            "schema_version": "1.0",
            "benchmark_id": BENCHMARK_ID,
            "status": "NOT_RUN",
            "recorded_at": datetime.now(timezone.utc).isoformat(),
            "repository_commit": os.environ.get("GITHUB_SHA", "local"),
            "validation": validation,
            "interpretation": "The dataset failed validation; no empirical CAP-007 result is claimed.",
        }
        Path(args.output).write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 1

    documents = json.loads(index_path.read_text(encoding="utf-8"))
    per_case: dict[str, tuple] = {}
    for case in dataset["cases"]:
        started = time.perf_counter()
        results = search_documents(case["query"], documents, limit=5)
        elapsed_ms = (time.perf_counter() - started) * 1000.0
        per_case[case["case_id"]] = ([item["id"] for item in results], elapsed_ms)

    deterministic_replay = True
    for case in dataset["cases"]:
        first = per_case[case["case_id"]][0]
        second = [item["id"] for item in search_documents(case["query"], documents, limit=5)]
        if first != second:
            deterministic_replay = False
            break

    metrics = compute_metrics(dataset["cases"], per_case)
    status = decide_status(
        metrics["recall_at_5"],
        metrics["precision_at_5"],
        metrics["latency_ms"]["p95"],
        deterministic_replay,
    )

    result = {
        "schema_version": "1.0",
        "benchmark_id": BENCHMARK_ID,
        "status": status,
        "recorded_at": datetime.now(timezone.utc).isoformat(),
        "repository_commit": os.environ.get("GITHUB_SHA", "local"),
        "dataset_sha256": sha256(dataset_path),
        "search_index_sha256": sha256(index_path),
        "pass_criteria": PASS_CRITERIA,
        "fail_criteria": FAIL_CRITERIA,
        "threshold_source": "intelligence/ontology/evaluation_ontology.json CAP-007 mapping",
        "metrics": metrics,
        "deterministic_replay": deterministic_replay,
        "interpretation": (
            "One observed empirical run of the CAP-007 contract against the canonical deterministic "
            "lexical retrieval engine. Recall@5 and Precision@5 are micro-averaged over labeled "
            "expected-skill sets; no_relevant_document cases contribute only to precision. Latency is "
            "wall-clock and environment-dependent; record the measurement environment with the result. "
            "This run is not a popularity, adoption, or user-satisfaction claim."
        ),
    }
    Path(args.output).write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
