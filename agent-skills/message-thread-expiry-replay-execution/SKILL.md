---
name: message-thread-expiry-replay-execution
description: Execute full-conversation replay when a message thread is expired or not found, restoring session progress without loss.
metadata:
  source: skills/04-action-execution/message-thread-expiry-replay-execution.md
  category: 04-action-execution
  version: "v1"
---

# Message Thread Expiry Replay Execution

## Description
Execute full-conversation replay when a message thread is expired or not found, restoring session progress without loss. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A provider thread event marks the session thread dead mid-task.
- The outcome would change if the agent restarted the task from scratch on thread loss.
- The result must prove the replayed history matches the client mirror.

## Inputs
| Area | Contract |
|---|---|
| Inputs | The dead thread verdict, the client history mirror, and the provider replay API contract. |
| Outputs | A new active thread with the full replayed history and continuation point. |
| Safety | Failures must fail closed by halting the task rather than continuing on partial history. |

## Procedure
1. Confirm the thread dead verdict before composing any replay.
2. Rebuild the full history payload from the client mirror in original order.
3. Create a new thread and submit the replayed history as a single submission.
4. Verify the provider acknowledgment covers every replayed message sequence.
5. Bind the new thread identifier to the session and mark continuation points.
6. Emit the replay report linking old and new thread identifiers with message counts.

## Outputs
| Area | Contract |
|---|---|
| Primary | A replay report naming the new thread, replayed message count, and continuation point. |
| Verification | Recorded acknowledgment checks that prove the mirror was fully replayed. |
| Failure | A fail-closed halt naming the unreplayed prefix and preserved mirror state. |

## Runnable Example
```python
def replay(mirror, dead_tid):
    assert mirror.get(dead_tid), 'no mirror for dead thread'
    history = mirror[dead_tid]
    new_tid = 'new-' + dead_tid
    ack = {'tid': new_tid, 'count': len(history)}
    assert ack['count'] == len(history), 'partial replay acknowledged'
    return {'new_tid': new_tid, 'replayed': ack['count'], 'continuation': len(history)}
r = replay({'t1': ['a', 'b', 'c']}, 't1')
assert r['new_tid'] == 'new-t1' and r['replayed'] == 3
```

## Failure Modes
- The replay is composed from the thread's server-side state, which no longer exists.
- A partial acknowledgment is accepted and the task continues from the middle.
- The dead verdict is not confirmed, so an active thread is replayed into a duplicate.
- The continuation point is recorded before the acknowledgment check passes.
- Replay failures fall back to a fresh session, silently losing all history.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- Anthropic's Message Threads beta requires handling thread expirations with a robust client copy and full replay of conversation history when a thread is refused or not found (AI Agent News Today, dated November 3, 2026) ([public signal](https://aiagentstore.ai/ai-agent-news/this-week))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Idempotent Retries](idempotent-retries.md)
- [Durable Resume After Provider Restart](durable-resume-after-provider-restart.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |
