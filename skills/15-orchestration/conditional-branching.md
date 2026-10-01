---
title: "Conditional Branching"
category: 15-orchestration
level: advanced
stability: stable
description: "Route workflow execution using explicit conditions, predicates, and mutually understood branch outcomes."
added: "2025-03"
related: ["15-orchestration", "input-guardrails", "output-guardrails"]
---

**Category:** Orchestration
**Skill Level:** `advanced`
**Stability:** stable

## Description
Route workflow execution using explicit conditions, predicates, and mutually understood branch outcomes.

## When to Use
Use when downstream execution depends on validated state or decision criteria.

## Inputs / Outputs / Failure Modes
| Area | Contract |
|---|---|
| Inputs | Workflow state, role/agent context, task constraints, trigger or decision criteria, and execution bounds. |
| Outputs | Deterministic orchestration decision/action plus state and evidence needed for downstream work. |
| Failure modes | Stale state, ambiguous ownership, race conditions, duplicate execution, or missing recovery path. |

## Procedure
1. Establish workflow state, ownership, boundaries, and acceptance criteria.
2. Validate the inputs or trigger before changing workflow state.
3. Execute only the declared orchestration operation.
4. Record resulting state, evidence, and unresolved conditions.
5. Apply explicit recovery or escalation behavior when the workflow cannot continue safely.

## Runnable Example
```python
task = {"capability": "conditional-branching", "validated": True}
assert task["validated"]
result = {"status": "orchestration_step", "capability": task["capability"]}
print(result)
```

## Failure Modes
- Ambiguous agent ownership or workflow state.
- Stale or conflicting state.
- Duplicate, concurrent, or non-idempotent execution.
- Missing authorization or recovery path.
- Completion reported without verifiable postconditions.

## Orchestration Boundary
Ambiguous predicates can route work incorrectly; validate branch inputs and define a default/error path.

## Evidence
Canonical repository skill: this file. Structural conformance is defined by the repository schema, validation workflows, Agent Skills contract, and security gates. Orchestration decisions must preserve state, ownership, and material evidence.

## Related
- 15-orchestration
- input-guardrails
- output-guardrails
