# MEMORY_STATE.md — Canonical Agent Memory Checkpoint

> **This file is the single source of truth for any agent resuming work on this repository.**  
> Read this first. Do not rely on conversation history.  
> Last updated: 2026-06-21 by Perplexity / SamoTech Architect

---

## Current Phase

**Phase 1 — Core Agent Skills**  
Status: **In Progress**  
Target Sprint: C-13  
Phase 1 objective: Reach 53 graph nodes covering `02-reasoning`, `09-agentic-patterns`, and `01-perception`.

---

## Current Sprint

**Sprint C-13** (Phase 1, first active sprint)

---

## Graph Metrics

| Metric | Value |
|---|---|
| Total nodes | **47** |
| Total edges | **93** |
| Schema version | 1.3 |
| Avg edge confidence | 0.899 |
| Graph file | `data/SKILLS_GRAPH.json` |

### Categories Covered (nodes ≥ 1)

| Category | Nodes | Notes |
|---|---|---|
| `02-reasoning` | **10** | TASK-003 DONE — 9 new nodes added |
| `03-memory` | 4 | `vector-search`, `rag-retrieval`, `embedding-generation`, `context-management` |
| `04-action-execution` | 1 | `error-recovery` |
| `05-code` | 1 | `code-generation` |
| `07-tool-use` | 2 | `function-calling`, `api-integration` |
| `09-agentic-patterns` | **24** | **Fully mapped** — TASK-001 DONE |
| `10-computer-use` | 1 | `browser-automation` |
| `11-web` | 1 | `web-scraping` |
| `12-data` | 1 | `data-extraction` |
| `15-orchestration` | 2 | `llm-orchestration`, `multi-agent-coordination` |

### Categories Missing (0 nodes — blocker for goals)

| Category | Priority | Blocked Goals |
|---|---|---|
| `01-perception` | HIGH | G03 (Browser Agent), G05, G06 |
| `06-knowledge` | MEDIUM | G02, G04 |
| `08-planning` | MEDIUM | G06, G08 |
| `13-execution` | LOW | G06 |
| `14-evaluation` | LOW | G11 |

---

## Completed Tasks

| Task ID | Title | Commit SHA | Date | Nodes Added | Edges Added |
|---|---|---|---|
| TASK-001 | Map `09-agentic-patterns/` to graph | `d47878dbef6c11e9932672d1747ab367eb6cb6c6` | 2026-06-16 | +23 | +59 |
| TASK-003 | Add advanced reasoning layer | _(see DECISION_LOG)_ | 2026-06-21 | +9 | +21 |

---

## Open Tasks (Phase 1 — no blockers)

| Task ID | Title | Deps | Est. Nodes | Est. Edges |
|---|---|---|---|---|
| TASK-002 | Add Context Engineering skills | None | +5 | +10–12 |
| TASK-005 | Add core perception skills (OCR, screen parsing) | None | +6 | +12–15 |

## Open Tasks (Phase 1 — have dependencies)

| Task ID | Title | Blocked By | Est. Nodes | Est. Edges |
|---|---|---|---|---|
| TASK-004 | Add causal + counterfactual reasoning | TASK-003 ✅ (unblocked) | +3 | +6–8 |
| TASK-006 | Add document/data perception skills | TASK-005 | +9 | +15–18 |

---

## Blocked Tasks

TASK-007 through TASK-042 are blocked pending Phase 1 completion or specific Phase 2 prerequisites. See `meta/AGENT_SKILLS_BACKLOG.md` for full dependency chains.

---

## Top Priority Next Actions

1. **Execute TASK-002** (Add Context Engineering skills) — no deps, Phase 1, creates 5 new nodes
2. **Execute TASK-004** (Causal + counterfactual reasoning) — now unblocked by TASK-003 completion
3. **Execute TASK-005** (Core perception layer) — no deps, unlocks G03 Browser Agent goal path
4. After TASK-005: execute TASK-006 (document/data perception)

**Do not skip to Phase 2 tasks** — Phase 1 targets are 53 nodes (currently at 47, need +6 more).

---

## Anti-Drift Checklist

Before adding any node, verify:
- [ ] Node ID `skill:kebab-case` does not already exist in `data/SKILLS_GRAPH.json`
- [ ] Concept is not covered by an existing node under a different name
- [ ] Category directory is correct

### Existing Node IDs (47 total — do not duplicate)

`skill:code-generation`, `skill:prompt-engineering`, `skill:function-calling`, `skill:web-scraping`, `skill:browser-automation`, `skill:vector-search`, `skill:rag-retrieval`, `skill:embedding-generation`, `skill:llm-orchestration`, `skill:multi-agent-coordination`, `skill:workflow-automation`, `skill:error-recovery`, `skill:context-management`, `skill:api-integration`, `skill:data-extraction`, `skill:react-pattern`, `skill:cot`, `skill:tot`, `skill:reflection-pattern`, `skill:plan-and-execute`, `skill:rag-pattern`, `skill:agent-as-tool`, `skill:agent-handoffs`, `skill:agentic-rag`, `skill:bootstrapping-pattern`, `skill:constitutional-ai`, `skill:critic-agent`, `skill:debate-pattern`, `skill:interruptible-agent-flows`, `skill:lats`, `skill:mcts-pattern`, `skill:memory-augmented-agent`, `skill:mixture-of-agents`, `skill:rag-pipeline`, `skill:self-play-pattern`, `skill:subagent-delegation`, `skill:time-travel-debugging`, `skill:tool-use-loop`, `skill:self-consistency`, `skill:step-back-prompting`, `skill:least-to-most`, `skill:meta-prompting`, `skill:planning-decomposition`, `skill:hypothesis-generation`, `skill:goal-decomposition`, `skill:reasoning-under-uncertainty`, `skill:analogical-reasoning`

---

## Known Risks

| Risk | Severity | Mitigation |
|---|---|---|
| `01-perception` has 0 nodes — G03 Browser Agent cannot be recommended | HIGH | TASK-005 must be in next sprint |
| TASK-007+ blocked until Phase 1 complete | MEDIUM | Expected — by design |

---

## Recent Commits

| SHA | Message | Date |
|---|---|---|
| `d47878dbef6c11e9932672d1747ab367eb6cb6c6` | `feat(graph): TASK-001 — map 23 agentic-pattern skills to graph` | 2026-06-16 |
| `0b699a4cd2007a7f302fef15f873bf07c1af3555` | `chore(governance): persistent-memory bootstrap after TASK-001` | 2026-06-16 |
| _(TASK-003 SHA — see DECISION_LOG.md)_ | `feat(graph): TASK-003 advanced reasoning layer` | 2026-06-21 |

---

## Phase 1 Completion Target

| Stage | Nodes | Status |
|---|---|---|
| Baseline (pre-TASK-001) | 15 | — |
| After TASK-001 | 38 | ✓ DONE |
| After TASK-003 | **47** | ✓ DONE |
| After TASK-002 + TASK-004 | ~55 | OPEN |
| Phase 1 target | **53** | In Progress |

**Phase 1 completion: 88.7% of node target (47/53)**

---

*Memory State version: 1.1.0 — Updated 2026-06-21 (TASK-003)*
