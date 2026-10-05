#!/usr/bin/env python3
"""Run the versioned retrieval benchmark against the canonical CLI search runtime."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path

from cli.search_engine import search_documents


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", default="benchmarks/retrieval/cli-search-v1.json")
    parser.add_argument("--index", default="data/search-index.json")
    parser.add_argument("--output", default="retrieval-benchmark-result.json")
    args = parser.parse_args()

    dataset_path = Path(args.dataset)
    index_path = Path(args.index)
    dataset = json.loads(dataset_path.read_text(encoding="utf-8"))
    documents = json.loads(index_path.read_text(encoding="utf-8"))

    cases = dataset["cases"]
    rows = []
    ranks = []
    top5_hits = 0

    for case in cases:
        results = search_documents(case["query"], documents, limit=5)
        ranked_ids = [item["id"] for item in results]
        target = case["expected_skill_id"]
        rank = ranked_ids.index(target) + 1 if target in ranked_ids else None
        if rank is not None:
            top5_hits += 1
            ranks.append(rank)
        rows.append({
            "id": case["id"],
            "query": case["query"],
            "expected_skill_id": target,
            "rank": rank,
            "top5": ranked_ids,
        })

    n = len(cases)
    recall_at_5 = top5_hits / n if n else 0.0
    mrr = sum((1.0 / row["rank"]) if row["rank"] else 0.0 for row in rows) / n if n else 0.0
    deterministic_replay = True

    # Replay each query and require identical ranked IDs.
    for case in cases:
        first = [x["id"] for x in search_documents(case["query"], documents, limit=5)]
        second = [x["id"] for x in search_documents(case["query"], documents, limit=5)]
        if first != second:
            deterministic_replay = False
            break

    result = {
        "schema_version": "1.0",
        "benchmark_id": dataset["benchmark_id"],
        "benchmark_version": dataset["benchmark_version"],
        "status": "PASS" if recall_at_5 >= 0.90 and mrr >= 0.80 and deterministic_replay else "OBSERVED_FAILURE",
        "recorded_at": datetime.now(timezone.utc).isoformat(),
        "repository_commit": os.environ.get("GITHUB_SHA", "local"),
        "search_index_sha256": sha256(index_path),
        "dataset_sha256": sha256(dataset_path),
        "metrics": {
            "cases": n,
            "recall_at_5": round(recall_at_5, 4),
            "mrr": round(mrr, 4),
            "deterministic_replay": deterministic_replay,
        },
        "cases": rows,
        "interpretation": "This is a deterministic retrieval evidence snapshot for the canonical CLI search contract. It is not a semantic-search, popularity, adoption, or user-satisfaction benchmark.",
    }
    Path(args.output).write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
