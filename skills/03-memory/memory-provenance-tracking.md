---
title: "Memory Provenance Tracking"
category: 03-memory
level: advanced
stability: experimental
description: "Record where each stored memory came from, including source, time, and confidence, and keep that provenance attached through retrieval so any claim can be traced to its origin."
added: "2026-10"
version: v1
related: [episodic-memory, fact-verification-memory, memory-indexing]
tags: [memory, provenance, tracking, memory]
---
# Memory Provenance Tracking

## Description
Record where each stored memory came from, including source, time, and confidence, and keep that provenance attached through retrieval so any claim can be traced to its origin. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- Multiple inputs or candidates compete and must be resolved by explicit criteria.
- A wrong intermediate result would propagate into consequential actions.
- The task repeats and benefits from a deterministic procedure.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for memory provenance tracking. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the memory provenance tracking steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
# Memory Provenance Tracking: deterministic check
options = [{"name": "x", "gain": 5, "cost": 1}, {"name": "y", "gain": 4, "cost": 1}]
ranked = sorted(options, key=lambda o: (o["cost"], -o["gain"]))
assert ranked[0]["name"] == "x"
print("best:", ranked[0]["name"])
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
Provenance hardening is an active 2026 theme for agent memory and skill packages alike; retrieval without provenance is a named audit failure. These are dated public signals, not adoption metrics.

## Related
- episodic-memory.md
- fact-verification-memory.md
- memory-indexing.md
