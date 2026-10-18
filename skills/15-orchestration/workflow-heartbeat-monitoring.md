---
title: "Workflow Heartbeat Monitoring"
category: 15-orchestration
level: advanced
stability: experimental
description: "Monitor long-running agent workflows with periodic heartbeats that carry progress state, so silent stalls raise an alert with the last known checkpoint."
added: "2026-10"
version: v1
related: [long-running-action-monitoring, agent-halt-conditions]
tags: [heartbeats, monitoring, workflows]
---
# Workflow Heartbeat Monitoring

## Description
Monitor long-running agent workflows with periodic heartbeats that carry progress state, so silent stalls raise an alert with the last known checkpoint. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- An agent operator must detect silently stalled long-running workflows.
- The outcome would change if inputs were stale, ambiguous, or incomplete.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | workflow heartbeat monitoring task context, candidate data, and explicit acceptance criteria. |
| Outputs | A structured record with the decision, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the workflow heartbeat monitoring steps in a bounded, checkpointed way.
4. Compare the actual outcome against the acceptance criteria and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Outputs
| Area | Contract |
|---|---|
| Primary | A heartbeat log with progress state and an alert carrying the last known checkpoint. |
| Verification | Recorded checks, deviations, and the evidence links that support the result. |
| Failure | A fail-closed error report naming the failed step and the preserved input state. |

## Runnable Example
```python
def stalled(last_beat_age_s, limit=120):
    return last_beat_age_s > limit
assert stalled(200) is True
assert stalled(30) is False
```

## Failure Modes
- Acting outside the declared task boundary.
- Heartbeats that carry no progress state, so stalls look like slow progress.
- Alerting on the workflow start time instead of the last heartbeat.
- Restarting from scratch when the last checkpoint was intact.
- Reporting success without checking the resulting state.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- Agent observability guides use heartbeats to detect stalled agent workflows. ([public signal](https://www.braintrust.dev/articles/agent-observability-complete-guide-2026))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Long Running Action Monitoring](../04-action-execution/long-running-action-monitoring.md)
- [Agent Halt Conditions](../09-agentic-patterns/agent-halt-conditions.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
