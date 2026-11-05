---
title: "MCP Events Spec Tool Usage"
category: 07-tool-use
level: advanced
stability: experimental
description: "Adopt the proposed MCP Events specification for server-to-client event flows with explicit event schemas and ordering rules."
added: "2026-11"
version: v1
related: [mcp-extensions-authoring, mcp-resource-subscription-authoring]
tags: [tools, mcp, events, spec]
---
# MCP Events Spec Tool Usage

## Description
Adopt the proposed MCP Events specification for server-to-client event flows with explicit event schemas and ordering rules. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- An MCP server needs to push events to clients beyond tool results.
- The proposed MCP Events specification covers the flow.
- Event consumers must tolerate spec-version negotiation.

## Inputs
| Area | Contract |
|---|---|
| Inputs | The event catalog, the client capability declaration, and the transport session. |
| Outputs | An events stream naming each emitted event, its sequence number, and schema verdict. |
| Safety | Fail closed by disabling event flow when the client does not declare events capability. |

## Procedure
1. Declare the server events capability with the spec version supported.
2. Negotiate the events capability during client connection.
3. Emit only catalog-declared events with schema-valid payloads.
4. Apply the spec ordering rules for per-session event streams.
5. Handle ordering violations by closing the session, not by resyncing silently.
6. Record emitted events with sequence numbers for audit.

## Outputs
| Area | Contract |
|---|---|
| Primary | An events stream naming each emitted event, its sequence number, and schema verdict. |
| Verification | Recorded sequence numbers and schema checks that reproduce the stream. |
| Failure | A fail-closed disabled-flow report naming the missing client capability. |

## Runnable Example
```python
def emit_event(state, name, payload, client_caps):
    if "events" not in client_caps:
        return {"sent": False, "reason": "no-capability"}
    seq = state["seq"] + 1
    state["seq"] = seq
    return {"sent": True, "seq": seq, "event": name, "payload": payload}
st = {"seq": 0}
assert emit_event(st, "job-done", {}, {})["sent"] is False
r = emit_event(st, "job-done", {}, {"events"})
assert r["sent"] and r["seq"] == 1
```

## Failure Modes
- Events are emitted to clients that never declared the capability.
- Undeclared ad-hoc events are sent alongside cataloged ones.
- Sequence numbers reset silently after a reconnect.
- Ordering violations are resynced without closing the session.
- The events stream is enabled without spec-version negotiation.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- OpenAI DevDay 2026 announced support for the proposed MCP Events specification in the ChatGPT platform (OpenAI DevDay 2026 Recap, dated November 5, 2026) ([public signal](https://openai.com/index/devday-2026-recap/))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [MCP Extensions Authoring](mcp-extensions-authoring.md)
- [MCP Resource Subscription Authoring](mcp-resource-subscription-authoring.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |
