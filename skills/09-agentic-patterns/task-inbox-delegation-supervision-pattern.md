---
title: "Task Inbox Delegation Supervision Pattern"
category: 09-agentic-patterns
level: advanced
stability: experimental
description: "Supervise delegated agent work through a tasks inbox that exposes state, subagent delegation, and blocked items, with escalation when the open-item limit is exceeded."
added: "2026-10"
version: v1
related: [agent-preflight-checklist-patterns, agent-fleet-monitoring]
tags: [task, inbox, delegation, supervision]
---
# Task Inbox Delegation Supervision Pattern

## Description
Supervise delegated agent work through a tasks inbox that exposes state, subagent delegation, and blocked items, with escalation when the open-item limit is exceeded. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A user must supervise an agent's delegated work through a single task inbox view.
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
3. Triage the inbox on a schedule, separate blocked-on-human items for escalation, and flag any open-item count above the declared limit before new work is accepted.
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
def triage_inbox(items, max_open):
    open_items = [i for i in items if i["state"] == "open"]
    blocked = [i for i in open_items if i["waiting_on"] == "human"]
    return {"over_limit": len(open_items) > max_open, "escalate": blocked}
t = triage_inbox([{"state": "open", "waiting_on": "human"}, {"state": "done", "waiting_on": None}] * 2, 3)
assert t["over_limit"] and len(t["escalate"]) == 2
```

## Failure Modes
- Blocked-on-human items sit in the inbox with no escalation and work stalls unnoticed.
- The open-item limit is never checked and the inbox grows past what the user can review.
- Done and open items are visually identical and review relies on memory.
- The limit is exceeded and new delegations are still accepted without triage.
- Subagent delegation is invisible in the inbox and supervision covers only top-level tasks.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- The Gemini tasks inbox exposing agent thinking, subagent delegation, and progress is the dated public signal for this pattern contract. ([public signal](https://techcrunch.com/2026/10/08/google-brings-agentic-ai-to-gemini-starting-with-businesses/))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Agent Preflight Checklist Patterns](../09-agentic-patterns/agent-preflight-checklist-patterns.md)
- [Agent Fleet Monitoring](../09-agentic-patterns/agent-fleet-monitoring.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
