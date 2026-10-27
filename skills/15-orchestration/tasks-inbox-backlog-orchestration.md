---
title: "Tasks Inbox Backlog Orchestration"
category: 15-orchestration
level: advanced
stability: experimental
description: "Orchestrate a user's agent task inbox as a capacity-bounded backlog that orders work by priority and age, deferring overflow explicitly instead of dropping or hiding it."
added: "2026-10"
version: v1
related: [task-priority-queue-orchestration, specialist-agent-routing]
tags: [tasks, inbox, backlog, orchestration]
---
# Tasks Inbox Backlog Orchestration

## Description
Orchestrate a user's agent task inbox as a capacity-bounded backlog that orders work by priority and age, deferring overflow explicitly instead of dropping or hiding it. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A unified agent's task inbox must be managed as a real queue with visible overflow.
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
3. Order the inbox by priority then age, accept up to the declared capacity, and return the explicit deferred list with reasons rather than silently truncating.
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
def schedule_inbox(tasks, capacity):
    order = sorted(tasks, key=lambda t: (t["priority"], t["created_at"]))
    return {"accepted": order[:capacity], "deferred": order[capacity:]}
s = schedule_inbox([{"id": "a", "priority": 2, "created_at": 1}, {"id": "b", "priority": 1, "created_at": 2}], 1)
assert s["accepted"][0]["id"] == "b" and s["deferred"][0]["id"] == "a"
```

## Failure Modes
- Overflow tasks are dropped and the user believes all delegated work is running.
- Priority ordering is overridden by insertion order under load and urgent work waits behind old items.
- Deferred tasks carry no reason and the user cannot tell why work did not start.
- Capacity is read from a config that drifted from the user's declared review limit.
- Aging is ignored and a starved low-priority task never surfaces at all.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- The Gemini tasks inbox where users track delegated agent tasks and subagent progress is the dated public signal for this orchestration contract. ([public signal](https://techcrunch.com/2026/10/08/google-brings-agentic-ai-to-gemini-starting-with-businesses/))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Task Priority Queue Orchestration](../15-orchestration/task-priority-queue-orchestration.md)
- [Specialist Agent Routing](../15-orchestration/specialist-agent-routing.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
