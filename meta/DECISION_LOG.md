# DECISION LOG

Only decisions that can be proven from commits, files, or repository structure are recorded here.

---

## D-R01-001 — Governance Recovery (R-01)

**Date:** 2026-06-22  
**Initiative:** R-01  
**Evidence:** Commit `71e93eba` (R-01 governance recovery push)

**Decision:** Rebuild all governance documents from repository evidence only. Prior agent-claimed metrics (58 nodes, 122 edges, schema 1.5) removed as unverifiable. Actual graph state at time of recovery: 368 nodes, 774 edges, schema 3.1 (read from `data/SKILLS_GRAPH.json` SHA `c9b0be60`).

**Rationale:** Multiple prior session outputs contained hallucinated graph metrics. Governance documents citing those metrics cannot be trusted as session-independent truth. Repository files are the only reliable source.

---

## D-007R-001 — Governance Reality Check

**Date:** 2026-06-23  
**Initiative:** INITIATIVE-007R  
**Evidence:** Commit `ff1a4e99`; files read: `tools/dependency_auditor.py` (SHA `4a3e7a3e`), `tools/recommend.py` (SHA `3d95d515`), `.github/workflows/validate-graph.yml` (SHA `667323ca`), `.github/workflows/pr-checks.yml` (SHA `c5414f05`)

**Decision:** Accept capability matrix as authoritative baseline. `dependency_auditor.py` is NOT a graph governance tool (it audits Python pip dependencies in skill frontmatter). `pr-checks.yml` has zero graph blocking capability. The only real graph CI is `validate-graph.yml` with 4 active checks.

**Deliverables created:** `GOVERNANCE_CAPABILITY_MATRIX.md`, `GOVERNANCE_GAP_CLASSIFICATION.md`, `GOVERNANCE_DEAD_CODE_AUDIT.md`, `GOVERNANCE_PRIORITY_MATRIX.md`

---

## D-INIT-008R-001 — Graph Integrity Hardening

**Date:** 2026-06-23  
**Initiative:** INITIATIVE-008R  
**Evidence:** Files read before implementation: `data/SKILLS_GRAPH.json` (SHA `c9b0be60`), `.github/workflows/validate-graph.yml` (SHA `667323ca`), `tools/recommend.py` (SHA `3d95d515`), `meta/GOVERNANCE_CAPABILITY_MATRIX.md`, `meta/GOVERNANCE_GAP_CLASSIFICATION.md`

**Pre-flight:** PASS — all required files present, graph verified (368 nodes, 774 edges, schema 3.1).

**Decisions:**

1. **Add dangling target check to CI** — Category A gap (pattern already proven in invalid-source check; mirror it for targets). Zero dangling targets found in current graph. Step added to `validate-graph.yml` after the invalid-source step.

2. **Add duplicate edge check to CI** — Category A gap (pattern already proven in duplicate-node-ID check; apply to `(source, target, type)` tuples). Zero duplicates found in current graph. Step added to `validate-graph.yml` after dangling-target step.

3. **Remove cycle suppression from `recommend.py`** — The `if not ready: ready = [sorted(remaining)[0]]` fallback (lines ~126-129, SHA `3d95d515`) was replaced with `raise ValueError(...)`. The author's own comment (`# cycle detected — add arbitrarily`) confirmed this was intentional silent suppression. Current graph has no REQUIRES cycles, so no existing functionality is broken.

**Out of scope (explicitly excluded):**
- Cycle detection in CI (Category C — not activated in this initiative)
- Orphan/unreachable node detection (Category C)
- Invalid edge type validation (Category C)
- Recommendation quality improvements
- Dependency backfill
- Architecture changes

**Success criteria met:**
- `DANGLING_TARGET_DETECTION = ACTIVE`
- `DUPLICATE_EDGE_DETECTION = ACTIVE`
- `CYCLE_SUPPRESSION = REMOVED`
- `GRAPH_VALIDATION_STATUS = HARDENED`
- No new graph features added
- No dependency expansion performed
