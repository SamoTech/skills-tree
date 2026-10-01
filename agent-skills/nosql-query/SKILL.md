---
name: nosql-query
description: Apply nosql query with explicit data contracts, validation, provenance, and bounded execution.
---

# nosql query

## Description
Apply nosql query only within a declared data contract and preserve reproducibility and provenance.

## Evidence
Canonical source: `skills/12-data/nosql-query.md`. Repository schema, Agent Skills validation, security scanning, and CI define structural conformance.

## Usage
Establish the source schema, method assumptions, execution bounds, validation rules, and expected output before processing.

## Failure modes
- Schema or context mismatch.
- Invalid assumptions or method selection.
- Silent data loss or leakage.
- Unbounded or unauthorized execution.
- Output not validated against the target contract.

## Related
- `12-data`
- `input-guardrails`
- `output-guardrails`
