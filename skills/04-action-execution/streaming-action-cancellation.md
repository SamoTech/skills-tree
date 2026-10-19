---
title: "Streaming Action Cancellation"
category: 04-action-execution
level: advanced
stability: experimental
description: "Cancel an in-flight streaming action at a safe boundary so that partial effects are either completed cleanly or rolled back on record."
added: "2026-10"
version: v1
related: [human-takeover-mid-action-handoff, long-running-action-monitoring]
tags: [cancellation, streaming, actions, safety]
---
# Streaming Action Cancellation

## Description
Cancel an in-flight streaming action at a safe boundary so that partial effects are either completed cleanly or rolled back on record. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A user or supervisor must stop a long streaming action without leaving half-written effects.
- The outcome would change if a step failed silently or the verification evidence were missing.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | the declared input set, policy thresholds, and explicit acceptance criteria. |
| Outputs | A structured record with the decision, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Register the cancellation token before the stream starts, define the safe boundaries where cancellation may land, and on cancel complete or roll back the partial effect and record which boundary was chosen.
4. Compare the actual outcome against the acceptance criteria and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Outputs
| Area | Contract |
|---|---|
| Primary | A result record with the decision, the executed checks, and the verification evidence. |
| Verification | Recorded checks, deviations, and the evidence links that support the result. |
| Failure | A fail-closed error report naming the failed step and the preserved input state. |

## Runnable Example
```python
def cancel_at_boundary(sent, total, boundaries):
    if sent == total:
        return "completed"
    if sent in boundaries:
        return "rolled_back"
    return "finish_then_rollback"
assert cancel_at_boundary(10, 10, [5]) == "completed"
assert cancel_at_boundary(5, 10, [5]) == "rolled_back"
```

## Failure Modes
- Cancellation aborts mid-chunk and leaves a corrupted partial write behind.
- The cancel token is checked only between actions, so a single long action cannot be stopped at all.
- Rollback of the partial effect is attempted without a record of what was already emitted.
- A cancelled stream still reports success to the caller because completion checks the wrong flag.
- Cancellation during the final flush is treated as failure and redoes an already-committed effect.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- 2026 observability reporting covers controlling acting agents mid-stream as a debugging and safety requirement (futransolutions.com, dated October 2026) ([public signal](https://futransolutions.com/blog/ai-agent-observability-in-2026-how-to-trace-evaluate-and-debug-ai-that-takes-action/))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Human Takeover Mid-Action Handoff](../04-action-execution/human-takeover-mid-action-handoff.md)
- [Long-Running Action Monitoring](../04-action-execution/long-running-action-monitoring.md)

## Changelog
| Version | Date | Notes |
|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
