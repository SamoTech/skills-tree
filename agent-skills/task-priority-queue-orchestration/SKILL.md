---
name: task-priority-queue-orchestration
description: Orchestrate agent tasks through priority queues with fairness classes, starvation guards, and dead-letter handling.
metadata:
  source: skills/15-orchestration/task-priority-queue-orchestration.md
  category: 15-orchestration
  version: "v1"
---

# Task Priority Queue Orchestration

## Description
Orchestrate agent tasks through priority queues with fairness classes, starvation guards, and dead-letter handling. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- A task requires task priority queue orchestration before downstream steps can proceed safely.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for task priority queue orchestration. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the task priority queue orchestration steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def pop(queue):
    if not queue:
        return None
    queue.sort(key=lambda t: (t["prio"], t["seq"]))
    return queue.pop(0)
q = [{"prio": 2, "seq": 1, "id": "b"}, {"prio": 1, "seq": 2, "id": "a"}]
assert pop(q)["id"] == "a"
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
Priority queueing with starvation prevention is a recurring multi-agent scheduling request. These are dated public signals, not adoption metrics.

## Related
- prioritization.md
- message-queue-consuming.md
- queue-infrastructure-provisioning.md
