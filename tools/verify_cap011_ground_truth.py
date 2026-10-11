#!/usr/bin/env python3
"""Fail-closed verifier for the CAP-011 ground-truth dataset.

Re-executes the deterministic predicate of every case from the checked-in
verifier spec and requires the derived outcome to match the dataset's
expected_outcome exactly. Ground truth in this dataset is a property of the
committed files, not of any human or model opinion.

Validating the dataset is NOT evidence that any agent passed CAP-011. The
empirical contract remains NOT RUN until a real candidate system is executed
with retained raw outputs and independent hallucination adjudication.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import date
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATASET = ROOT / "benchmarks" / "self-evaluation" / "cap011-dataset-v1.json"
DEFAULT_SPEC = ROOT / "benchmarks" / "self-evaluation" / "cap011-verifier-v1.json"
DEFAULT_SCHEMA = ROOT / "benchmarks" / "self-evaluation" / "cap011-dataset.schema.json"
REVIEWER_ID = "cap011-verifier-v1 (deterministic predicate re-execution)"

ARITH_OPS = {"add", "sub", "mul", "div"}
STRING_OPS = {"uppercase", "reverse", "star_vowels", "sort_chars"}


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _string_transform(op: str, text: str) -> str:
    if op == "uppercase":
        return text.upper()
    if op == "reverse":
        return text[::-1]
    if op == "star_vowels":
        return "".join("*" if ch in "aeiou" else ch for ch in text)
    if op == "sort_chars":
        return "".join(sorted(text))
    raise ValueError(f"unsupported string transform op: {op}")


def derive_outcome(check: dict[str, Any]) -> str:
    """Re-derive a case's expected outcome from its deterministic predicate."""
    predicate = check.get("predicate_type")
    params = check.get("params") or {}
    if predicate == "arith":
        a, b, op = params["a"], params["b"], params["op"]
        if op not in ARITH_OPS:
            raise ValueError(f"unsupported arith op: {op}")
        if op == "div" and (b == 0 or a % b != 0):
            raise ValueError("arith div must be exact integer division")
        truth = {"add": a + b, "sub": a - b, "mul": a * b, "div": a // b}[op]
        return "pass" if params["claimed"] == truth else "fail"
    if predicate == "count":
        return "pass" if params["claimed"] == len(params["items"]) else "fail"
    if predicate == "membership":
        actual = params["item"] in params["items"]
        return "pass" if params["claimed_present"] == actual else "fail"
    if predicate == "date_delta":
        start = date.fromisoformat(params["start"])
        end = date.fromisoformat(params["end"])
        return "pass" if params["claimed"] == (end - start).days else "fail"
    if predicate == "string_transform":
        if params["op"] not in STRING_OPS:
            raise ValueError(f"unsupported string op: {params['op']}")
        return "pass" if params["claimed"] == _string_transform(params["op"], params["input"]) else "fail"
    if predicate == "max_min":
        if params["op"] not in {"max", "min"}:
            raise ValueError(f"unsupported extremum op: {params['op']}")
        truth = max(params["items"]) if params["op"] == "max" else min(params["items"])
        return "pass" if params["claimed"] == truth else "fail"
    if predicate == "lookup_join":
        table = params["table"]
        key = params["key"]
        if key not in table:
            raise ValueError(f"lookup key not present in table: {key}")
        return "pass" if params["claimed"] == table[key] else "fail"
    if predicate == "unsupported_claim":
        supported = any(params["cited_value"] in line for line in params["inputs"])
        return "pass" if supported else "fail"
    raise ValueError(f"unknown predicate_type: {predicate}")


def verify_dataset(dataset: dict[str, Any], spec: dict[str, Any], schema: dict[str, Any]) -> list[str]:
    """Return a list of errors; an empty list means the dataset is valid."""
    errors: list[str] = []
    for schema_error in sorted(Draft202012Validator(schema).iter_errors(dataset), key=lambda e: list(e.absolute_path)):
        errors.append(f"schema: {schema_error.message}")

    cases = dataset.get("cases")
    if not isinstance(cases, list):
        return errors + ["dataset.cases must be an array"]
    if len(cases) < 100:
        errors.append(f"dataset must contain at least 100 cases, found {len(cases)}")

    checks = spec.get("checks")
    if not isinstance(checks, list):
        return errors + ["verifier spec must contain a checks array"]
    checks_by_id: dict[str, dict[str, Any]] = {}
    for check in checks:
        check_id = check.get("case_id")
        if check_id in checks_by_id:
            errors.append(f"duplicate verifier check for {check_id}")
        checks_by_id[check_id] = check

    case_ids: list[str] = []
    outcomes: set[str] = set()
    for case in cases:
        case_id = case.get("case_id")
        case_ids.append(case_id)
        expected = case.get("expected_outcome")
        outcomes.add(expected)
        check = checks_by_id.get(case_id)
        if check is None:
            errors.append(f"{case_id}: no deterministic check in the verifier spec")
            continue
        try:
            derived = derive_outcome(check)
        except (KeyError, ValueError, TypeError) as exc:
            errors.append(f"{case_id}: predicate re-derivation failed: {exc}")
            continue
        if derived != expected:
            errors.append(f"{case_id}: predicate derivation {derived!r} != expected_outcome {expected!r}")
        adjudication = case.get("adjudication") or {}
        if adjudication.get("reviewer_id") != REVIEWER_ID:
            errors.append(f"{case_id}: adjudication reviewer must be the deterministic verifier")
        references = adjudication.get("evidence_references") or []
        if not any(f"#check:{case_id}" in ref for ref in references):
            errors.append(f"{case_id}: adjudication must reference its verifier check")

    if len(set(case_ids)) != len(case_ids):
        errors.append("dataset contains duplicate case IDs")
    unknown = set(checks_by_id) - set(case_ids)
    for check_id in sorted(unknown):
        errors.append(f"{check_id}: verifier check has no dataset case")
    if outcomes != {"pass", "fail"}:
        errors.append("dataset must include both pass and fail cases")
    return errors


def build_report(dataset: dict[str, Any], spec: dict[str, Any], errors: list[str], dataset_raw: bytes, spec_raw: bytes) -> dict[str, Any]:
    cases = dataset.get("cases") or []
    pass_count = sum(1 for case in cases if case.get("expected_outcome") == "pass")
    return {
        "benchmark_id": dataset.get("benchmark_id"),
        "dataset_status": "VALID_DETERMINISTIC_GROUND_TRUTH" if not errors else "INVALID",
        "case_count": len(cases),
        "pass_count": pass_count,
        "fail_count": len(cases) - pass_count,
        "dataset_sha256": sha256_bytes(dataset_raw),
        "verifier_spec_sha256": sha256_bytes(spec_raw),
        "ground_truth_method": "deterministic_predicate_re_derivation",
        "reviewer": REVIEWER_ID,
        "errors": errors,
        "empirical_result": "NOT_RUN",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", type=Path, default=DEFAULT_DATASET)
    parser.add_argument("--spec", type=Path, default=DEFAULT_SPEC)
    parser.add_argument("--schema", type=Path, default=DEFAULT_SCHEMA)
    args = parser.parse_args()

    dataset_raw = args.dataset.read_bytes()
    spec_raw = args.spec.read_bytes()
    dataset = json.loads(dataset_raw)
    spec = json.loads(spec_raw)
    schema = json.loads(args.schema.read_text(encoding="utf-8"))
    errors = verify_dataset(dataset, spec, schema)
    report = build_report(dataset, spec, errors, dataset_raw, spec_raw)
    print(json.dumps(report, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
