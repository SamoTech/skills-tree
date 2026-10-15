---
name: a2a-task-lifecycle-management
description: Drive A2A task objects through their lifecycle states, with recorded state transitions and terminal detection.
metadata:
  source: skills/07-tool-use/a2a-task-lifecycle-management.md
  category: 07-tool-use
  version: "v1"
---

# A2a Task Lifecycle Management

## Description
Drive A2A task objects through their lifecycle states, with recorded state transitions and terminal detection. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- A task requires a2a task lifecycle management before downstream steps can proceed safely.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for a2a task lifecycle management. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the a2a task lifecycle management steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
TERMINAL = {"completed", "failed", "canceled"}
def step(state, transition):
    if state in TERMINAL:
        raise ValueError("terminal task")
    return transition
assert step("submitted", lambda: "working")() == "working"
try:
    step("failed", lambda: "working"); raise AssertionError("should have raised")
except ValueError:
    print("terminal guard held")
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
A2A v1.0 defines tasks with eight lifecycle states; agent teams request lifecycle management guidance. These are dated public signals, not adoption metrics.

## Related
- a2a-tool.md
- a2a-agent-card-authoring.md
- composite-tool-composition.md
