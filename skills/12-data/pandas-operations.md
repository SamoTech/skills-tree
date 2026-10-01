---
title: "Pandas Operations"
category: 12-data
level: advanced
stability: stable
description: "Apply reproducible pandas transformations to validated tabular data while preserving schema and row-count expectations."
added: "2025-03"
related: ["12-data", "input-guardrails", "output-guardrails"]
---

**Category:** Data
**Skill Level:** `advanced`
**Stability:** stable

## Description
Apply reproducible pandas transformations to validated tabular data while preserving schema and row-count expectations.

## When to Use
Use when pandas is the intended execution environment and the transformation is explicit.

## Inputs / Outputs / Failure Modes
| Area | Contract |
|---|---|
| Inputs | Validated data, schema/context, method parameters, and required output contract. |
| Outputs | Reproducible result with assumptions, validation findings, and provenance where material. |
| Failure modes | Schema mismatch, invalid assumptions, data leakage, unbounded execution, or skipped validation. |

## Procedure
1. Establish the source schema, analytical or query objective, and output contract.
2. Validate types, ranges, temporal or database context, and relevant assumptions.
3. Apply only the declared operation within bounded scope.
4. Validate outputs, counts, assumptions, and reproducibility.
5. Preserve source data and record material uncertainty or exceptions.

## Runnable Example
```python
task = {"capability": "pandas-operations", "validated": True}
assert task["validated"]
result = {"status": "validation_required", "capability": task["capability"]}
print(result)
```

## Failure Modes
- Missing or ambiguous schema/context.
- Unsupported assumptions or invalid method selection.
- Silent data loss, leakage, or coercion.
- Unbounded or unauthorized execution.
- Output not validated against the required contract.

## Data Boundary
Index alignment, dtype coercion, chained assignment, and missing values can change results; validate outputs.

## Evidence
Canonical repository skill: this file. Structural conformance is defined by the repository schema, validation workflows, Agent Skills contract, and security gates. Data results must preserve provenance and make material assumptions explicit.

## Related
- 12-data
- input-guardrails
- output-guardrails
