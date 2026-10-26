---
title: "Channel Conversation State Continuity Memory"
category: 03-memory
level: advanced
stability: experimental
description: "Maintain conversation state continuity for one agent served across channel packages such as OpenAI Responses, Telegram, A2A, and MCP."
added: "2026-10"
version: v1
related: [cross-thread-memory, dialogue-state-tracking]
tags: [channel, conversation, state, continuity, memory]
---
# Channel Conversation State Continuity Memory

## Description
Maintain conversation state continuity for one agent served across channel packages such as OpenAI Responses, Telegram, A2A, and MCP. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- An operator needs this capability to proceed safely and verifiably.
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
3. Bind each inbound message to a channel identity and a shared conversation key, replay the declared state window on channel switch, and reject state writes that would fork the conversation.
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
def route_state(events, conv_key):
    state = {"conv": conv_key, "turns": []}
    for e in events:
        if e["conv"] != conv_key:
            raise ValueError("cross-conversation write blocked")
        state["turns"].append((e["channel"], e["turn_id"]))
    return state

ev = [{"conv":"c1","channel":"telegram","turn_id":1},{"conv":"c1","channel":"a2a","turn_id":2}]
out = route_state(ev, "c1")
assert len(out["turns"]) == 2 and out["turns"][1][0] == "a2a"
```

## Failure Modes
- Each channel keeps a private history and the agent repeats or contradicts itself across channels.
- Channel user IDs are used as conversation keys and two users collide.
- State replays the full history on every switch and the token cost grows without bound.
- A failed state write forks the conversation and two branches diverge silently.
- Turn IDs are channel-local and the replay order is reconstructed incorrectly.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- Microsoft Agent Framework channel packages for OpenAI Responses, Telegram, A2A, and MCP hosting are documented in an October framework review (developersdigest.tech, dated October 24, 2026) ([public signal](https://www.developersdigest.tech/blog/microsoft-agent-framework-whats-new-2026))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Cross-thread Memory](../03-memory/cross-thread-memory.md)
- [Dialogue State Tracking](../03-memory/dialogue-state-tracking.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
