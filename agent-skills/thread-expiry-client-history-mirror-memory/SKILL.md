---
name: thread-expiry-client-history-mirror-memory
description: Keep a client-side mirror of conversation history so a dead or expired message thread can be replayed without data loss.
metadata:
  source: skills/03-memory/thread-expiry-client-history-mirror-memory.md
  category: 03-memory
  version: "v1"
---

# Thread Expiry Client History Mirror Memory

## Description
Keep a client-side mirror of conversation history so a dead or expired message thread can be replayed without data loss. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A long agent session depends on a provider-side thread that can expire or be lost.
- The outcome would change if replay needed history the client never kept.
- The result must keep the mirror bounded and reconciled with the thread.

## Inputs
| Area | Contract |
|---|---|
| Inputs | The outbound message stream, the thread identifier, and the mirror retention budget. |
| Outputs | A reconciled client history mirror keyed by thread with replay readiness. |
| Safety | Failures must fail closed by blocking sends until the mirror is consistent. |

## Procedure
1. Append every outbound message to the mirror keyed by thread identifier.
2. Reconcile the mirror against thread acknowledgment events on receipt.
3. Mark threads expired or not-found as requiring replay from the mirror.
4. Rebuild the replay payload from the mirror on the replay decision.
5. Bound the mirror by the retention budget, trimming from the oldest acked prefix.
6. Emit the mirror state with per-thread replay readiness before the next send.

## Outputs
| Area | Contract |
|---|---|
| Primary | A per-thread client history mirror with acknowledgment state and replay readiness. |
| Verification | Recorded reconciliation events and trim decisions that reproduce the mirror state. |
| Failure | A fail-closed block naming the inconsistent thread and missing acknowledgment. |

## Runnable Example
```python
class ThreadMirror:
    def __init__(self):
        self.hist = {}
    def send(self, tid, msg):
        self.hist.setdefault(tid, []).append(msg)
        return {'tid': tid, 'seq': len(self.hist[tid])}
    def replay(self, tid):
        assert tid in self.hist, 'no mirror for thread'
        return list(self.hist[tid])
m = ThreadMirror(); m.send('t1', 'a'); m.send('t1', 'b')
assert m.replay('t1') == ['a', 'b']
```

## Failure Modes
- The mirror is trimmed before acknowledgment, cutting the replayable prefix.
- Expired threads are marked replayable while their mirror was never reconciled.
- Replay payloads are rebuilt from a stale copy captured before the last messages.
- The retention budget silently grows until the client store exhausts.
- Mirror writes happen after the send, so a crash between them loses the message.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- Anthropic's Message Threads beta keeps threads in encrypted memory that expire after inactivity, so agents must keep a robust client copy of conversation history to handle expirations (AI Agent News Today, dated November 3, 2026) ([public signal](https://aiagentstore.ai/ai-agent-news/this-week))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Context Compaction](context-compaction.md)
- [Session Artifact Rehydration](session-artifact-rehydration.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |

