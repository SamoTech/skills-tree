#!/usr/bin/env python3
"""Validate a CAP-007 human-labeled retrieval dataset.

Fail-closed: a dataset is VALID only when it satisfies the versioned schema,
resolves every expected skill to a canonical file, has unique case IDs, and
covers all four query types. Anything else is INVALID and cannot be used for
an empirical CAP-007 run.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

DEFAULT_SCHEMA = Path("benchmarks/retrieval/cap007-dataset.schema.json")
QUERY_TYPES = ("exact_match", "paraphrase", "multi_hop", "no_relevant_document")
MAX_REPORTED_ERRORS = 50


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_dataset(dataset: dict, schema: dict, skills_root: Path) -> dict:
    errors: list[str] = []
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    for err in validator.iter_errors(dataset):
        location = "/".join(str(part) for part in err.absolute_path) or "root"
        errors.append(f"schema: {location}: {err.message}")

    cases = dataset.get("cases", []) if isinstance(dataset, dict) else []

    seen: set[str] = set()
    duplicates: set[str] = set()
    missing_skills: list[str] = []
    query_type_counts: dict[str, int] = {}
    labelers: set[str] = set()

    for case in cases:
        if not isinstance(case, dict):
            continue
        case_id = case.get("case_id")
        if case_id in seen:
            duplicates.add(str(case_id))
        seen.add(str(case_id))

        query_type = case.get("query_type")
        if isinstance(query_type, str):
            query_type_counts[query_type] = query_type_counts.get(query_type, 0) + 1

        labeling = case.get("labeling")
        if isinstance(labeling, dict) and isinstance(labeling.get("labeler_id"), str):
            labelers.add(labeling["labeler_id"])

        expected = case.get("expected_skill_ids") or []
        for skill_id in expected:
            if not (skills_root / f"{skill_id}.md").is_file():
                missing_skills.append(f"{case_id}: {skill_id}")

    if duplicates:
        errors.append("duplicate case ids: " + ", ".join(sorted(duplicates)))
    for ref in missing_skills:
        errors.append(f"unresolved canonical skill: {ref}")
    for query_type in QUERY_TYPES:
        if query_type_counts.get(query_type, 0) == 0:
            errors.append(f"query_type coverage missing: {query_type}")

    errors = errors[:MAX_REPORTED_ERRORS]
    return {
        "schema_version": "1.0",
        "tool": "validate_cap007_dataset",
        "status": "VALID" if not errors else "INVALID",
        "cases": len(cases),
        "query_type_counts": {qt: query_type_counts.get(qt, 0) for qt in QUERY_TYPES},
        "distinct_labelers": len(labelers),
        "errors": errors,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", required=True)
    parser.add_argument("--schema", default=str(DEFAULT_SCHEMA))
    parser.add_argument("--skills-root", default="skills/")
    parser.add_argument("--output")
    args = parser.parse_args(argv)

    dataset_path = Path(args.dataset)
    dataset = json.loads(dataset_path.read_text(encoding="utf-8"))
    schema = json.loads(Path(args.schema).read_text(encoding="utf-8"))
    skills_root = Path(args.skills_root)

    report = validate_dataset(dataset, schema, skills_root)
    report["dataset_sha256"] = sha256(dataset_path)

    rendered = json.dumps(report, indent=2, ensure_ascii=False)
    print(rendered)
    if args.output:
        Path(args.output).write_text(rendered + "\n", encoding="utf-8")
    return 0 if report["status"] == "VALID" else 1


if __name__ == "__main__":
    raise SystemExit(main())
