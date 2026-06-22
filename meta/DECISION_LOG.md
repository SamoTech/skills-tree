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
**Status:** SUPERSEDED — pipeline now active via INITIATIVE-004

---

## D-INIT-003-001 — Schema v3.1: Add Optional `prerequisites` Field

**Date:** 2026-06-22  
**Decision:** Add optional `prerequisites` array field to `schema/skill.schema.json`.  
**Evidence:**
- `schema/skill.schema.json` prior SHA `25d54e18` — no `prerequisites` field
- `tools/extract_edges.py` SHA `6c16fb37` — docstring Source 2 references `dependencies` frontmatter field, body has no frontmatter parser
- `tools/build_graph.py` SHA `f84c8e00` — `build_node()` had no `prerequisites` read
- `meta/INITIATIVE_002B_AUTHORING_MODEL_AUDIT.md` — confirmed schema/code divergence  
**Breaking change:** NO  
**Schema version:** 3.0 → 3.1  
**Status:** COMPLETE

---

## D-INIT-004-001 — Pipeline Activation: tools updated to emit REQUIRES edges

**Date:** 2026-06-22  
**Decision:** Update `tools/build_graph.py` and `tools/extract_edges.py` to consume the `prerequisites` frontmatter field and emit `REQUIRES` edges with `source_method: "frontmatter_prerequisite"`.

**Changes made (this commit):**
1. `tools/build_graph.py`
   - `parse_frontmatter()` extended to support YAML block sequences
   - `build_node()` reads `prerequisites` list into node object
   - New `build_prerequisite_edges(node)` function emits REQUIRES edges
   - `main()` loops over nodes, calls `build_prerequisite_edges()` after body-text extraction
   - `SCHEMA_VERSION` constant: `"3.0"` → `"3.1"`
   - `meta` section of graph JSON now includes `requires_count`
2. `tools/extract_edges.py`
   - `parse_frontmatter()` added (same logic as build_graph.py)
   - `extract_from_file()` implements Source 1 (frontmatter prerequisites)
   - Docstring corrected: Source 1 = prerequisites frontmatter, Source 2 = Related Skills
3. `skills/00-sandbox/pipeline-test.md` — pilot fixture with `prerequisites: [02-reasoning/chain-of-thought]`

**Evidence basis:**
- `meta/DEPENDENCY_TOOL_ALIGNMENT.md` — exact changes required documented in INITIATIVE-003
- `schema/skill.schema.json` SHA `3917bb79` — `prerequisites` field validated at v3.1
- `schema/edge.schema.json` SHA `980e2146` — `REQUIRES` already in type enum

**Breaking change:** NO — all 367 existing skills have no `prerequisites` field; they generate 0 REQUIRES edges (same as before). Pilot fixture generates ≥1.

**Expected pipeline output after workflow trigger:**
- `meta.schema_version`: `3.1`
- `meta.requires_count`: ≥1
- REQUIRES edge from `00-sandbox/pipeline-test` → `02-reasoning/chain-of-thought`

**Status:** ACTIVE — awaiting workflow trigger and graph regeneration confirmation
