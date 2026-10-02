---
name: consensus-voting
description: Combine independent agent votes under an explicit voting rule, quorum, tie-break policy, and evidence boundary.
metadata:
  source: skills/15-orchestration/consensus-voting.md
  category: 15-orchestration
---

**Category:** Orchestration
**Skill Level:** `advanced`
**Stability:** stable

## Description
Combine independent agent votes under an explicit voting rule, quorum, tie-break policy, and evidence boundary.

## When to Use
Use when multiple independent assessments are available and a consensus mechanism is justified.

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
task = {"capability": "consensus-voting", "validated": True}
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
Consensus is not proof of correctness; preserve dissent, voter independence, and underlying evidence.

## Evidence
Canonical repository skill: this file. Structural conformance is defined by the repository schema, validation workflows, Agent Skills contract, and security gates. Orchestration decisions must preserve state, ownership, and material evidence.

## Related
- 15-orchestration
- input-guardrails
- output-guardrails
