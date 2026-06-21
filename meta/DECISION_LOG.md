# DECISION_LOG.md

---

## D-009 — TASK-005B: Collision Review Final Decisions (2026-06-21)

**Context:** PERCEPTION_AUDIT identified four nodes with potential semantic collision in the 12-data cluster.

**Decisions:**

1. `skill:data-extraction` → **KEEP** — existing node, becoming cluster hub
2. `skill:structured-data-reading` → **KEEP** — semantically distinct pre-extraction role
3. `skill:database-reading` → **KEEP** — SQL/cursor access, domain-specific
4. `skill:api-response-parsing` → **MERGE into data-extraction** — too thin as standalone; absorbed via `data-extraction → api-integration RECOMMENDED_WITH` edge

**Impact:** 6 nodes added (not 7), 15 edges applied, graph integrity maintained.

---

## D-008 — TASK-005B: Six Approved Nodes (2026-06-21)

**Context:** NODE_SELECTION.md approved exactly 6 nodes for TASK-005B implementation.

**Nodes approved:**
- `skill:structured-data-reading` (12-data, beginner)
- `skill:database-reading` (12-data, intermediate)
- `skill:file-system-access` (04-action-execution, beginner)
- `skill:output-formatting` (05-code, beginner)
- `skill:schema-validation` (12-data, intermediate)
- `skill:data-transformation` (12-data, intermediate)

**Constraint:** No additional nodes. No category expansion.

---

## D-007 — TASK-004: PERCEPTION_AUDIT Scope (2026-06-18)

**Context:** Audit identified gaps in agent perception/data-reading capabilities. Proposed 6-node expansion.

**Decision:** Proceed with 6 nodes only. Defer api-response-parsing, visual-understanding, audio-processing to future tasks.

---

## D-006 — TASK-003: Reasoning Category Expansion (2026-06-15)

**Context:** 9 new nodes added to 02-reasoning category.

**Decision:** Approved. Graph grew 38→47 nodes.

---

## D-005 — Schema Version Policy

**Decision:** Bump schema_version on every structural change (node or edge additions). Minor changes increment the patch digit. This is v1.4 after TASK-005B.

---

## D-004 — Centrality Recalculation Policy

**Decision:** Centrality values in node objects are advisory snapshots, not live-computed. They are recalculated at task completion. The EvidenceDeriver derives evidence counts at runtime separately.

---

## D-003 — Sink Node Policy

**Decision:** Sink nodes (zero out-degree) are acceptable and expected. Terminal knowledge nodes like `skill:llm-orchestration`, `skill:vector-search` are correct sinks — they receive many dependencies but do not themselves require other skills in this graph's scope.

---

## D-002 — Edge Type Vocabulary

**Decision:** Four edge types in use: REQUIRES, RECOMMENDED_WITH, SUPPORTS, LEARN_BEFORE. No new types may be added without PROJECT_CONSTITUTION amendment.

---

## D-001 — Graph Initialization

**Decision:** Start from the 23 agentic-patterns skill files as seed nodes. Build outward by audit-driven expansion.
