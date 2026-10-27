---
title: "Team Organizational Context Memory"
category: 03-memory
level: advanced
stability: experimental
description: "Maintain an agent-side memory of team membership, time zones, approval roles, and meeting constraints so an agent can route work through the right human context."
added: "2026-10"
version: v1
related: [enterprise-agent-task-context-retention, user-profile-memory]
tags: [team, organizational, context, memory]
---
# Team Organizational Context Memory

## Description
Maintain an agent-side memory of team membership, time zones, approval roles, and meeting constraints so an agent can route work through the right human context. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- An agent operating with its own organizational account must remember who approves what, in which team, and in which time zone.
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
3. Store team membership with roles and time zones keyed by team, and answer every approval or routing lookup from that store with a recorded miss when the team is unknown.
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
def lookup_approver(context, team):
    members = context["teams"].get(team, [])
    approvers = [m for m in members if m["role"] == "approver" and m["timezone"] == context["actor_tz"]]
    return approvers[0]["name"] if approvers else None
ctx = {"actor_tz": "UTC", "teams": {"payments": [{"name": "Dana", "role": "approver", "timezone": "UTC"}, {"name": "Ravi", "role": "member", "timezone": "UTC"}]}}
assert lookup_approver(ctx, "payments") == "Dana" and lookup_approver(ctx, "nope") is None
```

## Failure Modes
- Approval decisions are made from a stale team map and the wrong approver is contacted.
- Time-zone context is dropped and requests are routed to approvers who are asleep.
- The memory is updated from an unverified chat remark and a fake approver enters the record.
- Team lookups silently return empty and the agent routes work to a default owner.
- A role change is never propagated and a departed employee remains the recorded approver.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- Google's unified Gemini agent operating with its own Workspace account and knowledge of teams, time zones, and approval owners is the dated public signal for this memory contract. ([public signal](https://techcrunch.com/2026/10/08/google-brings-agentic-ai-to-gemini-starting-with-businesses/))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Enterprise Agent Task Context Retention](../03-memory/enterprise-agent-task-context-retention.md)
- [User Profile Memory](../03-memory/user-profile-memory.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
