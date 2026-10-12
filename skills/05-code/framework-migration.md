---
title: "Framework Migration"
category: 05-code
level: advanced
stability: experimental
description: "Plan and execute migrations between agent or application frameworks by inventorying usage, mapping concepts, and running equivalence tests rather than performing blind rewrites."
added: "2026-10"
version: v1
related: [code-translation, refactoring, integration-test-writing]
tags: [framework, migration, code]
---
# Framework Migration

## Description
Plan and execute migrations between agent or application frameworks by inventorying usage, mapping concepts, and running equivalence tests rather than performing blind rewrites. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- Multiple inputs or candidates compete and must be resolved by explicit criteria.
- A wrong intermediate result would propagate into consequential actions.
- The task repeats and benefits from a deterministic procedure.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for framework migration. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the framework migration steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
# Framework Migration: deterministic check
candidates = [{"id": "a", "score": 0.8, "cost": 2}, {"id": "b", "score": 0.95, "cost": 9}]
eligible = [c for c in candidates if c["score"] >= 0.8]
selected = min(eligible, key=lambda c: c["cost"])
assert selected["id"] == "a"
print("selected:", selected["id"])
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
2026 framework churn, including Microsoft Agent Framework 1.0 succeeding AutoGen and Semantic Kernel and the AG2 fork, creates recurring public migration requests. These are dated public signals, not adoption metrics.

## Related
- code-translation.md
- refactoring.md
- integration-test-writing.md
