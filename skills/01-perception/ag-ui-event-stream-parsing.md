---
title: "AG-UI Event Stream Parsing"
category: 01-perception
level: advanced
stability: experimental
description: "Parse AG-UI protocol event streams into typed turn, state-delta, and tool-call events so that frontend agent bindings consume a validated ordered event log rather than raw socket bytes."
added: "2026-10"
version: v1
related: [agent-protocol-message-envelope-parsing, sse-parsing]
tags: [ag-ui, parsing, frontend-agents, event-streams]
---
# AG-UI Event Stream Parsing

## Description
Parse AG-UI protocol event streams into typed turn, state-delta, and tool-call events so that frontend agent bindings consume a validated ordered event log rather than raw socket bytes. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A frontend agent binding consumes AG-UI events and must never act on malformed or out-of-order events.
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
3. Split the stream on event boundaries, validate each event against the AG-UI event schema, and reject the batch on the first unknown or out-of-sequence event before surfacing state to the UI.
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
def parse_event(raw, seen_start):
    kind = raw.get("type")
    if kind == "STATE_DELTA" and not seen_start:
        raise ValueError("delta before RUN_STARTED")
    return {"type": kind, "payload": raw.get("payload", {})}
assert parse_event({"type": "RUN_STARTED"}, False)["type"] == "RUN_STARTED"
```

## Failure Modes
- A STATE_DELTA arrives before its RUN_STARTED boundary and corrupts UI state.
- A TEXT_MESSAGE_CONTENT event is applied after its STOP event, appending orphaned text.
- An unknown event type is silently dropped, hiding protocol version drift from the binding.
- Partial JSON chunks are parsed as complete events and raise downstream type errors.
- Tool-call arguments are surfaced before the ARGUMENTS_DONE event completes them.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- 2026 agent protocol stack coverage lists AG-UI among the frontend agent transport protocols (peterindia.net, dated October 2026) ([public signal](https://www.peterindia.net/AgenticAICommunicationProtocols.html))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Agent Protocol Message Envelope Parsing](../01-perception/agent-protocol-message-envelope-parsing.md)
- [SSE Parsing](../01-perception/sse-parsing.md)

## Changelog
| Version | Date | Notes |
|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
