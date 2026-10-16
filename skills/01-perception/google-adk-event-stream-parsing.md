---
title: "Google ADK Event Stream Parsing"
category: 01-perception
level: advanced
stability: experimental
description: "Parse Google Agent Development Kit event streams into typed step records so downstream logic can observe agent progress, tool calls, and errors without depending on framework log formats."
added: "2026-10"
version: v1
related: [agent-trace-span-parsing, api-response-parsing]
tags: [adk, event-streams, parsing]
---
# Google ADK Event Stream Parsing

## Description
Parse Google Agent Development Kit event streams into typed step records so downstream logic can observe agent progress, tool calls, and errors without depending on framework log formats. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- An agent runtime must consume Google ADK 2.0 event streams and react to individual steps rather than whole runs.
- The outcome would change if inputs were stale, ambiguous, or incomplete.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | a captured ADK event stream, a step-record schema, and explicit acceptance criteria for parsed output. |
| Outputs | A structured record with the decision, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the google ADK event stream parsing steps in a bounded, checkpointed way.
4. Compare the actual outcome against the acceptance criteria and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Outputs
| Area | Contract |
|---|---|
| Primary | A list of typed step records with actor, event name, payload keys, and an ordering token for replay. |
| Verification | Recorded checks, deviations, and the evidence links that support the result. |
| Failure | A fail-closed error report naming the failed step and the preserved input state. |

## Runnable Example
```python
def parse_adk_events(events):
    steps = []
    for ev in events:
        steps.append({"actor": ev.get("author"), "name": ev.get("event_type"), "keys": sorted(ev.get("payload", {}))})
    return steps
steps = parse_adk_events([{"author": "agent", "event_type": "tool_call", "payload": {"b": 1, "a": 2}}])
assert steps[0]["keys"] == ["a", "b"]
```

## Failure Modes
- Treating framework log lines as a stable API when ADK versions rename event fields.
- Dropping events that arrive out of order instead of recording an ordering token.
- Silently accepting unknown event types as success records.
- Building tool-call records from truncated payloads without flagging the truncation.
- Reporting a complete parse when stream framing errors remain unhandled.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- Google ADK 2.0 event-based agent runtime surfaced in dated 2026 agent-framework trend coverage. ([public signal](https://www.shakudo.io/blog/top-9-ai-agent-frameworks))
- Cross-framework agent runtime comparison names ADK among the typed agent frameworks of fall 2026. ([public signal](https://vdf.ai/blog/best-ai-agent-frameworks/))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [agent trace span parsing](../01-perception/agent-trace-span-parsing.md)
- [api response parsing](../01-perception/api-response-parsing.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |

