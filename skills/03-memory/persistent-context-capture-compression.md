---
title: "Persistent Context Capture Compression"
category: 03-memory
level: advanced
stability: experimental
description: "Capture what an agent does across sessions and compress it into persistent context that survives restarts without unbounded growth."
added: "2026-11"
version: v1
related: [session-artifact-rehydration, cross-device-session-state-synchronization]
tags: [memory, compression, persistence, sessions]
---
# Persistent Context Capture Compression

## Description
Capture what an agent does across sessions and compress it into persistent context that survives restarts without unbounded growth. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- An agent loses useful state between sessions and re-learns the same facts, or its saved context grows until it stops fitting the budget.
- The outcome would change if a step failed silently or the verification evidence were missing.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | the session activity stream, the retention policy with compression ratios, and the rehydration consumer contract. |
| Outputs | A structured record with the decision, rejected alternatives, and the verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Capture session activity as discrete events with timestamps and scope tags.
2. Compress closed sessions into summaries that preserve decisions, facts, and open items.
3. Enforce the retention policy by evicting or archiving summaries outside the active window.
4. Verify each compressed summary still answers the recorded key questions for the next session.
5. On a compression that drops a key fact, fail closed and keep the raw capture for review.
6. Emit a structured result with the compressed context, its size, and the verification evidence.

## Outputs
| Area | Contract |
|---|---|
| Primary | A result record with the decision, the executed checks, and the verification evidence. |
| Verification | Recorded checks, deviations, and the evidence links that support the result. |
| Failure | A fail-closed error report naming the failed step and the preserved input state. |

## Runnable Example
```python
def compress_session(events, keep=("decision", "fact", "open_item")):
    summary = [e for e in events if e["kind"] in keep]
    if len(summary) == 0 and len(events) > 0:
        return {"ok": False, "reason": "compression dropped all content"}
    return {"ok": True, "summary": summary, "ratio": len(summary) / max(len(events), 1)}
ev = [{"kind": "decision", "t": "use postgres"}, {"kind": "noise", "t": "typing"}]
c = compress_session(ev); assert c["ok"] is True and c["summary"][0]["t"] == "use postgres"
assert compress_session([{"kind": "noise", "t": "x"}])["ok"] is False
```

## Failure Modes
- Captured context grows without eviction and eventually breaks the session budget.
- Compression silently drops decisions or open items that later sessions needed.
- Raw captures are kept forever with no retention policy and become a liability store.
- Summaries are never verified against key questions before being committed.
- Restarts load compressed context that contradicts the raw activity record.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- claude-mem providing persistent context across sessions for every agent by capturing what the agent does and compressing it (Munder Difflin agent-tools daily, dated November 1, 2026) ([public signal](https://munderdiffl.in/blog/agent-tools-today-2026-11-01/))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Session Artifact Rehydration](session-artifact-rehydration.md)
- [Cross Device Session State Synchronization](cross-device-session-state-synchronization.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |
