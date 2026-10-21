---
title: "Enterprise Agent Task Context Retention"
category: 03-memory
level: advanced
stability: experimental
description: "Retain task context for enterprise work agents so long-running work survives handoffs with bounded, auditable state."
added: "2026-10"
version: v1
related: [persistent-agent-workspace-memory, context-window-budget-planning]
tags: [memory, retention, enterprise, agents]
---
# Enterprise Agent Task Context Retention

## Description
Retain task context for enterprise work agents so long-running work survives handoffs with bounded, auditable state. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- An enterprise agent works across days and its task context must be retained and auditable across sessions.
- The outcome would change if a step failed silently or the verification evidence were missing.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | the declared input set, policy thresholds, and explicit acceptance criteria. |
| Outputs | A structured record with the decision, rejected alternatives, and the verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Persist the active task context with per-task scope, expiry, and owner fields, and record each retention pass with what was kept, demoted, and expired.
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
def retain(tasks, max_active=2):
    active = [t for t in tasks if t["state"] == "active"]
    demoted = sorted(active, key=lambda t: t["priority"])[:-max_active]
    return [d["id"] for d in demoted]
tasks = [{"id": "a", "state": "active", "priority": 1}, {"id": "b", "state": "active", "priority": 3}]
assert retain(tasks) == ["a"]
```

## Failure Modes
- Task context is retained indefinitely and retention scope grows unbounded.
- Expiry has no owner review and active work is dropped mid-task.
- Retention passes are not recorded and handoffs cannot explain the kept set.
- Personal data is retained under a task scope that never had a lawful basis.
- Demoted tasks have no reactivation trigger and work silently stalls.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- Google Cloud introduced the Gemini agent as one universal agent for enterprise work (cloud.google.com, dated October 8, 2026) ([public signal](https://cloud.google.com/blog/products/ai-machine-learning/welcome-to-gemini-at-work-2026))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Persistent Agent Workspace Memory](../03-memory/persistent-agent-workspace-memory.md)
- [Context Window Budget Planning](../03-memory/context-window-budget-planning.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
