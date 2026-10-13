---
name: memory-graph-pruning
description: Prune stale or low-value nodes and edges from a memory graph under explicit retention rules, measure retrieval impact before and after, and keep prune decisions reversible.
metadata:
  source: skills/03-memory/memory-graph-pruning.md
  category: 03-memory
  version: "v1"
---

# Memory Graph Pruning

## Description
Prune stale or low-value nodes and edges from a memory graph under explicit retention rules, measure retrieval impact before and after, and keep prune decisions reversible. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- a memory graph has grown past its useful size and pruning must not hurt recall before downstream steps can proceed safely.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for memory graph pruning work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the memory graph pruning steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def prune(graph, max_age, now):
    kept, pruned = {}, []
    for node, meta in graph.items():
        if now - meta["ts"] > max_age and not meta.get("pinned"):
            pruned.append(node)
        else:
            kept[node] = meta
    return kept, pruned

g = {"a": {"ts": 0, "pinned": False}, "b": {"ts": 100, "pinned": False}}
kept, pruned = prune(g, 10, 100)
assert pruned == ["a"] and list(kept) == ["b"]
```

## Failure Modes
- Pruning without measuring retrieval impact.
- Deleting pinned or legally retained records.
- Losing provenance links that surviving nodes referenced.
- Making pruning irreversible.
- Using age alone and ignoring access frequency.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Memory hygiene for long-running agents follows recurring 2026 requests for hierarchical memory management, including forgetting and eviction; this is a dated signal, not an adoption metric.

## Related
- forgetting.md
- memory-indexing.md
- knowledge-graph-updates.md
