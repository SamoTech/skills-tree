---
name: schema-inference
description: Infer candidate data schemas from representative records while distinguishing observed fields from inferred types or optionality.
metadata:
  source: skills/12-data/schema-inference.md
  category: 12-data
---

**Category:** Data
**Skill Level:** `advanced`
**Stability:** stable

## Description
Infer candidate data schemas from representative records while distinguishing observed fields from inferred types or optionality.

## When to Use
Use when a source schema is absent and representative samples are available.

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
task = {"capability": "schema-inference", "validated": True}
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
Inference from samples can miss rare fields or types; treat the result as a candidate schema requiring validation.

## Evidence
Canonical repository skill: this file. Structural conformance is defined by the repository schema, validation workflows, Agent Skills contract, and security gates. Data results must preserve provenance and make material assumptions explicit.

## Related
- 12-data
- input-guardrails
- output-guardrails
