---
name: agent-session-rewind-state-capture
description: Capture and restore conversation state snapshots so an agent session can rewind to a prior point and continue from consistent context.
metadata:
  source: skills/03-memory/agent-session-rewind-state-capture.md
  category: 03-memory
  version: "v1"
---

# Agent Session Rewind State Capture

## Description
Capture and restore conversation state snapshots so an agent session can rewind to a prior point and continue from consistent context. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A long agent session must be rewound to an earlier conversation point without losing durable state.
- Divergent branches from a rewound point must remain traceable.
- Restores must be verified rather than assumed consistent.

## Inputs
| Area | Contract |
|---|---|
| Inputs | The session event log, the snapshot schedule, and the restore policy. |
| Outputs | A rewind verdict naming the target snapshot, the restored context, and the branch identifier for continued work. |
| Safety | Fail closed by refusing a restore when the target snapshot is incomplete or corrupted. |

## Procedure
1. Record the session event log against the declared snapshot schedule.
2. Validate each snapshot's completeness before it becomes a restore target.
3. On rewind, locate the last valid snapshot at or before the requested point.
4. Rebuild the conversation context from the snapshot and verify it against the log.
5. Mint a new branch identifier so post-rewind work stays traceable.
6. Emit the rewind verdict with restored context and branch identifier.

## Outputs
| Area | Contract |
|---|---|
| Primary | A rewind verdict naming the target snapshot, the restored context, and the branch identifier for continued work. |
| Verification | Snapshot hashes and event-log checks that reproduce the restored context. |
| Failure | A fail-closed error naming the incomplete snapshot and the refused restore. |

## Runnable Example
```python
def rewind(log, snapshots, target_ts):
    valid = [s for s in snapshots if s["complete"] and s["ts"] <= target_ts]
    if not valid:
        return {"ok": False, "reason": "no_valid_snapshot"}
    snap = valid[-1]
    replayed = [e for e in log if e["ts"] <= snap["ts"]]
    return {"ok": True, "restored": snap["id"], "events": len(replayed), "branch": snap["id"] + "-b"}

log = [{"ts": 1}, {"ts": 2}, {"ts": 3}]
snaps = [{"id": "s1", "ts": 2, "complete": True}]
r = rewind(log, snaps, 2)
assert r["ok"] and r["events"] == 2 and r["branch"] == "s1-b"
assert rewind(log, [{"id": "s0", "ts": 1, "complete": False}], 2)["ok"] is False
```

## Failure Modes
- Snapshots are trusted without completeness validation.
- Rewind restores a snapshot but keeps the pre-rewind context mixed in.
- Post-rewind work overwrites the original branch instead of minting a new one.
- Snapshot schedule gaps leave no valid restore target undetected.
- Restored context is not verified against the event log.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- Nous Research's Hermes Agent v0.23.0 adds /rewind for conversation navigation alongside its unified gateway surfaces (HeadsUpAI, November 6, 2026) ([public signal](https://headsupai.io/ai-news-and-updates/today))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [A2a Conversation Context Continuity Memory](a2a-conversation-context-continuity-memory.md)
- [Agent Attributed Action History Memory](agent-attributed-action-history-memory.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |
