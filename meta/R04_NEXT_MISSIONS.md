# R04 — NEXT MISSIONS RANKING

**Source:** R-04 forensic findings  
**Date:** 2026-06-22  
**Mutation:** NONE — this is a recommendation document only

---

## Mission Ranking

### RANK 1 — R-02G: Complete Category Enumeration

| Attribute | Value |
|---|---|
| Priority | CRITICAL |
| Impact | HIGH — adds ~100–200 nodes to the graph |
| Risk | LOW — pure enumeration, no graph mutation |
| Expected gain | 17/17 categories covered; full node universe known |
| Blocking | R-05 cannot run on incomplete node universe |

**Rationale:** R-05 edge extraction requires knowing all valid node IDs. Adding edges to an incomplete node universe risks dangling references (edges pointing to nodes that don't exist yet). R-02G must complete before R-05 begins.

**Pre-flight:** Verify `data/SKILLS_GRAPH.json` contains exactly 197 active nodes across 8 categories.

---

### RANK 2 — R-05: Edge Extraction

| Attribute | Value |
|---|---|
| Priority | HIGH |
| Impact | CRITICAL — transforms null graph into connected graph |
| Risk | MEDIUM — risk of false positives, invalid targets, cycles |
| Expected gain | ~300–600 edges; graph goes from Level 2 to Level 3 |
| Blocking | All recommendation, traversal, and path features |

**Rationale:** The single most impactful mission available. Every downstream capability depends on edges existing. Without edges, the repository is a categorized file list, not a knowledge graph. This is the mission that changes the maturity classification.

**Requires:** R-02G complete first. Full prerequisite keyword scan of all skill files. REQUIRES/SUPPORTS/RELATED_TO edge type assignment. Validation against node ID universe.

---

### RANK 3 — R-03B: Edge Evidence Collection

| Attribute | Value |
|---|---|
| Priority | MEDIUM |
| Impact | MEDIUM — improves edge quality for R-05 |
| Risk | LOW — read-only evidence collection |
| Expected gain | Produces R03_EDGE_EVIDENCE.md, R03_GRAPH_ANALYSIS.md, R03_VALIDATION_REPORT.md |
| Blocking | Edge evidence base for R-05 confidence scoring |

**Rationale:** R-03 was never executed. Its three output files (R03_EDGE_EVIDENCE.md, R03_GRAPH_ANALYSIS.md, R03_VALIDATION_REPORT.md) are missing from the repository. These files were listed as authoritative sources for R-04 but did not exist. R-03B generates the evidence base that makes R-05 edge extraction higher-confidence and auditable.

**Can run in parallel with R-02G.**

---

### RANK 4 — R-06: Edge Validation & Cycle Audit

| Attribute | Value |
|---|---|
| Priority | MEDIUM (post R-05) |
| Impact | HIGH — ensures graph integrity after mass edge insertion |
| Risk | LOW — read-only audit |
| Expected gain | Catches duplicate edges, invalid targets, cycles |
| Blocking | Production deployment of graph query layer |

**Rationale:** After R-05 inserts hundreds of edges, a full integrity audit is mandatory before the graph is used for recommendations. R-06 is the quality gate between edge extraction and production use.

**Requires:** R-05 complete.

---

### RANK 5 — R-07: Learning Path Validation

| Attribute | Value |
|---|---|
| Priority | LOW (post R-06) |
| Impact | HIGH — proves recommendation-readiness |
| Risk | LOW — read-only traversal |
| Expected gain | Validates that REQUIRES paths form DAGs; produces sample learning paths |
| Blocking | LEVEL 5 maturity classification |

**Rationale:** The ultimate goal of the knowledge graph is learning path recommendations. R-07 validates that the graph produces correct, non-circular, meaningful learning sequences. Cannot run until edges exist and are validated.

---

## Recommended Execution Order

```
R-02G → R-03B (parallel) → R-05 → R-06 → R-07
```

R-02G and R-03B can run in parallel. R-05 requires both. R-06 and R-07 are sequential post-R-05.

## DO NOT EXECUTE

This document is a recommendation only. Do not execute any mission from this document without a fresh session prompt.
