# Decision Log

**Rule:** Only decisions provable from commits, files, or repository structure are recorded here.

---

## D-INIT-001-001 — Terminate Manual Graph Missions

**Date:** 2026-06-22  
**Decision:** Terminate R-02, R-03, R-05. Replace with INITIATIVE-001 automated pipeline.  
**Evidence:** `meta/INITIATIVE_001.md` committed at `38082503fb42c16445ce468ec7d67159cecd6dec`  
**Status:** ACTIVE

---

## D-INIT-001A-001 — Root Cause Confirmed: Workflow/Script Interface Mismatch

**Date:** 2026-06-22  
**Decision:** The graph generation failure is caused by a three-way interface mismatch between the workflow invocation, the script's CLI interface, and the output path. Fix-1 (align workflow to script) is the recommended remediation.  
**Evidence:**
- `tools/build_graph.py` SHA `f84c8e008ad17ba2f357107f7df98fab2f80fa44` — argparse defines only `--dry-run` and `--output`
- `.github/workflows/build-graph.yml` SHA `82a1afd03df5d10c3312b997b71c1fc42c300789` — workflow passes `--skills-root` and `--sbom-root` (unrecognized by script)
- `data/SKILLS_GRAPH.json` — 21-byte placeholder, never overwritten by automation  
**Status:** RESOLVED — fixed in INITIATIVE-001B

---

## D-INIT-001B-001 — INITIATIVE-001B Closes: Graph Generation Verified

**Date:** 2026-06-22  
**Decision:** Workflow patch already applied before session. Graph generated at `2026-06-22T11:07:34Z` by `github-actions[bot]`. No `workflow_dispatch` triggered (redundant).  
**Evidence:** `data/SKILLS_GRAPH.json` SHA `639b9cbb`, `meta.generated_at: 2026-06-22T11:07:34.632945+00:00`, `meta.node_count: 367`, `meta.edge_count: 773`  
**Status:** COMPLETE

---

## D-INIT-001C-001 — Graph Audit: RECOMMENDATION_READINESS = NOT READY

**Date:** 2026-06-22  
**Decision:** Graph is valid JSON with 367 nodes and 773 edges, but is NOT ready for recommendations, learning paths, or dependency analysis.  
**Primary blocker:** 0 REQUIRES edges — all 773 edges are `RELATED_TO`. `recommend.py` backward BFS depends entirely on REQUIRES edges and will return empty learning paths for all goals.  
**Secondary blockers:** tags=[] (367/367), related_skills=[] (367/367), quality_score=null (367/367), 9 dangling targets, 54 orphans.  
**Evidence:** Python audit of `data/SKILLS_GRAPH.json` SHA `639b9cbb`. Counts verified programmatically.  
**Action required:** INITIATIVE-002 — REQUIRES Edge Generation.  
**Status:** ACTIVE
