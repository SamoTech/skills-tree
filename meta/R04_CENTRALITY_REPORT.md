# R04 — CENTRALITY REPORT

**Source:** `data/SKILLS_GRAPH.json` (R-02F, 2026-06-22)  
**Mutation:** NONE

---

## Centrality Analysis Status

**RESULT: NOT COMPUTABLE**

Centrality metrics (degree centrality, betweenness centrality, closeness centrality) require at least one edge to produce meaningful values.

The current graph contains:
- Nodes: 197
- Edges: 0

With zero edges:
- Degree centrality = 0 for all nodes
- Betweenness centrality = 0 for all nodes (no paths exist)
- Closeness centrality = undefined for all nodes (no connected pairs)

Reporting synthetic centrality values would violate the R-04 governance rule: **"If a value cannot be proven: write UNKNOWN."**

## TOP 25 HUBS

```
CANNOT BE DETERMINED — no edges in graph
```

All 197 nodes have identical degree = 0. No node is more or less central than any other.

## Predicted Hub Candidates (post-edge extraction)

Based on skill taxonomy and domain knowledge, the following are *predicted* high-degree nodes once R-05 edge extraction runs. These are **predictions, not measurements.**

| Predicted Hub | Category | Rationale |
|---|---|---|
| skill:chain-of-thought | 02-reasoning | Foundational to nearly all reasoning skills |
| skill:code-generation | 05-code | Central to all code-adjacent skills |
| skill:rag | 03-memory | Connected to retrieval, embedding, search |
| skill:task-decomposition | 02-reasoning | Prerequisite pattern across planning |
| skill:api-call | 04-action-execution | Action hub for tool-use |
| skill:web-search | 11-web | Entry point for information retrieval |
| skill:structured-data-reading | 01-perception | Bridge between perception and data |
| skill:sql-execution | 12-data | Core data manipulation hub |

**All values above are predictions. None are measurements. Centrality must be rerun after edges are added.**
