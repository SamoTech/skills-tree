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
**Decision:** The graph generation failure is caused by a three-way interface mismatch between the workflow invocation, the script's CLI interface, and the output path.  
**Evidence:** `tools/build_graph.py` SHA `f84c8e00`, `.github/workflows/build-graph.yml` SHA `82a1afd0`  
**Status:** RESOLVED — fixed in INITIATIVE-001B

---

## D-INIT-001B-001 — INITIATIVE-001B Closes: Graph Generation Verified

**Date:** 2026-06-22  
**Decision:** Workflow patch applied. Graph generated at `2026-06-22T11:07:34Z`. node_count: 367, edge_count: 773.  
**Evidence:** `data/SKILLS_GRAPH.json` SHA `639b9cbb`  
**Status:** COMPLETE

---

## D-INIT-001C-001 — Graph Audit: RECOMMENDATION_READINESS = NOT READY

**Date:** 2026-06-22  
**Decision:** Graph valid JSON, 367 nodes, 773 edges. NOT ready for recommendations. Primary blocker: 0 REQUIRES edges.  
**Evidence:** Python audit of `data/SKILLS_GRAPH.json` SHA `639b9cbb`.  
**Status:** SUPERSEDED — pipeline active via INITIATIVE-004

---

## D-INIT-003-001 — Schema v3.1: Add Optional `prerequisites` Field

**Date:** 2026-06-22  
**Decision:** Add optional `prerequisites` array to `schema/skill.schema.json`. Schema version 3.0 → 3.1.  
**Evidence:** `schema/skill.schema.json` prior SHA `25d54e18`, `tools/extract_edges.py` SHA `6c16fb37`  
**Breaking change:** NO  
**Status:** COMPLETE

---

## D-INIT-004-001 — Pipeline Activation: tools updated to emit REQUIRES edges

**Date:** 2026-06-22  
**Decision:** Update `tools/build_graph.py` and `tools/extract_edges.py` to consume `prerequisites` frontmatter and emit REQUIRES edges.  
**Commit:** `bc973371`  
**Status:** ACTIVE — graph rebuild pending

---

## D-INIT-004V-001 — Verification: Graph Stale, Workflow Trigger Required

**Date:** 2026-06-22  
**Decision:** `data/SKILLS_GRAPH.json` SHA `b3c27479`: schema_version 3.0, requires_count 0. Graph pre-dates INITIATIVE-004 tools.  
**Evidence:** Live read of `data/SKILLS_GRAPH.json`, commit log.  
**Status:** RESOLVED by INITIATIVE-004W

---

## D-INIT-004W-001 — Root Cause Proven: Concurrency Cancel Race

**Date:** 2026-06-22  
**Decision:** The build-graph workflow triggered by INITIATIVE-004 commit `bc973371` was cancelled before its commit step due to `cancel-in-progress: true` concurrency setting combined with four rapid bot commits (11:49:07–11:49:19Z) that entered the same concurrency group within 11–23 seconds of the triggering commit.

**Evidence:**
- `.github/workflows/build-graph.yml` SHA `d2f4ac36`: `concurrency.cancel-in-progress: true`
- Commit log: `bc973371` at 11:48:56Z; next bot commits at 11:49:07Z (11 seconds later)
- No `chore(graph): rebuild skills dependency graph` commit exists after `bc973371`
- `beadae4d` (11:49:11Z): "chore(export): regenerate skills API — 368 skills" — confirms pipeline-test.md counted by export workflow, proving it exists and is parseable
- `tools/build_graph.py` SHA `32cb1509`: SCHEMA_VERSION = "3.1", `build_prerequisite_edges()` present, `parse_frontmatter()` handles block sequences — code is correct

**Remediation:** INITIATIVE-004W commit touches `skills/00-sandbox/pipeline-test.md` (qualifying `skills/**/*.md` path). This is the sole triggering file in this commit. No concurrent bot workflows expected. Build-graph workflow should complete without cancellation.

**Architectural risk documented:** Future multi-workflow commits may reproduce this race. Options: use `workflow_run` trigger, add `[skip ci]` scope to bot commits more aggressively, or accept the risk and retry via `workflow_dispatch`.

**Status:** ACTIVE — awaiting post-rebuild verification
