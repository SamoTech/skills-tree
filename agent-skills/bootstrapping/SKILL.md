---
name: bootstrapping
description: Generate controlled synthetic training or demonstration data to improve a model or agent without treating self-generated data as independent ground truth.
metadata:
  source: skills/09-agentic-patterns/bootstrapping.md
  category: 09-agentic-patterns
---

## Description

Generate controlled synthetic training or demonstration data to improve a model or agent without treating self-generated data as independent ground truth.

## When to Use

Use when the pattern has a measurable objective, explicit acceptance criteria, and a bounded execution budget.

## Inputs / Outputs / Failure Modes

| Area | Contract |
|---|---|
| Inputs | task distribution, generation policy, acceptance criteria, and compute/data budget. |
| Outputs | versioned synthetic dataset or demonstrations with provenance, filtering decisions, and evaluation results. |
| Failure modes | Ambiguous objective, budget exhaustion, correlated model errors, unsupported evidence, stale state, or acceptance without a reproducible postcondition. |

## Procedure

1. Define the objective, evaluation criteria, state representation, and termination condition.
2. Validate inputs, role boundaries, and the evidence boundary.
3. Execute within explicit compute, tool, depth, data, or agent budgets.
4. Preserve provenance for candidates, subagents, memories, and tool observations.
5. Verify the selected result against the declared criteria before acceptance.
6. Report conflicts, uncertainty, failed branches, and incomplete evidence.

## Runnable Example

```python
pattern = {"capability": "bootstrapping", "validated": True, "budget": 4}
assert pattern["validated"] and pattern["budget"] > 0
print({"status": "bounded_execution", "capability": pattern["capability"]})
```

## Failure Modes

- Objective or acceptance criterion is ambiguous.
- Budget is exhausted without a verified result.
- Correlated model outputs are treated as independent evidence.
- Stale or unsupported evidence is accepted.
- The pattern mutates state outside its authorization boundary.
- Completion is reported without a reproducible postcondition.

## Evidence

Canonical repository skill: this file. Repository schema, validation workflows, Agent Skills contract, and security gates define local conformance. Pattern-specific claims require reproducible implementation evidence or authoritative primary documentation; generated reasoning is not evidence by itself.

## Related

- 09-agentic-patterns
- input-guardrails
- output-guardrails
