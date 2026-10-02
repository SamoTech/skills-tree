---
name: anomaly-detection
description: Identify unusual observations in supplied datasets using explicit baselines, thresholds, or statistical criteria.
metadata:
  source: skills/12-data/anomaly-detection.md
  category: 12-data
---

**Category:** Data
**Skill Level:** `advanced`
**Stability:** stable

## Description
Identify unusual observations in supplied datasets using explicit baselines, thresholds, or statistical criteria.

## When to Use
Use when a dataset, comparison baseline, and anomaly objective are defined.

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
task = {"capability": "anomaly-detection", "validated": True}
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
An anomaly is not automatically an error or incident; investigate context before acting.

## Evidence
Canonical repository skill: this file. Structural conformance is defined by the repository schema, validation workflows, Agent Skills contract, and security gates. Data transformations must preserve provenance and make material assumptions explicit.

## Related
- 12-data
- input-guardrails
- output-guardrails
