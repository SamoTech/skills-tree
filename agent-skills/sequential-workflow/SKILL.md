---
name: sequential-workflow
description: Execute workflow stages in a declared order with explicit dependencies, checkpoints, and completion criteria.
metadata:
  source: skills/15-orchestration/sequential-workflow.md
  category: 15-orchestration
---

**Category:** Orchestration
**Skill Level:** `advanced`
**Stability:** stable

## Description
Execute workflow stages in a declared order with explicit dependencies, checkpoints, and completion criteria.

## When to Use
Use when later stages depend on verified outputs from earlier stages.

## Inputs / Outputs / Failure Modes
| Area | Contract |
|---|---|
| Inputs | Workflow state, roles, task constraints, dependencies, authorization, and acceptance criteria. |
| Outputs | Explicit orchestration state/result with ownership, evidence, and recovery information. |
| Failure modes | Stale state, ambiguous transitions, duplicate work, missing authority, or unverifiable completion. |

## Procedure
1. Establish state, ownership, dependencies, and acceptance criteria.
2. Validate preconditions before changing workflow state.
3. Execute the declared orchestration operation within bounded authority.
4. Record state changes, evidence, and unresolved conditions.
5. Apply explicit retry, recovery, escalation, or terminal behavior when required.

## Runnable Example
```python
task = {"capability": "sequential-workflow", "validated": True}
assert task["validated"]
result = {"status": "orchestration_step", "capability": task["capability"]}
print(result)
```

## Failure Modes
- Missing or ambiguous workflow state.
- Invalid transition or unmet dependency.
- Duplicate or concurrent execution.
- Capability or authority exceeds declared scope.
- Completion cannot be verified.

## Orchestration Boundary
Do not advance on unverified or partial outputs; preserve stage state and failure handling.

## Evidence
Canonical repository skill: this file. Structural conformance is defined by the repository schema, validation workflows, Agent Skills contract, and security gates. Orchestration state must remain explicit, bounded, and traceable.

## Related
- 15-orchestration
- input-guardrails
- output-guardrails
