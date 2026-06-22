# Dependency Migration Plan

**Mission:** INITIATIVE-003 Phase 4  
**Date:** 2026-06-22  
**Status:** APPROVED — phases defined, none executed yet

---

## Overview

This plan moves the repository from its current state (0 REQUIRES edges, no prerequisite authoring model) to a fully functional dependency graph capable of powering `recommend.py` learning path generation.

---

## Phase A — Schema Support ✅ COMPLETE (this commit)

**Objective:** Allow authors to declare prerequisites in skill frontmatter without schema validation failure.

**Changes delivered:**
- `schema/skill.schema.json` updated to v3.1 — `prerequisites` field added (optional array, validated)
- `meta/DEPENDENCY_SCHEMA_SPEC.md` — canonical field specification
- `meta/DEPENDENCY_TOOL_ALIGNMENT.md` — exact changes required in tools

**Verification:** All 367 existing skills pass schema validation unchanged (field is optional).

**Blocking next phase:** Phase B cannot start until Phase A is complete. ✅

---

## Phase B — Tool Updates (INITIATIVE-004)

**Objective:** Update `build_graph.py` and `extract_edges.py` to read `prerequisites` frontmatter and emit `REQUIRES` edges.

**Changes required (from `meta/DEPENDENCY_TOOL_ALIGNMENT.md`):**

1. `tools/build_graph.py`
   - Add frontmatter `prerequisites` read in `build_node()`
   - Add REQUIRES edge generation loop after node construction
   - Update `SCHEMA_VERSION` constant: `"3.0"` → `"3.1"`

2. `tools/extract_edges.py`
   - Add frontmatter parser (reuse `parse_frontmatter()` pattern from `build_graph.py`)
   - Implement Source 2 in `extract_from_file()`: loop over `prerequisites` field, emit REQUIRES edges

**Success criterion:** `python tools/build_graph.py --dry-run` with a pilot skill file containing `prerequisites` produces at least 1 REQUIRES edge in output. No regressions on existing 773 edges.

**Blocking next phase:** Phase C requires the tool updates to be live before backfill writes produce edges.

---

## Phase C — Pilot Category Backfill (INITIATIVE-005)

**Objective:** Backfill `prerequisites` declarations in one high-value category to validate the end-to-end pipeline.

**Recommended pilot category:** `09-agentic-patterns`
- Rationale: Most naturally sequential skill set (foundational patterns → composite patterns). INITIATIVE-002A found 5 LEVEL 3 candidates here. Highest density of dependency language in existing files.

**Process:**
1. For each skill in `09-agentic-patterns`, read the file and identify explicit dependencies
2. Add `prerequisites` array to frontmatter where evidence exists
3. Run `build_graph.py` — verify REQUIRES edges appear
4. Run `recommend.py --goal "build autonomous agent"` — verify learning path is ordered
5. Document coverage achieved

**Success criterion:** ≥10 REQUIRES edges generated from `09-agentic-patterns` alone. `recommend.py` returns a non-trivial ordering for at least one test goal.

---

## Phase D — Repository-wide Rollout (INITIATIVE-006)

**Objective:** Systematic backfill of `prerequisites` across all 13 categories.

**Process:** Category by category, ordered by dependency depth:
1. `02-reasoning` (foundational — few prerequisites expected)
2. `03-memory`, `04-context`
3. `07-tool-use`, `12-data`
4. `09-agentic-patterns`, `08-evaluation`
5. `05-output`, `06-code`, `10-safety`, `11-multimodal`, `13-deployment`

**Success criterion:** REQUIRES edge density ≥ 30% of nodes have at least one REQUIRES edge. `recommend.py` produces meaningful learning paths for 5+ distinct goals.

---

## Phase E — CI Enforcement (INITIATIVE-007)

**Objective:** Add GitHub Actions workflow to validate `prerequisites` field on every PR.

**Changes required:**
- New workflow: `.github/workflows/validate-prerequisites.yml`
- Validates: all IDs in `prerequisites` resolve to known skill IDs
- Validates: no circular prerequisites (A requires B requires A)
- On failure: block merge

**Success criterion:** CI catches at least one invalid prerequisite reference in test run.

---

## Phase Summary

| Phase | Initiative | Status | Blocker |
|---|---|---|---|
| A — Schema support | INITIATIVE-003 | ✅ COMPLETE | — |
| B — Tool updates | INITIATIVE-004 | ⏳ PENDING | Phase A |
| C — Pilot backfill | INITIATIVE-005 | ⏳ PENDING | Phase B |
| D — Repository rollout | INITIATIVE-006 | ⏳ PENDING | Phase C |
| E — CI enforcement | INITIATIVE-007 | ⏳ PENDING | Phase D |
