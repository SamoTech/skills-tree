---
name: constitutional-ai
description: Apply Constitutional Ai as a bounded agentic pattern with explicit inputs, evaluation criteria, budgets, evidence boundaries, and failure handling.
---

# Constitutional Ai

## Description
Apply this agentic pattern only within its declared scope. Define the objective, evaluation criteria, execution budget, and evidence boundary before use.

## When to Use
Use when the workflow explicitly benefits from this pattern and its acceptance criteria are observable.

## Inputs / Outputs
- Inputs: validated task context, pattern configuration, constraints, and evidence sources.
- Outputs: structured result with provenance, assumptions, and unresolved uncertainty where material.

## Failure Modes
- Ambiguous objective or evaluation criterion.
- Budget exhaustion without a verified result.
- Correlated model errors treated as independent evidence.
- Unsupported claims or stale source material.
- Acceptance without a reproducible postcondition.

## Runnable Example
```python
pattern = {"capability": "constitutional-ai", "validated": True, "budget": 4}
assert pattern["validated"] and pattern["budget"] > 0
print({"status": "bounded_execution", "capability": pattern["capability"]})
```

## Evidence
Canonical repository skill: skills/09-agentic-patterns/constitutional-ai.md. Repository schema and validation workflows define local conformance; pattern-specific claims require reproducible evidence.

## Related
- 09-agentic-patterns
- input-guardrails
- output-guardrails
