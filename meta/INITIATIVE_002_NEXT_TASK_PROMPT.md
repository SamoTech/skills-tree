# NEXT_TASK_PROMPT — INITIATIVE-002

## MISSION: REQUIRES Edge Generation

**Trigger:** INITIATIVE-001C audit finding B-001 — 0 REQUIRES edges in graph.  
**Prerequisite:** INITIATIVE-001C COMPLETE.  
**Baseline:** 367 nodes, 773 edges (all RELATED_TO), generated 2026-06-22T11:07:34Z.

---

## OBJECTIVE

Implement `REQUIRES` edge detection in the edge extraction pipeline so that `tools/recommend.py` can generate valid ordered learning paths.

---

## PRE-FLIGHT

Read:
- `data/SKILLS_GRAPH.json` — verify 367 nodes, 773 edges, 0 REQUIRES edges
- `tools/extract_edges.py` — inspect current edge type logic
- `tools/build_graph.py` — confirm how extract_edges is invoked
- `schema/edge.schema.json` — confirm valid edge types and required fields

Verify:
- REQUIRES_EDGES = 0  
- If non-zero: STOP, create `meta/STATE_DIVERGENCE_REPORT.md`

---

## PHASE 1 — EXTRACT_EDGES INSPECTION

Document:
- How edge types are currently assigned
- What triggers `RELATED_TO` vs other types
- Whether `REQUIRES` detection exists but is disabled
- Whether skill frontmatter `related_skills` field is used for type inference

Create: `meta/EXTRACT_EDGES_INTERFACE.md`

---

## PHASE 2 — REQUIRES DETECTION DESIGN

Design `REQUIRES` detection rules based on:
- Skill markdown content patterns (e.g. "requires", "prerequisite", "must know", "depends on")
- Frontmatter `related_skills` field + level ordering (basic → intermediate → advanced)
- Cross-category prerequisite patterns observable from existing RELATED_TO edges

Document all rules before implementation.  
Create: `meta/REQUIRES_EDGE_DESIGN.md`

---

## PHASE 3 — IMPLEMENTATION

Modify only: `tools/extract_edges.py` (or `tools/build_graph.py` if edge logic lives there).  
No changes to: schemas, skill markdown files, `recommend.py`, workflow.

---

## PHASE 4 — REBUILD & VERIFY

Trigger: `workflow_dispatch` on `build-graph.yml`  
Verify:
- REQUIRES edges > 0
- No new dangling targets introduced
- Orphan count does not increase
- `recommend.py` returns non-empty `learning_path` for at least 3 test goals

Create: `meta/INITIATIVE_002_RUN_REPORT.md`

---

## GOVERNANCE

Update:
- `meta/MEMORY_STATE.md`
- `meta/DECISION_LOG.md` — append D-INIT-002-001

---

## SUCCESS CRITERIA

```
REQUIRES_EDGES > 0
LEARNING_PATH_NON_EMPTY: YES for >= 3 test goals
ORPHANS: <= 54
DANGLING_TARGETS: <= 9
NEW_BLOCKERS_INTRODUCED: 0
```

## DO NOT

- Modify skill markdown files
- Change schema definitions  
- Add or remove nodes
- Redesign the recommendation algorithm in `recommend.py`
- Run any other initiatives concurrently
