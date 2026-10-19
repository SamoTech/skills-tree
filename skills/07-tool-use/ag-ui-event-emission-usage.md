---
title: "AG-UI Event Emission Usage"
category: 07-tool-use
level: advanced
stability: experimental
description: "Emit AG-UI protocol events from an agent backend so that frontend clients receive valid, ordered event streams with declared lifecycle boundaries."
added: "2026-10"
version: v1
related: [ag-ui-event-stream-parsing, streaming-tool-output]
tags: [ag-ui, events, backend, protocols]
---
# AG-UI Event Emission Usage

## Description
Emit AG-UI protocol events from an agent backend so that frontend clients receive valid, ordered event streams with declared lifecycle boundaries. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- An agent backend must serve AG-UI frontends with correct event sequencing.
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
3. Implement the event emitter against the AG-UI lifecycle schema, enforce start and stop boundaries around every run, and validate the emitted stream against the schema before release.
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
def emit(events, state):
    if events[0]["type"] != "RUN_STARTED" or events[-1]["type"] != "RUN_FINISHED":
        raise ValueError("lifecycle boundary violation")
    return events
assert emit([{"type": "RUN_STARTED"}, {"type": "RUN_FINISHED"}], {}) is not None
```

## Failure Modes
- A RUN_STARTED is emitted twice and clients reset mid-run and lose state..
- Tool-call events are emitted without argument boundaries and clients render partial JSON..
- An error path skips RUN_ERROR and clients wait on a stream that already died..
- State deltas are emitted before the snapshot they patch, corrupting client state..
- Event ordering relies on transport guarantees that streaming transports do not provide..

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- 2026 agent protocol stack coverage documents AG-UI event contracts between agents and frontends (peterindia.net, dated October 2026) ([public signal](https://www.peterindia.net/AgenticAICommunicationProtocols.html))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [AG-UI Event Stream Parsing](../01-perception/ag-ui-event-stream-parsing.md)
- [Streaming Tool Output](../07-tool-use/streaming-tool-output.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
