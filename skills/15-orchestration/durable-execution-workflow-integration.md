---
title: "Durable Execution Workflow Integration"
category: 15-orchestration
level: advanced
stability: experimental
description: "Integrate agent task flows with durable execution engines so retries and resumes replay from recorded progress."
added: "2026-10"
version: v1
related: [long-running-action-monitoring, agent-checkpointing, scheduled-execution]
tags: [durable, execution, workflow, integration]
---
# Durable Execution Workflow Integration

## Description
Integrate agent task flows with durable execution engines so retries and resumes replay from recorded progress. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- A task requires durable execution workflow integration before downstream steps can proceed safely.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for durable execution workflow integration. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the durable execution workflow integration steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def replay(events, replayed_upto):
    return events[replayed_upto:]
assert replay(["a", "b", "c"], 1) == ["b", "c"]
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
Durable workflow engines are a named 2026 pattern for reliable long-running agent orchestration. These are dated public signals, not adoption metrics.

## Related
- long-running-action-monitoring.md
- agent-checkpointing.md
- scheduled-execution.md
