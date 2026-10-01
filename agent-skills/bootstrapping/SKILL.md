---
name: bootstrapping
description: Generate controlled synthetic training or demonstration data to improve a model or agent without treating self-generated data as independent ground truth. Use explicit budgets, provenance, uncertainty handling, and postcondition verification.
---

# Bootstrapping

## Description

Generate controlled synthetic training or demonstration data to improve a model or agent without treating self-generated data as independent ground truth.

## When to Use

Use when the pattern's objective and acceptance criteria are observable.

## Inputs / Outputs

- Inputs: validated task context, pattern configuration, authorization, and execution bounds.
- Outputs: structured result with provenance, assumptions, and unresolved uncertainty where material.

## Procedure

1. Define objective and termination criteria.
2. Validate inputs and authorization boundaries.
3. Execute within explicit budgets.
4. Preserve provenance.
5. Verify the result.
6. Report uncertainty and conflicts.

## Failure Modes

- Ambiguous objective.
- Budget exhaustion.
- Correlated outputs treated as independent evidence.
- Unsupported or stale evidence.
- Unauthorized state mutation.
- Unverified completion.

## Runnable Example

```python
pattern = {"capability": "bootstrapping", "validated": True, "budget": 4}
assert pattern["validated"] and pattern["budget"] > 0
print({"status": "bounded_execution", "capability": pattern["capability"]})
```

## Evidence

Canonical repository skill: skills/09-agentic-patterns/bootstrapping.md. Repository schema, validation workflows, Agent Skills contract, and security gates define local conformance. Pattern-specific claims require reproducible implementation evidence or authoritative primary documentation.

## Related

- 09-agentic-patterns
- input-guardrails
- output-guardrails
