---
name: tool-use-loop
description: Run a bounded agent loop that can dispatch multiple independent tool calls in one step and reconcile their observations before continuing.
metadata:
  source: skills/09-agentic-patterns/tool-use-loop.md
  category: 09-agentic-patterns
---

## Description

Run a bounded agent loop that can dispatch multiple independent tool calls in one step and reconcile their observations before continuing.

## When to Use

Use when the pattern has a measurable objective, explicit acceptance criteria, and a bounded execution budget.

## Inputs / Outputs / Failure Modes

| Area | Contract |
|---|---|
| Inputs | task state, tool contracts, parallelism limit, authorization, and termination criteria. |
| Outputs | tool observations, reconciled state, provenance, and verified outcome. |
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
pattern = {"capability": "tool-use-loop", "validated": True, "budget": 4}
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
