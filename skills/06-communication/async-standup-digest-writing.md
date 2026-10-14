---
title: "Async Standup Digest Writing"
category: 06-communication
level: advanced
stability: experimental
description: "Compile distributed-team activity into asynchronous standup digests with per-person progress, plans, and blockers."
added: "2026-10"
version: v1
related: [stakeholder-status-updates, meeting-notes, cross-timezone-async-communication]
tags: [async, standup, digest, writing]
---
# Async Standup Digest Writing

## Description
Compile distributed-team activity into asynchronous standup digests with per-person progress, plans, and blockers. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- A task requires async standup digest writing before downstream steps can proceed safely.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for async standup digest writing. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the async standup digest writing steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def digest(entries):
    blockers = [e["name"] for e in entries if e["blocked"]]
    return "Blockers: " + ", ".join(blockers)
assert digest([{"name": "ana", "blocked": True}, {"name": "bo", "blocked": False}]) == "Blockers: ana"
```

## Failure Modes
- Acting outside the declared task boundary.
- Assuming an estimate or preview equals the verified effect.
- Retrying without preserving state or evidence.
- Using stale inputs as if they were current.
- Reporting success without checking the resulting state.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Async-first team processes request structured standup digests across time zones in 2026 workflows. These are dated public signals, not adoption metrics.

## Related
- stakeholder-status-updates.md
- meeting-notes.md
- cross-timezone-async-communication.md
