---
title: "Realtime Voice Event Stream Parsing"
category: 01-perception
level: advanced
stability: experimental
description: "Parse realtime voice-agent event streams so transcript deltas, tool calls, and audio events are read deterministically."
added: "2026-10"
version: v1
related: [sse-parsing, audio-stream-segmentation]
tags: [realtime, voice, parsing, events]
---
# Realtime Voice Event Stream Parsing

## Description
Parse realtime voice-agent event streams so transcript deltas, tool calls, and audio events are read deterministically. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A realtime voice agent runtime must consume its provider event stream and extract transcript deltas and tool-call events without losing ordering.
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
3. Parse the realtime event stream, extract event types, transcript deltas, tool calls, and session lifecycle markers in arrival order, and abort on any event type outside the declared schema.
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
def parse_events(events):
    transcript, calls = [], []
    for event in events:
        if event["type"] == "transcript.delta":
            transcript.append(event["delta"])
        elif event["type"] == "tool.call":
            calls.append(event["name"])
        elif event["type"] == "session.closed":
            break
        else:
            raise ValueError("undeclared realtime event type: " + event["type"])
    return {"transcript": "".join(transcript), "calls": calls}
result = parse_events([
    {"type": "transcript.delta", "delta": "book "},
    {"type": "transcript.delta", "delta": "a table"},
    {"type": "tool.call", "name": "reserve_table"},
    {"type": "session.closed"},
])
assert result == {"transcript": "book a table", "calls": ["reserve_table"]}
```

## Failure Modes
- Transcript deltas are appended out of arrival order and the reconstructed utterance is wrong.
- Unknown event types are skipped silently, so protocol upgrades drop tool calls without any error.
- Session lifecycle events are treated as transcript text and control markers leak into the user-facing transcript.
- Tool-call payloads are parsed without argument validation and malformed calls are dispatched anyway.
- The stream is buffered without a bounded window and a stuck provider pins the parser forever.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- Production guidance for the OpenAI Realtime API voice agents documents the event-stream contract, including transcript deltas and tool events, that clients must parse deterministically (forasoft.com, dated October 2026) ([public signal](https://www.forasoft.com/blog/article/openai-realtime-api-voice-agent-production-guide-2026))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Sse Parsing](../01-perception/sse-parsing.md)
- [Audio Stream Segmentation](../01-perception/audio-stream-segmentation.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
