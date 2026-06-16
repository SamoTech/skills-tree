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

**Impact:** TASK-003 must skip `cot` and `tot` from its node creation list. TASK-003 should add only the remaining reasoning skills not already in the graph: `self-consistency`, `step-back-prompting`, `least-to-most`, `meta-prompting`, `planning-decomposition`, `hypothesis-generation`, `goal-decomposition`, `reasoning-under-uncertainty`, `analogical-reasoning`.

**Alternatives Rejected:**
- Deferring cot/tot to TASK-003: rejected (would leave `09-agentic-patterns/` directory incompletely mapped, violating TASK-001 acceptance criteria)

---

### 2026-06-16 TASK-001 — Schema version held at 1.3

**Decision:** `schema_version` field in `SKILLS_GRAPH.json` was not incremented. Remained at `1.3`.

**Reasoning:** TASK-001 added nodes and edges but did not change the JSON schema shape. Schema version should only increment on structural/breaking changes to the graph format.

**Impact:** Consumers of the graph API continue to work without version-bump handling.

**Alternatives Rejected:**
- Bumping to 1.4: rejected (no schema-shape change was made)

---

### 2026-06-16 GOVERNANCE — MEMORY_STATE.md and DECISION_LOG.md created

**Decision:** Created `meta/MEMORY_STATE.md` and `meta/DECISION_LOG.md` as required by the Persistent Roadmap + Persistent Memory operating mode.

**Reasoning:** These files did not exist prior to this governance commit. Without them, any new agent session would have no canonical checkpoint and could repeat TASK-001 or drift from the roadmap.

**Impact:** All future agent sessions must read `MEMORY_STATE.md` first. All major decisions must be appended here.

**Alternatives Rejected:**
- Relying on conversation history: rejected (violates the Persistent Memory Rule — repo artifacts are the only source of truth)

---

### 2026-06-16 GOVERNANCE — Project Constitution v1.0.0 ratified

**Decision:** Created and committed `meta/PROJECT_CONSTITUTION.md` as the supreme governance document for the repository.

**Reasoning:** The SamoTech Architect provided a Mission, 10 Principles, Non-Goals, and 5 Success Metrics. These needed to be encoded as binding, operational rules — not just aspirational text. The constitution translates each principle into an enforceable operational rule (with enforcement clauses), defines a conflict resolution priority order (Article VII), and establishes an amendment process (Article VI).

**Impact:**
- All 10 principles now have binding Operational Rules
- Conflict resolution follows P-06 > P-07 > P-02 > P-05 > P-03 priority
- Success metrics M-01 through M-05 have measurable definitions and current baselines
- The constitution supersedes ROADMAP.md and ROADMAP_V2.md where they conflict
- Current M-04 (production relevance) is already met: 84.2% of nodes are stable/evolving
- Current M-05 partially met: Remember (5 nodes ✓) and Coordinate (26 nodes ✓); Perceive and Reason are blockers

**Alternatives Rejected:**
- Adding principles to AGENT_SKILLS_MASTER_PLAN.md: rejected (plans change; constitutions constrain plans)
- Encoding rules in CI only: rejected (CI cannot capture reasoning-level constraints on agent behavior)

---

*Decision Log initialized: 2026-06-16 | Last updated: 2026-06-16*
