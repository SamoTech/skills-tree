#!/usr/bin/env python3
"""Build and validate the deterministic Agent Skills discovery index.

Canonical source: skills/
Projection source: reconciled agent-skills/ packages
Output: a discovery index plus SHA-256 digests of the exact published SKILL.md bytes.

This tool never generates or mutates agent-skills/. Reconciliation and the
canonical projection generator remain responsible for that boundary.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from urllib.parse import urlparse

from jsonschema import Draft202012Validator

from tools.reconcile_agent_skills import (
    NAME_RE,
    canonical_records,
    desired_names,
    project,
    reconcile,
    reconciliation_failures,
)

SCHEMA_PATH = Path(__file__).resolve().parents[1] / "meta" / "agent-skills-discovery-index.schema.json"
SCHEMA_URL = "https://raw.githubusercontent.com/SamoTech/skills-tree/main/meta/agent-skills-discovery-index.schema.json"
DEFAULT_BASE_URL = "https://samotech.github.io/skills-tree"
DIGEST_RE = re.compile(r"^sha256:[0-9a-f]{64}$")


def artifact_digest(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def validate_index(index: dict) -> None:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    errors = sorted(Draft202012Validator(schema).iter_errors(index), key=lambda e: list(e.path))
    if errors:
        raise ValueError("; ".join(error.message for error in errors))

    names = [item["name"] for item in index["skills"]]
    if len(names) != len(set(names)):
        raise ValueError("discovery index contains duplicate skill names")
    if names != sorted(names):
        raise ValueError("skills must be sorted by name")

    for item in index["skills"]:
        if not NAME_RE.fullmatch(item["name"]):
            raise ValueError(f"invalid skill name: {item['name']}")
        if not DIGEST_RE.fullmatch(item["digest"]):
            raise ValueError(f"invalid digest: {item['digest']}")
        if not urlparse(item["url"]).scheme:
            raise ValueError(f"skill URL must be absolute: {item['url']}")


def build_index(root: Path, base_url: str = DEFAULT_BASE_URL) -> dict:
    report = reconcile(root)
    failures = reconciliation_failures(report)
    if failures:
        raise ValueError("cannot publish with reconciliation failures: " + ", ".join(failures))

    records = canonical_records(root)
    desired, _ = desired_names(records)
    items = []

    for record in records:
        source = record["source"]
        package = desired[source]
        projection = project(root / source, root, name_override=package)
        if not projection.eligible:
            continue

        artifact = root / "agent-skills" / package / "SKILL.md"
        if not artifact.is_file():
            raise ValueError(f"eligible projection missing: {artifact.relative_to(root)}")

        data = artifact.read_bytes()
        expected = projection.content.rstrip() + "\n"
        if data.decode("utf-8") != expected:
            raise ValueError(f"projection drift: {artifact.relative_to(root)}")

        items.append(
            {
                "name": package,
                "type": "skill",
                "description": projection.description,
                "url": f"{base_url.rstrip('/')}/agent-skills/{package}/SKILL.md",
                "digest": artifact_digest(data),
            }
        )

    index = {"$schema": SCHEMA_URL, "skills": sorted(items, key=lambda item: item["name"])}
    validate_index(index)
    return index


def write_index(index: dict, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(index, indent=2, sort_keys=False) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    root = args.root.resolve()
    index = build_index(root, args.base_url)
    if args.check:
        if not args.output.is_file():
            raise SystemExit(f"missing discovery index: {args.output}")
        actual = json.loads(args.output.read_text(encoding="utf-8"))
        if actual != index:
            raise SystemExit("discovery index is not deterministic or is stale")
        print(f"OK: {len(index['skills'])} skills; discovery index is deterministic and verified")
    else:
        write_index(index, args.output)
        print(f"Wrote {len(index['skills'])} skills to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
