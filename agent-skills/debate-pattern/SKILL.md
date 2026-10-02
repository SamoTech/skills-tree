---
name: debate-pattern
description: Use multiple role-separated agents to present, challenge, and reconcile competing claims under an explicit evidence protocol.
metadata:
  source: skills/09-agentic-patterns/debate-pattern.md
  category: 09-agentic-patterns
---

## Description
Use multiple role-separated agents to present, challenge, and reconcile competing claims under an explicit evidence protocol.

## When to Use
Use when adversarial examination can expose assumptions or missing evidence.

## Inputs / Outputs / Failure Modes
| Area | Contract |
|---|---|
| Inputs | claim_or_question, roles, and task constraints or execution bounds. |
| Outputs | synthesized_result with assumptions, evidence references, and unresolved uncertainty where material. |
| Failure modes | Debate does not guarantee truth; agents may agree on the same error, and rhetorical strength must not substitute for evidence. |

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
    "capability": "debate-pattern",
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
