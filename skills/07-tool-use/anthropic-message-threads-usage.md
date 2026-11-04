---
title: "Anthropic Message Threads Usage"
category: 07-tool-use
level: advanced
stability: experimental
description: "Use the Messages API thread feature to send conversation once and only new messages afterward, within its eligibility limits."
added: "2026-11"
version: v1
related: [anthropic-api, api-version-pinning]
tags: [tool-use, message-threads, api, sessions]
---
# Anthropic Message Threads Usage

## Description
Use the Messages API thread feature to send conversation once and only new messages afterward, within its eligibility limits. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- An agent makes very long multi-turn requests where resending full history dominates latency.
- The outcome would change if threads were used where they are ineligible, such as zero-retention workflows.
- The result must record the thread lifecycle and the client mirror state.

## Inputs
| Area | Contract |
|---|---|
| Inputs | The Messages API request stream, the thread beta contract, and the eligibility policy. |
| Outputs | Thread-bound sends with only-new-message payloads and lifecycle records. |
| Safety | Failures must fail closed by full-history send when eligibility or the thread is uncertain. |

## Procedure
1. Check the workflow eligibility against the thread contract exclusions first.
2. Send the first request with full history and capture the returned thread identifier.
3. Send subsequent requests with only new messages plus the thread identifier.
4. Handle expiry and not-found by replaying from the client mirror.
5. Never assume token billing changed; account for the full history in cost models.
6. Record thread lifecycle events and mirror reconciliation for every session.

## Outputs
| Area | Contract |
|---|---|
| Primary | Thread-bound sends with per-turn new-message payloads and lifecycle records. |
| Verification | Recorded eligibility checks and mirror reconciliation supporting the session. |
| Failure | A fail-closed fallback to full-history send with the eligibility failure named. |

## Runnable Example
```python
def send(state, msg):
    if not state.get('eligible'):
        return {'payload': state['history'] + [msg], 'mode': 'full'}
    if state.get('thread') is None:
        state['thread'] = 't-' + str(len(state['history']))
        return {'payload': state['history'] + [msg], 'mode': 'initial'}
    return {'payload': [msg], 'mode': 'threaded', 'tid': state['thread']}
st = {'history': ['a', 'b'], 'eligible': True}
s1 = send(st, 'c'); s2 = send(st, 'd')
assert s1['mode'] == 'initial' and s2['mode'] == 'threaded' and s2['payload'] == ['d']
```

## Failure Modes
- Threads are used for a zero-data-retention workflow despite the eligibility exclusion.
- Cost models are updated as if payload size reduction lowers billed tokens.
- The thread identifier is stored in ephemeral state and lost on restart.
- Not-found responses are retried with the same dead thread instead of replaying.
- The eligibility check runs once per deployment and is skipped per session.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- Anthropic opened the Message Threads beta in the Messages API so agents send the full conversation once and thereafter only new messages, reporting median time-to-first-token drops of about 35 percent on 500k to 1M token requests (AI Agent News Today, dated November 3, 2026) ([public signal](https://aiagentstore.ai/ai-agent-news/this-week))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Anthropic Api](anthropic-api.md)
- [Api Version Pinning](api-version-pinning.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |
