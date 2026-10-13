---
title: "Graph Centrality Analysis"
category: 12-data
level: advanced
stability: experimental
description: "Compute and interpret centrality measures on graph data with explicit edge semantics and confidence bounds before ranking conclusions."
added: "2026-10"
version: v1
related: [statistical-analysis, data-visualization, data-aggregation]
tags: [graphs, centrality, analysis]
---

# Graph Centrality Analysis

## Description
Compute and interpret centrality measures on graph data with explicit edge semantics and confidence bounds before ranking conclusions. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- importance or influence must be inferred from graph structure.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for graph centrality analysis work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the graph centrality analysis steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def degree_centrality(edges, node):
    return sum(1 for a, b in edges if node in (a, b))

edges = [('a', 'b'), ('a', 'c'), ('b', 'c')]
assert degree_centrality(edges, 'a') == 2
assert degree_centrality(edges, 'd') == 0
```

## Failure Modes
- Ranking nodes without stating what an edge means.
- Comparing centralities across graphs of different density.
- Ignoring direction when the relation is asymmetric.
- Reading influence into centrality that only measures activity.
- Never validating edges against a sampled ground truth.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Graph analytics on relationship data recurs in 2026 analysis requests; this is a dated signal, not an adoption metric.

## Related
- statistical-analysis.md
- data-visualization.md
- data-aggregation.md
