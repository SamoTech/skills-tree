---
title: "OpenAI Agents API Stream Item Parsing"
category: 01-perception
level: advanced
stability: experimental
description: "Parse OpenAI Agents API streaming items so tool calls, deltas, and reasoning summaries are consumed in deterministic order."
added: "2026-10"
version: v1
related: [sse-parsing, api-response-parsing]
tags: [openai, agents-api, streaming, parsing]
---
# OpenAI Agents API Stream Item Parsing

## Description
Parse OpenAI Agents API streaming items so tool calls, deltas, and reasoning summaries are consumed in deterministic order. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- An agent host consumes the OpenAI Agents API streaming event stream and must order items before rendering or acting.
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
3. Reorder the stream into per-turn sequences keyed by item id and sequence number, verify each turn starts with a start item, and flag incomplete turns instead of emitting them.
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
def order_items(items):
    by_turn = {}
    for it in items:
        by_turn.setdefault(it["turn"], []).append((it["seq"], it["kind"]))
    return {t: [k for _, k in sorted(v)] for t, v in by_turn.items()}
stream = [{"turn": 1, "seq": 2, "kind": "delta"}, {"turn": 1, "seq": 1, "kind": "start"}]
assert order_items(stream) == {1: ["start", "delta"]}
```

## Failure Modes
- Items are consumed in arrival order and turns are interleaved across streams.
- Sequence gaps are ignored and turns render incomplete output.
- Reasoning items are treated as tool outputs and trigger actions.
- Item ids are not correlated across chunks and turns are duplicated.
- Transport keepalive items are parsed as content events.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- OpenAI DevDay 2026 introduced new Agents API surfaces for building agents (InfoQ recap, dated October 2, 2026) ([public signal](https://www.infoq.com/news/2026/10/openai-devday-2026/))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Sse Parsing](../01-perception/sse-parsing.md)
- [Api Response Parsing](../01-perception/api-response-parsing.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
