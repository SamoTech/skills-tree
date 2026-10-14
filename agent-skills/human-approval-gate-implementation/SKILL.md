---
name: human-approval-gate-implementation
description: Implement approval gates that pause before irreversible actions, present the planned effect, and record the approver decision.
metadata:
  source: skills/04-action-execution/human-approval-gate-implementation.md
  category: 04-action-execution
  version: "v1"
---
# Human Approval Gate Implementation

## Description
Implement approval gates that pause before irreversible actions, present the planned effect, and record the approver decision. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- A task requires human approval gate implementation before downstream steps can proceed safely.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for human approval gate implementation. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the human approval gate implementation steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def gate(effect, irreversible, approved):
    if irreversible and not approved:
        return "blocked"
    return effect()
assert gate(lambda: "done", True, False) == "blocked"
assert gate(lambda: "done", False, False) == "done"
```

## Failure Modes
- Acting outside the declared task boundary.
- Assuming an estimate or preview equals the verified effect.
- Retrying without preserving state or evidence.
- Using stale inputs as if they were current.
- Reporting success without checking the resulting state.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Human-in-the-loop checkpoints for irreversible actions like production deploys are a standing 2026 agent guidance point. These are dated public signals, not adoption metrics.

## Related
- dry-run-execution.md
- action-precondition-checking.md
- compensating-actions.md
