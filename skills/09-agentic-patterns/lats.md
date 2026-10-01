---
title: "LATS"
category: 09-agentic-patterns
level: advanced
stability: stable
description: "Combine tree search, tool use, and reflective evaluation to explore candidate actions under a bounded search budget."
added: "2025-03"
related: ["09-agentic-patterns", "input-guardrails", "output-guardrails"]
---

## Description
Combine tree search, tool use, and reflective evaluation to explore candidate actions under a bounded search budget.

## When to Use
Use when an agent must compare alternative tool-mediated trajectories and can tolerate additional inference cost.

## Inputs / Outputs / Failure Modes
| Area | Contract |
|---|---|
| Inputs | search_state, tool_observation, and task constraints or execution bounds. |
| Outputs | reflection_score with assumptions, evidence references, and unresolved uncertainty where material. |
| Failure modes | Do not claim benchmark superiority without reproducible evidence; keep search depth, tool permissions, and termination criteria explicit. |

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
    "capability": "lats",
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
