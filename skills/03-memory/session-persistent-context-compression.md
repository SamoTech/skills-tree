---
title: "Session Persistent Context Compression"
category: 03-memory
level: advanced
stability: experimental
description: "Compress captured agent activity into a persistent context store and inject only the relevant parts into later sessions with provenance."
added: "2026-11"
version: v1
related: [cloud-agent-session-state-scoping, automation-outcome-learning-memory]
tags: [memory, context, compression, sessions]
---

# Session Persistent Context Compression

## Description
Compress captured agent activity into a persistent context store and inject only the relevant parts into later sessions with provenance. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- Agent work spans sessions and later sessions need prior activity without replaying full transcripts.
- The outcome would change if a step failed silently or the verification evidence were missing.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | the captured activity stream, the compression method, and the relevance keys and injection triggers. |
| Outputs | A structured record with the decision, rejected alternatives, and the verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Declare what activity is captured, how it is compressed, and what triggers injection into a later session.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Capture and compress the session activity and index it by relevance key with provenance for every entry.
4. Compare the injected context against the acceptance criteria and record deviations.
5. On compression failure or missing provenance, fall back to full replay or discard the entry, and never inject untraceable context.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Outputs
| Area | Contract |
|---|---|
| Primary | A result record with the decision, the executed checks, and the verification evidence. |
| Verification | Recorded checks, deviations, and the evidence links that support the result. |
| Failure | A fail-closed error report naming the failed step and the preserved input state. |

## Runnable Example
```python
def inject(store, key):
    hits = [e for e in store if e["key"] == key and e.get("origin")]
    return {"injected": len(hits), "untraceable_removed": len([e for e in store if not e.get("origin")])}
r = inject([{"key": "api", "origin": "s1"}, {"key": "api"}], "api")
assert r["injected"] == 1 and r["untraceable_removed"] == 1
```

## Failure Modes
- Compressed context is injected without provenance so statements cannot be traced to their origin session.
- Compression silently drops critical facts because only average relevance was measured.
- The relevance filter is never tested so injections miss known-needed context.
- Entire histories are injected because the relevance key was never declared.
- Capture gaps between sessions go unnoticed and the store is treated as complete.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- claude-mem providing persistent context across sessions for every agent by capturing what the agent does, compressing that with AI, and injecting the relevant parts into later sessions (Munder Difflin agent-tools daily brief, dated November 1, 2026) ([public signal](https://munderdiffl.in/blog/agent-tools-today-2026-11-01/))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Cloud Agent Session State Scoping](cloud-agent-session-state-scoping.md)
- [Automation Outcome Learning Memory](automation-outcome-learning-memory.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |
