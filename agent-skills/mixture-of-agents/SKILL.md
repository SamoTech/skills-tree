---
name: mixture-of-agents
description: Route a task through multiple specialized agents and aggregate their outputs using an explicit synthesis policy.
metadata:
  source: skills/09-agentic-patterns/mixture-of-agents.md
  category: 09-agentic-patterns
---

## Description
Route a task through multiple specialized agents and aggregate their outputs using an explicit synthesis policy.

## When to Use
Use when specialization or independent perspectives can improve coverage and the aggregation rule is defined.

## Inputs / Outputs / Failure Modes
| Area | Contract |
|---|---|
| Inputs | task, agent_outputs, and task constraints or execution bounds. |
| Outputs | synthesized_output with assumptions, evidence references, and unresolved uncertainty where material. |
| Failure modes | More agents increase cost and correlated errors; measure whether added agents provide incremental signal before scaling. |

## Procedure
1. Define the objective, state representation, evaluation criteria, and termination condition.
2. Validate the inputs and establish the evidence boundary before generating candidates or branches.
3. Execute the pattern within an explicit compute, tool, depth, or agent budget.
4. Preserve candidate provenance and the observations or evidence supporting selection.
5. Verify the selected result against the declared criteria before acceptance.
6. Report uncertainty, conflicts, failed branches, or incomplete evidence instead of silently resolving them.

## Runnable Example
```python
pattern = {
    "capability": "mixture-of-agents",
    "validated": True,
    "budget": 4,
}
assert pattern["validated"] and pattern["budget"] > 0
result = {"status": "bounded_execution", "capability": pattern["capability"]}
print(result)
```

## Failure Modes
- Ambiguous objective or evaluation criterion.
- Search or agent budget exhaustion without a verified result.
- Correlated model errors presented as independent evidence.
- Stale, conflicting, or missing source evidence.
- Optimization against a proxy metric that diverges from the actual task objective.
- Completion reported without a reproducible postcondition.

## Evidence
Canonical repository skill: this file. Conformance is governed by the repository skill schema, validation workflows, Agent Skills contract, and security gates. Pattern-specific claims must be backed by reproducible implementation or cited primary evidence; generated reasoning is not itself evidence.

## Related
- 09-agentic-patterns
- input-guardrails
- output-guardrails
