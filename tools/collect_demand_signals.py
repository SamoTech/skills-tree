#!/usr/bin/env python3
"""Collect reproducible public demand signals.

This collector records raw public GitHub issue-search evidence. It does not
rank popularity, infer adoption, or modify MOST-WANTED-SKILLS.md.

Usage:
  python tools/collect_demand_signals.py --output data/demand-signals.json
  python tools/collect_demand_signals.py --check --output data/demand-signals.json
"""
from __future__ import annotations
import argparse
import datetime as dt
import json
import os
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = ROOT / "meta/demand-sources.json"

def _request(url: str) -> list[dict]:
    headers = {"Accept":"application/vnd.github+json","X-GitHub-Api-Version":"2026-03-10","User-Agent":"skills-tree-demand-collector"}
    if token := os.environ.get("GITHUB_TOKEN"):
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)["items"]

def collect(config: dict, observed_at: str) -> dict:
    signals = []
    for source in config.get("sources", []):
        if source.get("type") != "github_issue_search":
            raise ValueError(f"unsupported source type: {source.get('type')}")
        for query in source.get("queries", []):
            url = "https://api.github.com/search/issues?q=" + urllib.parse.quote(query, safe="") + "&per_page=100"
            for item in _request(url):
                if "pull_request" in item:
                    continue
                repo = item.get("repository_url", "").removeprefix("https://api.github.com/repos/")
                signals.append({
                    "source_id": source["id"], "source_type": source["type"],
                    "observed_at": observed_at, "query": query, "repository": repo,
                    "issue_number": item["number"], "title": item["title"],
                    "url": item["html_url"], "state": item["state"],
                    "created_at": item["created_at"], "updated_at": item["updated_at"],
                    "labels": sorted(label["name"] for label in item.get("labels", [])),
                })
    signals.sort(key=lambda x:(x["source_id"],x["query"],x["repository"],x["issue_number"],x["url"]))
    return {
        "schema_version": 1,
        "collected_at": observed_at,
        "method": "public GitHub issue search",
        "privacy": "public repositories/issues only",
        "interpretation": "Raw demand evidence only; issue volume is not adoption or popularity.",
        "signals": signals,
    }

def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--check", action="store_true")
    args = p.parse_args()
    config = json.loads(args.config.read_text(encoding="utf-8"))
    observed_at = dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00","Z")
    data = collect(config, observed_at)
    if args.check:
        if not args.output.is_file():
            raise SystemExit(f"missing demand signal snapshot: {args.output}")
        existing = json.loads(args.output.read_text(encoding="utf-8"))
        if existing.get("schema_version") != 1 or existing.get("method") != data["method"]:
            raise SystemExit("demand signal schema/method mismatch")
        if not isinstance(existing.get("signals"), list):
            raise SystemExit("demand signal snapshot must contain a signals array")
        print(f"OK: {len(existing['signals'])} raw demand signals are structurally valid")
        return 0
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print(f"Collected {len(data['signals'])} raw public demand signals.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
