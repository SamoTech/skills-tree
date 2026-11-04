---
title: "Message Thread Lifecycle Event Parsing"
category: 01-perception
level: advanced
stability: experimental
description: "Parse message-thread lifecycle events such as creation, expiry, and not-found responses into session state decisions."
added: "2026-11"
version: v1
related: [sse-parsing, incremental-json-parsing]
tags: [perception, message-threads, lifecycle, parsing]
---
# Message Thread Lifecycle Event Parsing

## Description
Parse message-thread lifecycle events such as creation, expiry, and not-found responses into session state decisions. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A long-session agent must detect thread expiry from provider events before the next send.
- The outcome would change if a not-found response were treated as a transport error.
- The result must be recorded with the thread identifier for replay decisions.

## Inputs
| Area | Contract |
|---|---|
| Inputs | The provider event stream or error payload, the thread identifier, and the expiry policy. |
| Outputs | A lifecycle verdict naming the event type and the required client action. |
| Safety | Failures must fail closed with the raw payload preserved for replay. |

## Procedure
1. Extract the event type and thread identifier from each payload before interpretation.
2. Classify the event into created, active, expiring, expired, or not-found.
3. Record remaining inactivity budget when the provider reports it.
4. Map each non-active verdict to its required client action from the policy table.
5. Preserve the raw payload for any verdict that requires replay.
6. Emit the verdict with the thread identifier and the mapped action.

## Outputs
| Area | Contract |
|---|---|
| Primary | A lifecycle verdict naming the event type, remaining budget, and the required client action. |
| Verification | Recorded event classification and preserved payloads that support the verdict. |
| Failure | A fail-closed error report naming the unrecognized event and preserved payload. |

## Runnable Example
```python
def classify(event):
    t = event['type']
    if t == 'thread.created':
        return {'state': 'active', 'action': 'send-new-messages-only'}
    if t in ('thread.expired', 'thread.not_found'):
        return {'state': 'dead', 'action': 'replay-full-history'}
    raise ValueError('unrecognized event: ' + t)
r = classify({'type': 'thread.not_found', 'thread_id': 't1'})
assert r['state'] == 'dead' and r['action'] == 'replay-full-history'
```

## Failure Modes
- A not-found error is classified as a transient transport error and retried on the dead thread.
- Expiry events with remaining budget are treated as already dead, dropping valid sends.
- The raw payload is discarded after classification, blocking later replay.
- Event types from a newer API version are forced into the closest known class.
- Thread identifiers are read from a different field than the one recorded.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- Anthropic opened the Message Threads beta so agents send full conversation once and thereafter only new messages, adding thread lifecycle events with expiry and not-found handling (AI Agent News Today, dated November 3, 2026) ([public signal](https://aiagentstore.ai/ai-agent-news/this-week))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Sse Parsing](sse-parsing.md)
- [Incremental Json Parsing](incremental-json-parsing.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |
