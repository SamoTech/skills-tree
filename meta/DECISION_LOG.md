# DECISION_LOG.md — Immutable Decision Audit Trail

> This log records every major architectural and implementation decision made during the SamoTech/skills-tree agent execution.  
> Entries are **append-only**. Never delete or modify existing entries.  
> Purpose: prevent future agents from reversing or duplicating past decisions.

---

## Format

```
### [DATE] [TASK-ID] — [Decision Title]
**Decision:** ...
**Reasoning:** ...
**Impact:** ...
**Alternatives Rejected:** ...
```

---

### 2026-06-16 TASK-001 — Map agentic-patterns files to graph (not create new files)

**Decision:** Map all 23 existing `.md` files in `skills/09-agentic-patterns/` to new graph nodes in `data/SKILLS_GRAPH.json`. Do NOT create new skill files.

**Reasoning:** The backlog explicitly required making existing skills "visible to the graph" rather than authoring new content. 23 files existed with 0 graph representation (except `workflow-automation`). Creating files would violate the TASK-001 acceptance criteria and risk duplication.

**Impact:** Graph grew from 15→38 nodes, 13→72 edges. `09-agentic-patterns` now fully mapped with 24 nodes. Hub node `skill:react-pattern` has highest centrality (0.1892).

**Alternatives Rejected:**
- Creating new skill files alongside mapping: rejected (out of scope, risk of duplication)
- Mapping only highest-priority skills (subset): rejected (task required all 23)

---

### 2026-06-16 TASK-001 — Node ID convention: `skill:kebab-case`

**Decision:** All new node IDs follow `skill:kebab-case` format. File name maps directly to ID with `skill:` prefix. E.g., `react.md` → `skill:react-pattern` (longer ID chosen to avoid collision with future `react` (JS framework) node).

**Reasoning:** The existing 15 nodes all used `skill:kebab-case`. Consistency is required. `react.md` was mapped to `skill:react-pattern` (not `skill:react`) to leave namespace room for frontend framework skills in a future category.

**Impact:** All 23 new IDs are unambiguous and non-colliding.

**Alternatives Rejected:**
- `skill:react` as ID: rejected (would collide with potential future React.js skill node)
- Using file path as ID: rejected (not consistent with existing schema)

---

### 2026-06-16 TASK-001 — `skill:cot` and `skill:tot` added in TASK-001 (not TASK-003)

**Decision:** `cot` and `tot` were added in TASK-001 (mapping `09-agentic-patterns/cot.md` and `09-agentic-patterns/tot.md`), not in TASK-003 (which also lists them in its description).

**Reasoning:** The files existed in `09-agentic-patterns/` and TASK-001 required mapping ALL files in that directory. TASK-003 must be aware that these nodes already exist.

**Impact:** TASK-003 skipped `cot` and `tot` from its node creation list. TASK-003 added only the remaining reasoning skills: `self-consistency`, `step-back-prompting`, `least-to-most`, `meta-prompting`, `planning-decomposition`, `hypothesis-generation`, `goal-decomposition`, `reasoning-under-uncertainty`, `analogical-reasoning`.

**Alternatives Rejected:**
- Deferring cot/tot to TASK-003: rejected (would leave `09-agentic-patterns/` directory incompletely mapped)

---

### 2026-06-16 TASK-001 — Schema version held at 1.3

**Decision:** `schema_version` field in `SKILLS_GRAPH.json` was not incremented. Remained at `1.3`.

**Reasoning:** TASK-001 added nodes and edges but did not change the JSON schema shape. Schema version should only increment on structural/breaking changes to the graph format.

**Impact:** Consumers of the graph at schema 1.3 continue to parse successfully.

**Alternatives Rejected:**
- Bumping to 1.4: rejected (no schema change occurred)

---

### 2026-06-21 TASK-003 — Add 9 advanced reasoning nodes to `02-reasoning` category

**Decision:** Added exactly 9 nodes as specified: `self-consistency`, `step-back-prompting`, `least-to-most`, `meta-prompting`, `planning-decomposition`, `hypothesis-generation`, `goal-decomposition`, `reasoning-under-uncertainty`, `analogical-reasoning`. All assigned to `category: "02-reasoning"`.

**Reasoning:** These are fundamental reasoning strategies that underpin higher-order agent behaviours. Placing them in `02-reasoning` (not `09-agentic-patterns`) correctly reflects their nature as cognitive techniques rather than agent execution patterns. TASK-003 spec explicitly listed 9 node IDs.

**Impact:** Graph grew from 38→47 nodes, 72→93 edges. `02-reasoning` category expanded from 1 node (`prompt-engineering`) to 10 nodes. TASK-004 (causal + counterfactual reasoning) is now unblocked.

**Alternatives Rejected:**
- Placing nodes in `09-agentic-patterns`: rejected (these are reasoning primitives, not agent execution patterns)
- Adding `skill:cot` and `skill:tot` again: rejected — both already exist from TASK-001, anti-duplicate check confirmed

---

### 2026-06-21 TASK-003 — Schema version held at 1.3

**Decision:** `schema_version` remained at `1.3`.

**Reasoning:** No structural change to the JSON schema. Node and edge addition is a data-level change, not a schema-level change.

**Impact:** Zero breaking changes for downstream consumers.

**Alternatives Rejected:**
- Bumping to 1.4: rejected (no schema structural change)

---

### 2026-06-21 TASK-003 — Bidirectional RECOMMENDED_WITH between `reasoning-under-uncertainty` and `hypothesis-generation`

**Decision:** `hypothesis-generation → reasoning-under-uncertainty` (RECOMMENDED_WITH) and `reasoning-under-uncertainty → hypothesis-generation` (RECOMMENDED_WITH) were both added, forming a symmetric synergy pair.

**Reasoning:** These two skills are genuinely complementary: generating hypotheses requires tolerating uncertainty, and reasoning under uncertainty is enriched by hypothesis-generation. A bidirectional RECOMMENDED_WITH pair is semantically valid in the schema and does not create a directed cycle (neither is REQUIRES or LEARN_BEFORE).

**Impact:** Two edges added for this pair. Graph remains a valid DAG when only REQUIRES + LEARN_BEFORE edge types are considered.

**Alternatives Rejected:**
- Single unidirectional edge: rejected (the relationship is symmetric; one direction would mislead traversal)
