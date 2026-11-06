---
title: "Agent Playbook Reuse Memory"
category: 03-memory
level: advanced
stability: experimental
description: "Store, version, and retrieve agent playbooks so repeated task sequences reuse recorded procedures instead of being re-derived."
added: "2026-11"
version: v1
related: [agent-attributed-action-history-memory, active-recall-memory-curation]
tags: [memory, playbooks, reuse, versioning]
---

# Agent Playbook Reuse Memory

## Description
Store, version, and retrieve agent playbooks so repeated task sequences reuse recorded procedures instead of being re-derived. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- The same multi-step task keeps being re-planned from scratch.
- Playbooks must be versioned so reuse is traceable to a recorded procedure.
- Stale playbooks must be detected before reuse.

## Inputs
| Area | Contract |
|---|---|
| Inputs | The playbook library, the task signature, and the reuse policy. |
| Outputs | A reuse decision naming the matched playbook version, its recorded outcomes, and any staleness flags. |
| Safety | Fail closed by refusing reuse when the matched playbook is stale or its outcomes are unverified. |

## Procedure
1. Compute the task signature from the incoming task description.
2. Match the signature against the playbook library and its version history.
3. Check the matched playbook's recorded outcomes and last-verified date.
4. Flag the playbook as stale when its verification predates relevant environment changes.
5. Fall back to fresh planning when no verified playbook matches.
6. Emit the reuse decision with the playbook version and verification state.

## Outputs
| Area | Contract |
|---|---|
| Primary | A reuse decision naming the matched playbook version, its recorded outcomes, and any staleness flags. |
| Verification | Version identifiers and outcome records that reproduce the reuse decision. |
| Failure | A fail-closed decision that falls back to fresh planning with the reason recorded. |

## Runnable Example
```python
def reuse(library, sig, today, stale_after_days=30):
    hits = [p for p in library if p["sig"] == sig]
    if not hits:
        return {"ok": True, "reused": False, "reason": "no_match"}
    p = hits[-1]
    if (today - p["verified"]) > stale_after_days:
        return {"ok": True, "reused": False, "reason": "stale", "version": p["ver"]}
    return {"ok": True, "reused": True, "version": p["ver"]}

lib = [{"sig": "weekly-report", "ver": "v3", "verified": 100}]
assert reuse(lib, "weekly-report", 120)["reused"] is True and reuse(lib, "weekly-report", 120)["version"] == "v3"
assert reuse(lib, "weekly-report", 200)["reused"] is False
assert reuse(lib, "other", 100)["reason"] == "no_match"
```

## Failure Modes
- Playbooks are reused without checking their last-verified date.
- Version history is dropped, so reuse cannot be traced to outcomes.
- Stale playbooks are preferred because they match faster.
- Task signatures are compared loosely, causing wrong-playbook reuse.
- Fresh planning results are never recorded back into the library.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- Redis announced six new capabilities for Redis Iris, its real-time context engine for AI agents, including playbooks for reusable procedures (AI Agent News Today, November 6, 2026) ([public signal](https://aiagentstore.ai/ai-agent-news/daily/2026-11-06))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Agent Attributed Action History Memory](agent-attributed-action-history-memory.md)
- [Active Recall Memory Curation](active-recall-memory-curation.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |

