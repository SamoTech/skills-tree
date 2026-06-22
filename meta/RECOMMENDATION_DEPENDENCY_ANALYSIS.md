# Recommendation Engine Dependency Analysis

**Mission:** INITIATIVE-002B Phase 3  
**Date:** 2026-06-22  
**Source:** `tools/recommend.py` (SHA: 3d95d51548536e1b5c930724bc1f9f9b380361c2)

---

## Engine Architecture (Confirmed)

`recommend.py` operates in three sequential stages:

```
Goal string
    │
    ▼
[1] Keyword match → seed_skills (up to 10 nodes)
    │
    ▼
[2] Backward BFS over REQUIRES edges → all_needed set
    │
    ▼
[3] Topological sort (Kahn's) → ordered learning path
    │
    ▼
JSON / Markdown output
```

---

## REQUIRES Dependency on REQUIRES Edges

### Stage 1 — Keyword Matching

**Does NOT require REQUIRES edges.**  
Matches against `title`, `id`, and `tags` fields. Works today with 0 REQUIRES edges.  
Return: up to 10 matching skill IDs.

### Stage 2 — Backward BFS (CRITICAL DEPENDENCY)

```python
def resolve_dependencies(seed_skills, adj_bwd):
    for (prereq, edge_type) in adj_bwd.get(skill, []):
        if edge_type == "REQUIRES" and prereq not in visited:
            ...
```

**Filters exclusively on `edge_type == "REQUIRES"`.** RELATED_TO edges are ignored entirely.  
**With 0 REQUIRES edges:** BFS terminates immediately. `all_needed` = seed_skills only. No prerequisites discovered.  
**With 5 REQUIRES edges (002A candidates):** BFS reaches at most 1–2 hops for 5 node pairs. Marginally functional.

**Minimum density for useful output:** UNKNOWN — no threshold defined in code or documentation. Empirical estimate: ≥ 30–50% of nodes need at least one REQUIRES edge before learning paths span more than 2–3 hops.

### Stage 3 — Topological Sort

**Depends entirely on Stage 2 output.**  
With an empty REQUIRES subgraph, topo sort returns seed_skills in alphabetical order — which is arbitrary, not pedagogically ordered.

---

## Current Behavior (0 REQUIRES edges)

| Query | Expected behavior | Actual behavior |
|---|---|---|
| `--goal "build autonomous agent"` | Returns full prerequisite chain | Returns 10 keyword-matched skills in alphabetical order |
| `--goal "causal reasoning"` | Returns foundational logic skills first | Returns matched skills, no ordering |
| Learning path depth | "shallow/medium/deep" based on chain length | Always "shallow" (≤5 nodes, no chain expansion) |

**The recommendation engine is architecturally complete but functionally blocked by missing REQUIRES edges.**

---

## Fallback Behavior

The engine has **no explicit fallback** for the zero-REQUIRES condition. It does not:
- Fall back to RELATED_TO edges for ordering
- Emit a warning that the graph has no dependency data
- Return a degraded-mode indicator

From user perspective, the engine appears to work (it returns skill IDs) but produces meaningless ordering.

---

## Minimum Viable Dependency Density

For `recommend.py` to produce useful learning paths:

| Density target | REQUIRES edges needed | Current gap |
|---|---|---|
| Minimal (1-hop paths) | ~50 edges | 50 edges short |
| Useful (2–3 hop paths) | ~150–200 edges | 145–195 short |
| Full (complete dependency model) | ~400–600 edges | UNKNOWN upper bound |

**These are estimates based on engine architecture. Exact numbers require empirical testing.**

---

## Conclusion

`recommend.py` is **not viable** in its current state for its stated purpose (ordered learning paths).  
It requires REQUIRES edges to function. Adding the 5 candidates from INITIATIVE-002A would have negligible impact.  
A systematic method to add REQUIRES edges at scale is required before the engine delivers value.
