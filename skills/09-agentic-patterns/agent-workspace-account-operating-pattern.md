---
title: "Agent Workspace Account Operating Pattern"
category: 09-agentic-patterns
level: advanced
stability: experimental
description: "Operate an agent as a first-class workspace account with its own identity, email, context, and attributed audit trail so every action is distinguishable from human colleagues' work."
added: "2026-10"
version: v1
related: [agent-handoffs, agent-observability-tracing]
tags: [agent, workspace, account, operating]
---
# Agent Workspace Account Operating Pattern

## Description
Operate an agent as a first-class workspace account with its own identity, email, context, and attributed audit trail so every action is distinguishable from human colleagues' work. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- An organization wants an agent to be reachable and accountable like a coworker without borrowing human identities.
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
3. Provision the agent its own account, bind every action to that account id in the audit trail, and reject unattributed entries before they reach downstream systems.
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
def attribute_action(entry, actor):
    if not entry.get("actor_id"):
        raise ValueError("unattributed action")
    return {"actor_type": actor, "actor_id": entry["actor_id"], "action": entry["action"]}
a = attribute_action({"actor_id": "agent:assign-01", "action": "book_room"}, "agent")
assert a["actor_type"] == "agent"
```

## Failure Modes
- The agent shares a human account and its actions land in that person's audit history.
- Attribution exists but downstream systems re-map agent actions to the human owner.
- The account is provisioned without scoped permissions and inherits the delegator's access.
- Colleagues reply to the agent's thread believing it is a person and attribution is never surfaced.
- The audit trail records the agent only at session start and mid-session actions are unattributed.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- Google's Gemini agent operating with its own Workspace account, email address, and attributed audit trail is the dated public signal for this pattern contract. ([public signal](https://techcrunch.com/2026/10/08/google-brings-agentic-ai-to-gemini-starting-with-businesses/))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Agent Handoffs](../09-agentic-patterns/agent-handoffs.md)
- [Agent Observability Tracing](../09-agentic-patterns/agent-observability-tracing.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
