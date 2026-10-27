---
title: "Agent Attributed Action History Memory"
category: 03-memory
level: advanced
stability: experimental
description: "Retain an append-only action history that attributes every recorded action to a specific human or agent identity so audit reviews never misattribute agent work to a person."
added: "2026-10"
version: v1
related: [permission-grant-history-memory, agent-sessions]
tags: [agent, attributed, action, history]
---
# Agent Attributed Action History Memory

## Description
Retain an append-only action history that attributes every recorded action to a specific human or agent identity so audit reviews never misattribute agent work to a person. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- An audit review must reconstruct who did what when the actor may be either a human or an agent account.
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
3. Append every action with an explicit actor id and a monotonic sequence number, and reject any entry that arrives without an actor id.
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
def record_action(store, actor_id, action):
    store.append({"actor": actor_id, "action": action, "seq": len(store)})
    return store
s = []
record_action(s, "agent:gemini-hr-01", "send_onboarding_email")
record_action(s, "human:dana", "approve")
assert [e["actor"] for e in s] == ["agent:gemini-hr-01", "human:dana"] and s[1]["seq"] == 1
```

## Failure Modes
- Actions are recorded under the human owner of the agent and agent work is invisible in audits.
- The store allows edits and a mid-history action is silently rewritten.
- Sequence numbers are reused and the ordering of two actions cannot be reconstructed.
- Entries without an actor id are accepted and later attributed by guessing.
- The history is trimmed for cost and an old escape-relevant action is gone when auditors ask.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- The Gemini agent's audit trail attributed to the agent's own account rather than to a person is the dated public signal for this memory contract. ([public signal](https://techcrunch.com/2026/10/08/google-brings-agentic-ai-to-gemini-starting-with-businesses/))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Permission Grant History Memory](../03-memory/permission-grant-history-memory.md)
- [Agent Sessions](../03-memory/agent-sessions.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
