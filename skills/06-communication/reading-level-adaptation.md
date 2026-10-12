---
title: "Reading Level Adaptation"
category: 06-communication
level: advanced
stability: experimental
description: "Adjust text to a target reading level while preserving meaning, terminology, and all factual claims, and verify comprehension targets with a stated method."
added: "2026-10"
version: v1
related: [plain-language-writing, audience-analysis, paraphrasing]
tags: [reading, level, adaptation, communication]
---

# Reading Level Adaptation

## Description
Adjust text to a target reading level while preserving meaning, terminology, and all factual claims, and verify comprehension targets with a stated method. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- Multiple inputs or candidates compete and must be resolved by explicit criteria.
- A wrong intermediate result would propagate into consequential actions.
- The task repeats and benefits from a deterministic procedure.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for reading level adaptation. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the reading level adaptation steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
# Reading Level Adaptation: deterministic check
allowed = {"idle": {"running"}, "running": {"done", "failed"}, "failed": {"idle"}}

def transition(state, nxt):
    return nxt in allowed.get(state, set())

assert transition("idle", "running")
assert not transition("idle", "done")
print("transitions checked")
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
Accessibility and plain-language requirements recur in 2026 documentation guidance. These are dated public signals, not adoption metrics.

## Related
- plain-language-writing.md
- audience-analysis.md
- paraphrasing.md
