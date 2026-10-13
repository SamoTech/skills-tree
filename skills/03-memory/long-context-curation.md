---
title: "Long Context Curation"
category: 03-memory
level: advanced
stability: experimental
description: "Select and order the subset of available context that fits a long-context window while preserving required facts, and record what was excluded and why."
added: "2026-10"
version: v1
related: [context-compaction, progressive-skill-loading, working-memory]
tags: [context, token-budget, curation]
---

# Long Context Curation

## Description
Select and order the subset of available context that fits a long-context window while preserving required facts, and record what was excluded and why. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- available context exceeds the window and the included subset must be chosen deliberately before downstream steps can proceed safely.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for long context curation work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the long context curation steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def curate(items, budget):
    chosen, spent, excluded = [], 0, []
    for item in sorted(items, key=lambda x: -x["priority"]):
        if spent + item["tokens"] <= budget:
            chosen.append(item["name"]); spent += item["tokens"]
        else:
            excluded.append(item["name"])
    return chosen, excluded

items = [{"name": "must", "tokens": 60, "priority": 3}, {"name": "nice", "tokens": 60, "priority": 1}, {"name": "skip", "tokens": 60, "priority": 2}]
chosen, excluded = curate(items, 150)
assert chosen == ["must", "skip"] and excluded == ["nice"]
```

## Failure Modes
- Filling the window with low-value items by insertion order.
- Excluding required facts to make room for volume.
- Not recording exclusions for later review.
- Assuming a bigger window removes the need to curate.
- Losing ordering cues that the model relied on.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Context curation under token budgets is a recurring 2026 long-context engineering topic in public coverage; this is a dated signal, not an adoption metric.

## Related
- context-compaction.md
- progressive-skill-loading.md
- working-memory.md
