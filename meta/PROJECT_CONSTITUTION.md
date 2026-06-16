# PROJECT_CONSTITUTION.md — Skills-Tree Project Constitution

> **Status:** RATIFIED  
> **Version:** 1.0.0  
> **Ratified:** 2026-06-16  
> **Authority:** SamoTech Architect  
> **Binding on:** All agents, contributors, and automated systems operating on this repository.

This document is the supreme governance authority for the SamoTech/skills-tree project.  
It takes precedence over all other documents when conflicts arise.  
It may only be amended by the SamoTech Architect. All amendments must be appended — no section may be deleted.

---

## Article I — Mission

> **Become the definitive skill graph and competency model for advanced AI agents and agent engineers.**

This mission has three operational components:

1. **Definitive** — The graph must be the best-connected, most production-relevant, most traversable skills graph in the AI agent domain. Not the largest. The best-curated.
2. **Skill graph** — The primary artifact is `data/SKILLS_GRAPH.json`. Documentation (`.md` files) is secondary. Graph edges are what make the project useful — without edges, nodes are just a flat list.
3. **Advanced AI agents and agent engineers** — The target audience is practitioners building production agent systems, not students learning LLM basics.

---

## Article II — Core Principles

Each principle is binding. Each includes an **Operational Rule** that agents and contributors must follow.

### P-01 — Graph quality over skill count

> "Graph quality is more important than skill count."

**Operational Rule:** A node with zero or one outgoing edge may not be merged to main unless explicitly approved. Every new node requires at minimum 2 typed edges (`REQUIRES`, `RECOMMENDED_WITH`, `LEARN_BEFORE`, or `SUPPORTS`). Nodes with degree centrality < 0.03 are candidates for pruning review.

**Enforcement:** `statistics.total_edges / statistics.total_nodes` ratio must not decrease between consecutive commits that add nodes.

---

### P-02 — Relationships first

> "Relationships are more important than documents."

**Operational Rule:** A skill `.md` file that exists with no corresponding graph node is a gap, not an asset. Adding a `.md` file without a graph node is forbidden. Graph edges must be added in the same commit as the node.

**Enforcement:** Every task that adds skill files must include graph node + edge additions in the same atomic commit.

---

### P-03 — Production skills first

> "Production skills are prioritized over academic skills."

**Operational Rule:** Before adding a new skill, the contributor must be able to name at least one production agent system or open-source framework that uses or requires it. Academic-only skills (no known production deployment) require explicit architect approval and a `stability: experimental` tag.

**Node stability taxonomy:**
- `stable` — Used in production systems
- `evolving` — Emerging but with real implementations
- `experimental` — Research / theoretical; requires justification

---

### P-04 — Real-world utility

> "Skills must be useful in real AI systems."

**Operational Rule:** Skills that cannot be linked to at least one entry in `meta/frameworks.md` or a known production framework (LangChain, LlamaIndex, AutoGen, CrewAI, Semantic Kernel, etc.) must not be added without justification documented in `meta/DECISION_LOG.md`.

---

### P-05 — Goal connectivity is mandatory

> "Every skill should connect to goals."

**Operational Rule:** Every skill node must have at least one path (direct or transitive, max 3 hops) to a goal defined in `meta/GOAL_TAXONOMY.md`. Skills with no goal path are **orphans** and must be connected or removed.

**Goal coverage metric:** `(skills reachable from ≥1 goal) / total_nodes`. Target: ≥ 90%.

---

### P-06 — Zero duplicates

> "Duplicate concepts are forbidden."

**Operational Rule:** Before adding any node, search `data/SKILLS_GRAPH.json` for:
1. Exact ID match
2. Name similarity (cosine similarity > 0.85 on name tokens)
3. Conceptual overlap (does an existing node cover this concept from a different angle?)

If a potential duplicate is found, extend the existing node (add edges, improve metadata) rather than creating a new node.

**Anti-drift registry:** `meta/MEMORY_STATE.md` maintains the canonical list of all existing node IDs. Check it before every task.

---

### P-07 — Connect before expand

> "Existing skills must be connected before new skills are added."

**Operational Rule:** At the start of every sprint, run a graph audit. If any existing node has fewer than 2 edges, those connections must be added before new nodes are introduced. Expanding a disconnected graph is explicitly forbidden.

**Current state (2026-06-16):** All 38 existing nodes have ≥ 2 edges. P-07 is satisfied.

---

### P-08 — Recommendation quality is first-class

> "Recommendation quality is a first-class feature."

**Operational Rule:** The graph must support the query: *"Given goal G and skill level L, return an ordered learning path."* Every task that modifies the graph must include a spot-check: pick one goal from `meta/GOAL_TAXONOMY.md` and verify the recommendation engine can produce a sensible path through the new/modified nodes.

**Recommendation engine spec:** `meta/RECOMMENDATION_ENGINE_SPEC.md`

---

### P-09 — Agentic systems are the primary domain

> "Agentic systems are the primary domain."

**Operational Rule:** When a skill is borderline (e.g., a general ML concept), ask: *"Does this skill change how an agent perceives, reasons, acts, or learns?"* If yes, it belongs. If it is purely academic, infrastructure, or DevOps, it does not.

**Primary categories (in priority order):**
1. `09-agentic-patterns` — Agent design patterns
2. `02-reasoning` — Agent cognition and reasoning
3. `01-perception` — Agent input modalities
4. `03-memory` — Agent memory systems
5. `04-action-execution` — Agent action primitives
6. `07-tool-use` — Agent tool integration
7. `10-computer-use` — Agent computer interaction
8. `15-orchestration` — Agent coordination

---

### P-10 — Traversability and explainability

> "The graph should be traversable and explainable."

**Operational Rule:** Every edge must have a `type` (one of `REQUIRES`, `RECOMMENDED_WITH`, `LEARN_BEFORE`, `SUPPORTS`) and a `confidence` score (0.0–1.0). Typeless or confidence-free edges are invalid. The graph must never contain cycles in `REQUIRES` or `LEARN_BEFORE` edges.

**Edge type semantics:**
- `REQUIRES` — Cannot effectively use skill A without skill B
- `LEARN_BEFORE` — Skill B should be learned before A for best results
- `RECOMMENDED_WITH` — Skills are complementary; learning together improves outcomes
- `SUPPORTS` — Skill A enhances but does not require skill B

---

## Article III — Non-Goals

The following are **permanently out of scope**. Adding content that serves these purposes is grounds for rejection without review.

| Non-Goal | Reason |
|---|---|
| Generic programming tutorials | Serves beginners, not agent engineers |
| Beginner-only content | Outside target audience |
| Unconnected skill stubs | Violates P-02 and P-07 |
| Marketing-driven skills | Violates P-04 (no real utility) |
| Trend-chasing skills without production value | Violates P-03 |

---

## Article IV — Success Metrics

### M-01 — Graph Coverage

**Definition:** Percentage of known AI agent skill domains represented in the graph with ≥ 3 nodes.  
**Target:** ≥ 80% of 15 defined categories have ≥ 3 nodes.  
**Current (2026-06-16):** 2 of 15 categories meet threshold (09-agentic-patterns: 24, 03-memory: 5). **Status: 13% — active Phase 1 work ongoing.**

### M-02 — Goal Coverage

**Definition:** Percentage of goals in `meta/GOAL_TAXONOMY.md` for which the graph can produce a minimum viable learning path (≥ 3 nodes, ≥ 2 edges, connected).  
**Target:** ≥ 90% of goals covered.  
**Current (2026-06-16):** G01, G02, G04, G08, G11 covered. G03, G05, G06 blocked on `01-perception` (0 nodes). Estimated ~45%. **Status: in progress.**

### M-03 — Recommendation Quality

**Definition:** For a given goal + skill level, the recommendation engine produces an ordered path where each step’s `REQUIRES` prerequisites are satisfied.  
**Target:** Zero broken prerequisite chains in any recommended path.  
**Measurement:** Automated path validation in CI (see `.github/workflows/`).

### M-04 — Production Relevance

**Definition:** Percentage of nodes tagged `stability: stable` or `stability: evolving`.  
**Target:** ≥ 75% of nodes are `stable` or `evolving`.  
**Current (2026-06-16):** 32/38 nodes = **84.2%. Target met.**

### M-05 — Agent Ecosystem Completeness

**Definition:** Coverage across the five core agent capability dimensions: perceive, reason, act, remember, coordinate.  
**Target:** Each dimension has ≥ 5 graph nodes.

| Dimension | Category | Nodes | Status |
|---|---|---|---|
| Perceive | `01-perception` | 0 | ❌ blocked |
| Reason | `02-reasoning` | 1 | ⚠️ weak |
| Act | `04-action-execution` + `07-tool-use` | 3 | ⚠️ weak |
| Remember | `03-memory` | 5 | ✅ met |
| Coordinate | `09-agentic-patterns` + `15-orchestration` | 26 | ✅ met |

---

## Article V — Governance Rules

### G-01 — Repository artifacts as source of truth

Conversation history, agent memory, and external documentation have no authority. The repository files are the only truth. Every agent session must rebuild state from:
1. `meta/MEMORY_STATE.md`
2. `meta/AGENT_SKILLS_MASTER_PLAN.md`
3. `meta/AGENT_SKILLS_BACKLOG.md`
4. `meta/DECISION_LOG.md`
5. All `meta/TASK_*_REPORT.md` files

### G-02 — Atomic commits

Every task must be completed in one atomic commit. A commit may not leave the graph in a partially-updated state. Node additions without corresponding edges are forbidden.

### G-03 — Immutable decision log

`meta/DECISION_LOG.md` is append-only. No entry may be deleted or modified. Future agents must read it before making architectural decisions.

### G-04 — Memory state update after every task

`meta/MEMORY_STATE.md` must be updated as part of every task commit. It is the canonical state checkpoint.

### G-05 — Backlog governance

Before executing any task:
1. Verify task status is `OPEN` in `meta/AGENT_SKILLS_BACKLOG.md`
2. Verify all dependencies are `DONE`
3. Verify the task has not already been partially implemented
4. If already implemented: STOP and write a `meta/TASK_XXX_SKIP_REPORT.md` explaining why no action was taken

### G-06 — No partial Phase skipping

Phase 2 tasks may not begin until Phase 1 node targets are met (≥ 53 nodes). Phase ordering is enforced.

---

## Article VI — Amendment Process

1. Amendments must be proposed in a GitHub Issue with label `constitution-amendment`
2. The SamoTech Architect must approve before merging
3. Approved amendments are appended to the relevant Article — no original text may be deleted
4. Each amendment includes: date, author, rationale, and the specific text change
5. Amendments take effect on merge to `main`

---

## Article VII — Conflict Resolution

When two principles conflict, apply this priority order:

1. **P-06 (Zero duplicates)** — Never add a duplicate, regardless of other pressure
2. **P-07 (Connect before expand)** — Connection completeness before growth
3. **P-02 (Relationships first)** — Edges before documents
4. **P-05 (Goal connectivity)** — Orphan skills must be resolved
5. **P-03 (Production first)** — Academic skills yield to production skills
6. All other principles — resolved by architect judgment

---

## Appendix A — Graph State at Ratification

| Metric | Value |
|---|---|
| Nodes | 38 |
| Edges | 72 |
| Phase | 1 In Progress |
| Last task | TASK-001 (2026-06-16) |
| Next tasks | TASK-002, TASK-003, TASK-005 |
| Commit | `a88d423c3d48b225e649240a52cbc87f31367ba3` |

---

## Appendix B — Ratification Statement

This constitution was ratified on 2026-06-16 by the SamoTech Architect.  
It supersedes any conflicting guidance in `meta/ROADMAP.md`, `meta/ROADMAP_V2.md`, or earlier planning documents.  
All agents, automated systems, and contributors operating on this repository are bound by it from this date forward.

---

*Project Constitution v1.0.0 — SamoTech/skills-tree — Ratified 2026-06-16*
