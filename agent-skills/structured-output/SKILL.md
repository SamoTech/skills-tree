---
name: structured-output
description: Generate machine-readable output that conforms to a declared schema and preserves validation failures instead of silently coercing invalid data. Preserve constraints, meaning, and validation boundaries.
---

# Structured Output

## Description

Generate machine-readable output that conforms to a declared schema and preserves validation failures instead of silently coercing invalid data.

## When to Use

Use when the output contract or target tone is explicit and can be checked after transformation.

## Inputs / Outputs

- Inputs: source content, declared constraints, audience, and validation criteria.
- Outputs: transformed or structured result with validation status and unresolved ambiguity.

## Procedure

1. Parse the requested contract and protected meaning.
2. Produce the transformation within explicit bounds.
3. Validate structure, semantics, required fields, and protected facts.
4. Preserve provenance and distinguish transformation from new claims.
5. Report errors or ambiguity rather than silently coercing.

## Failure Modes

- Contract or tone mismatch.
- Semantic drift.
- Missing constraints guessed rather than clarified.
- Unsupported claims introduced.
- Validation skipped.

## Runnable Example

```python
task = {"capability": "structured-output", "validated": True, "budget": 4}
assert task["validated"] and task["budget"] > 0
print({"status": "contract_checked", "capability": task["capability"]})
```

## Evidence

Canonical repository skill: skills/06-communication/structured-output.md. Repository schema, validation workflows, Agent Skills contract, and security gates define local conformance. Generated output is not evidence by itself.

## Related

- 06-communication
- input-guardrails
- output-guardrails
