---
name: csv-processing
description: Read, validate, transform, and export CSV data while preserving schema and row-level integrity.
metadata:
  source: skills/12-data/csv-processing.md
  category: 12-data
---

**Category:** Data
**Skill Level:** `advanced`
**Stability:** stable

## Description
Read, validate, transform, and export CSV data while preserving schema and row-level integrity.

## When to Use
Use when CSV input and required output schema are explicit.

## Inputs / Outputs / Failure Modes
| Area | Contract |
|---|---|
| Inputs | Dataset or records, schema/context, transformation rules, and required output format. |
| Outputs | Structured result with row counts, assumptions, validation findings, and provenance where material. |
| Failure modes | Schema mismatch, null/encoding issues, silent data loss, cardinality errors, or skipped validation. |

## Procedure
1. Inspect the source schema and establish explicit transformation semantics.
2. Validate required fields, types, encoding, null behavior, and relevant constraints.
3. Apply only the declared transformation or analysis.
4. Compare input/output counts and validate the resulting schema and values.
5. Preserve source data and record material assumptions or exceptions.

## Runnable Example
```python
task = {"capability": "csv-processing", "validated": True}
assert task["validated"]
result = {"status": "validation_required", "capability": task["capability"]}
print(result)
```

## Failure Modes
- Missing or ambiguous schema.
- Unexpected nulls, duplicates, or malformed records.
- Silent row/field loss.
- Incorrect join, aggregation, or type coercion semantics.
- Output not validated against the required contract.

## Data Boundary
Handle encoding, quoting, missing values, and malformed rows explicitly; never silently drop data.

## Evidence
Canonical repository skill: this file. Structural conformance is defined by the repository schema, validation workflows, Agent Skills contract, and security gates. Data transformations must preserve provenance and make material assumptions explicit.

## Related
- 12-data
- input-guardrails
- output-guardrails
