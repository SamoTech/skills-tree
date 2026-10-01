---
title: "Nosql Query"
category: 12-data
level: advanced
stability: stable
description: "Construct and validate NoSQL queries against an explicit document or key-value schema and query contract."
added: "2025-03"
related: ["12-data", "input-guardrails", "output-guardrails"]
---

**Category:** Data
**Skill Level:** `advanced`
**Stability:** stable

## Description
Construct and validate NoSQL queries against an explicit document or key-value schema and query contract.

## When to Use
Use when collection structure, query semantics, and expected result shape are known.

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
task = {"capability": "nosql-query", "validated": True}
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
Query semantics vary by database; validate against the target engine and avoid unbounded scans.

## Evidence
Canonical repository skill: this file. Structural conformance is defined by the repository schema, validation workflows, Agent Skills contract, and security gates. Data results must preserve provenance and make material assumptions explicit.

## Related
- 12-data
- input-guardrails
- output-guardrails
