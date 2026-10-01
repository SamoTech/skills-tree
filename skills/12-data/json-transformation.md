---
title: "Json Transformation"
category: 12-data
level: advanced
stability: stable
description: "Transform JSON structures between explicit schemas while preserving required fields and data types."
added: "2025-03"
related: ["12-data", "input-guardrails", "output-guardrails"]
---

**Category:** Data
**Skill Level:** `advanced`
**Stability:** stable

## Description
Transform JSON structures between explicit schemas while preserving required fields and data types.

## When to Use
Use when source and target JSON schemas are known.

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
task = {"capability": "json-transformation", "validated": True}
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
Do not silently discard fields or coerce incompatible types; validate the transformed document against the target schema.

## Evidence
Canonical repository skill: this file. Structural conformance is defined by the repository schema, validation workflows, Agent Skills contract, and security gates. Data transformations must preserve provenance and make material assumptions explicit.

## Related
- 12-data
- input-guardrails
- output-guardrails
