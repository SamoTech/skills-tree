---
name: stock-lookup
description: Retrieve and normalize supplied or connected market-data results for a requested security, preserving timestamp and source context.
metadata:
  source: skills/16-domain-specific/stock-lookup.md
  category: 16-domain-specific
---

**Category:** Domain-Specific
**Skill Level:** `advanced`
**Stability:** stable

## Description
Retrieve and normalize supplied or connected market-data results for a requested security, preserving timestamp and source context.

## When to Use
Use when the security identifier, market, and required observation time are known.

## Inputs / Outputs / Failure Modes
| Area | Contract |
|---|---|
| Inputs | Source material, domain context, task constraints, and required output format. |
| Outputs | Structured result with provenance, assumptions, uncertainty, and validation findings where material. |
| Failure modes | Missing context, stale/conflicting evidence, unsupported inference, malformed output, or skipped verification. |

## Procedure
1. Establish task scope, source boundaries, and required output schema.
2. Validate that the source material and domain context are sufficient.
3. Produce the result while preserving source meaning and separating evidence from inference.
4. Validate calculations, claims, citations, constraints, and required fields.
5. Escalate material ambiguity instead of inventing missing facts.

## Runnable Example
```python
task = {"capability": "stock-lookup", "validated": True}
assert task["validated"]
result = {"status": "review_required", "capability": task["capability"]}
print(result)
```

## Failure Modes
- Missing or ambiguous source context.
- Unsupported domain inference.
- Stale, conflicting, or unverifiable evidence.
- Presenting generated output as authoritative professional advice.
- Skipping validation or provenance checks.

## Domain Boundary
Market data can be delayed or provider-dependent; never present stale data as real-time and do not turn lookup output into investment advice.

## Evidence
Canonical repository skill: this file. Structural conformance is defined by the repository schema, validation workflows, Agent Skills contract, and security gates. Domain-specific factual claims must remain traceable to supplied or independently verified authoritative sources.

## Related
- 16-domain-specific
- input-guardrails
- output-guardrails
