---
name: long-task-progress-reporting
description: Report progress of long-running actions on a declared cadence with measurable units, distinguish progress from completion, and escalate stalled work.
metadata:
  source: skills/04-action-execution/long-task-progress-reporting.md
  category: 04-action-execution
  version: "v1"
---

# Long Task Progress Reporting

## Description
Report progress of long-running actions on a declared cadence with measurable units, distinguish progress from completion, and escalate stalled work. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- a long-running action must report measurable progress to a waiting consumer before downstream steps can proceed safely.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for long task progress reporting work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the long task progress reporting steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def progress(done, total, last_done=None):
    if total <= 0:
        raise ValueError("total must be positive")
    frac = done / total
    stalled = last_done is not None and done == last_done
    return {"fraction": round(frac, 3), "stalled": stalled}

assert progress(25, 100)["fraction"] == 0.25
assert progress(50, 100, last_done=50)["stalled"] is True
assert progress(75, 100, last_done=50)["stalled"] is False
```

## Failure Modes
- Reporting elapsed time as progress.
- Declaring completion while work remains.
- Hiding stall states behind a steady heartbeat.
- Choosing units the consumer cannot verify.
- Flooding the consumer with updates past the declared cadence.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Long-running agent task transparency is a recurring 2026 UX request signal in public coverage; this is a dated signal, not an adoption metric.

## Related
- long-running-action-monitoring.md
- notification-sending.md
- scheduled-execution.md
