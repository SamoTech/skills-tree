---
title: "Agent Employee Roster Memory"
category: 03-memory
level: advanced
stability: experimental
description: "Maintain a roster memory of agent identities, assigned roles, supervisors, and status so agent-as-workforce operations stay auditable."
added: "2026-10"
version: v1
related: [long-horizon-goal-state-resume, agent-scope-session-isolation-memory]
tags: [roster, workforce, identity, memory]
---
# Agent Employee Roster Memory

## Description
Maintain a roster memory of agent identities, assigned roles, supervisors, and status so agent-as-workforce operations stay auditable. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- An organization registers AI agents as managed workers and must keep a durable roster of who each agent is, what role it holds, and who supervises it.
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
3. Upsert each agent into the roster under its stable identifier with role, supervisor, and status, then record every status change with a timestamped reason instead of in-place overwrites.
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
def upsert_roster(roster, agent, history):
    roster[agent["agent_id"]] = {"role": agent["role"], "supervisor": agent["supervisor"], "status": agent.get("status", "active")}
    history.append({"agent_id": agent["agent_id"], "status": agent.get("status", "active")})
    return roster
r = {}
h = []
upsert_roster(r, {"agent_id": "A-1", "role": "analyst", "supervisor": "team-lead"}, h)
upsert_roster(r, {"agent_id": "A-1", "role": "analyst", "supervisor": "team-lead", "status": "suspended"}, h)
assert r["A-1"]["status"] == "suspended" and len(h) == 2
```

## Failure Modes
- Agents are renamed instead of re-registered and their historical record splits across identifiers.
- A supervisor assignment is changed without recording who approved the change.
- Suspended agents remain in the active roster and continue receiving work from schedulers.
- The roster is rebuilt from scratch on each sync and status-change history is lost.
- Roster entries carry no owner so an orphaned agent has no accountable supervisor.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- the SK Telecom governance model assigns agents employee ID numbers, records each agent role and supervisor, and suspends or retires agents after performance reviews (aiagentstore.ai AI Agents News, dated October 30, 2026) ([public signal](https://aiagentstore.ai/ai-agent-news/this-week))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Long Horizon Goal State Resume](long-horizon-goal-state-resume.md)
- [Agent Scope Session Isolation Memory](agent-scope-session-isolation-memory.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
