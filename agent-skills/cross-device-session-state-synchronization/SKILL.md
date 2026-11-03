---
name: cross-device-session-state-synchronization
description: Synchronize agent session state across web, mobile, CLI, IDE, and chat surfaces so any surface can continue the same task from the same state.
metadata:
  source: skills/03-memory/cross-device-session-state-synchronization.md
  category: 03-memory
  version: "v1"
---
# Cross Device Session State Synchronization

## Description
Synchronize agent session state across web, mobile, CLI, IDE, and chat surfaces so any surface can continue the same task from the same state. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A user works with one agent across several surfaces and divergent per-surface state has already caused conflicting instructions or duplicated work.
- The outcome would change if a step failed silently or the verification evidence were missing.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | the per-surface session states, the authoritative state store, and the conflict-resolution rule. |
| Outputs | A structured record with the decision, rejected alternatives, and the verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Designate one authoritative state store and register every surface that may read or write it.
2. Sync each surface's local state to the authoritative store before and after every task step.
3. Apply the declared conflict rule when two surfaces wrote divergent state and record which write won.
4. Verify the next surface reads the post-conflict state and not its stale local copy.
5. On a sync failure, block the write and report the divergent states rather than merging silently.
6. Emit a structured result with the sync log, conflicts, and resolutions.

## Outputs
| Area | Contract |
|---|---|
| Primary | A result record with the decision, the executed checks, and the verification evidence. |
| Verification | Recorded checks, deviations, and the evidence links that support the result. |
| Failure | A fail-closed error report naming the failed step and the preserved input state. |

## Runnable Example
```python
def sync_state(authoritative, local_writes, rule="latest"):
    conflicts = [k for k in local_writes if k in authoritative and local_writes[k] != authoritative[k]]
    merged = dict(authoritative)
    for k, v in local_writes.items():
        merged[k] = v
    return {"merged": merged, "conflicts": conflicts, "rule": rule}
auth = {"task": "draft pr", "step": 3}
w = {"step": 4}
r = sync_state(auth, w); assert r["merged"]["step"] == 4 and r["conflicts"] == ["step"]
```

## Failure Modes
- Each surface keeps a private copy and the stores drift until they contradict.
- Conflicts are merged field by field, producing a state no surface ever wrote.
- A surface reads its stale cache after another surface advanced the task.
- Sync failures are swallowed and the write is applied locally only.
- The authoritative store is a surface itself, so offline edits permanently fork the state.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- GitHub Copilot cloud sessions that follow the user across web, mobile, CLI, VS Code, and Slack or Teams so any surface continues the same work (AI Agent News Today, dated November 2, 2026) ([public signal](https://aiagentstore.ai/ai-agent-news/this-week))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Persistent Context Capture Compression](persistent-context-capture-compression.md)
- [Session Artifact Rehydration](session-artifact-rehydration.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |
