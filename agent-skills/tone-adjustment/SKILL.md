---
name: tone-adjustment
description: Transform wording to a declared tone while preserving factual meaning, intent, and required constraints.
metadata:
  source: skills/06-communication/tone-adjustment.md
  category: 06-communication
---

## Description

Transform wording to a declared tone while preserving factual meaning, intent, and required constraints.

## When to Use

Use when the output contract or target tone is explicit and can be checked after transformation.

## Inputs / Outputs / Failure Modes

| Area | Contract |
|---|---|
| Inputs | source text, target tone, audience, and protected facts. |
| Outputs | tone-adjusted text with preserved meaning and unresolved ambiguity. |
| Failure modes | Schema mismatch, semantic drift, omitted constraints, unsupported assumptions, or acceptance without validation. |

## Procedure

1. Parse the requested output contract, protected meaning, audience, and constraints.
2. Generate or transform the content within the declared bounds.
3. Validate structure, semantics, required fields, and protected facts.
4. Preserve provenance and distinguish transformed wording from new claims.
5. Report validation errors or ambiguity instead of silently coercing the result.

## Runnable Example

```python
task = {"capability": "tone-adjustment", "validated": True, "budget": 4}
assert task["validated"] and task["budget"] > 0
print({"status": "contract_checked", "capability": task["capability"]})
```

## Failure Modes

- Output fails the declared schema or target tone.
- Transformation changes factual meaning or user intent.
- Missing constraints are guessed rather than clarified.
- New claims are introduced without evidence.
- Validation is skipped before downstream use.

## Safety Boundary

Formatting, tone, or persona changes do not authorize factual changes, fabricated sources, or disclosure of protected information.

## Evidence

Canonical repository skill: this file. Structural conformance is governed by the repository schema, validation workflows, Agent Skills contract, and security gates. Generated output is not evidence by itself.

## Related

- 06-communication
- input-guardrails
- output-guardrails
