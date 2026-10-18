---
title: "Human Takeover Mid-Action Handoff"
category: 04-action-execution
level: advanced
stability: experimental
description: "Transfer control of an in-progress multi-step action to a human operator with complete state context, then record what the operator changed before resuming."
added: "2026-10"
version: v1
related: [human-approval-gate-implementation, agent-handoff]
tags: [takeover, handoff, human-control]
---
# Human Takeover Mid-Action Handoff

## Description
Transfer control of an in-progress multi-step action to a human operator with complete state context, then record what the operator changed before resuming. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A human operator must take over an agent action sequence that is partially complete.
- The outcome would change if inputs were stale, ambiguous, or incomplete.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | mid-action human takeover handoff task context, candidate data, and explicit acceptance criteria. |
| Outputs | A structured record with the decision, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the mid-action human takeover handoff steps in a bounded, checkpointed way.
4. Compare the actual outcome against the acceptance criteria and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Outputs
| Area | Contract |
|---|---|
| Primary | A takeover record with the state at handoff, the operator's declared changes, and the verified resumption point. |
| Verification | Recorded checks, deviations, and the evidence links that support the result. |
| Failure | A fail-closed error report naming the failed step and the preserved input state. |

## Runnable Example
```python
def resume(state, operator_changes):
    if operator_changes and not state["acknowledged"]:
        return "blocked-pending-ack"
    return "resume"
assert resume({"acknowledged": False}, ["edit"]) == "blocked-pending-ack"
assert resume({"acknowledged": True}, []) == "resume"
```

## Failure Modes
- Handing over state context that omits actions already in flight.
- Resuming execution without verifying what the operator changed during takeover.
- Treating the operator's clarifying question as an instruction to continue.
- Losing the takeover boundary so later audit cannot separate agent and human actions.
- Resuming from a stale snapshot after the operator advanced the task manually.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- 2026 agentic security best-practice guides require explicit human takeover boundaries with verified state handoff ([public signal](https://www.forcepoint.com/blog/insights/agentic-ai-security-best-practices))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Human Approval Gate Implementation](../04-action-execution/human-approval-gate-implementation.md)
- [Agent Handoff](../15-orchestration/agent-handoff.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
