---
name: hitl-checkpoint-pattern-design
description: Design checkpoint patterns where agents pause for human judgment at high-risk decision points with resumable state.
metadata:
  source: skills/09-agentic-patterns/hitl-checkpoint-pattern-design.md
  category: 09-agentic-patterns
  version: "v1"
---
# Hitl Checkpoint Pattern Design

## Description
Design checkpoint patterns where agents pause for human judgment at high-risk decision points with resumable state. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- A task requires hitl checkpoint pattern design before downstream steps can proceed safely.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for hitl checkpoint pattern design. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the hitl checkpoint pattern design steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def checkpoint(risk, threshold, human_ok):
    return "proceed" if risk < threshold else ("proceed" if human_ok else "pause")
assert checkpoint(0.9, 0.5, False) == "pause"
assert checkpoint(0.9, 0.5, True) == "proceed"
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
Human-in-the-loop checkpoints are a named 2026 pattern for high-stakes and irreversible agent actions. These are dated public signals, not adoption metrics.

## Related
- dry-run-execution.md
- self-correction.md
- action-precondition-checking.md
