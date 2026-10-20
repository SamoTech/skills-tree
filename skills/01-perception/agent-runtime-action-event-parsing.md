---
title: "Agent Runtime Action Event Parsing"
category: 01-perception
level: advanced
stability: experimental
description: "Parse runtime action events from agent platforms into typed records so downstream consumers can replay and audit what the agent actually did."
added: "2026-10"
version: v1
related: [agent-protocol-message-envelope-parsing, agent-trace-span-parsing]
tags: [event-parsing, agent-runtime, audit, replay]
---
# Agent Runtime Action Event Parsing

## Description
Parse runtime action events from agent platforms into typed records so downstream consumers can replay and audit what the agent actually did. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A platform emits action events for a long-running agent task and the action history must be reconstructed without guessing.
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
3. Normalize the event stream into typed action records keyed by task and turn, validate each event against the pinned platform schema version, and flag gaps, duplicates, or out-of-order entries in the emitted record.
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
def fold_events(events):
    out = {}
    for e in sorted(events, key=lambda e: e["seq"]):
        out.setdefault(e["task"], []).append(e["action"])
    return out
h = fold_events([{"seq": 2, "task": "t", "action": "write"}, {"seq": 1, "task": "t", "action": "read"}])
assert h["t"] == ["read", "write"]
```

## Failure Modes
- Events are consumed in arrival order and reordered deliveries corrupt the action history.
- The event schema version is not pinned and later breaking changes silently misparse fields.
- Partial or malformed events are dropped without recording the loss.
- Action events from unrelated tasks are merged into one history.
- The parsed record omits timing and cannot support later replay.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- 2026 Notion ships an agent harness able to run single agent tasks for more than 24 hours, making runtime action event records a durable need (notion.com, dated October 2026) ([public signal](https://www.notion.com/blog/notion-ai-more-for-less))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Agent Protocol Message Envelope Parsing](../01-perception/agent-protocol-message-envelope-parsing.md)
- [Agent Trace Span Parsing](../01-perception/agent-trace-span-parsing.md)

## Changelog
| Version | Date | Notes |
|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
