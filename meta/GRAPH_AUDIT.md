# GRAPH_AUDIT.md — Authoritative Graph Audit

> Rebuilt from direct measurement of `data/SKILLS_GRAPH.json` on 2026-06-21.  
> No estimates. All values measured.

---

## Measurement Summary

| Metric | Value |
|---|---|
| Total nodes | **47** |
| Total edges | **93** |
| Schema version | 1.3 |
| Avg confidence | 0.899 |
| Measurement date | 2026-06-21 |

---

## Node Distribution by Category

| Category | Nodes | Node IDs |
|---|---|---|
| `02-reasoning` | 10 | `prompt-engineering`, `self-consistency`, `step-back-prompting`, `least-to-most`, `meta-prompting`, `planning-decomposition`, `hypothesis-generation`, `goal-decomposition`, `reasoning-under-uncertainty`, `analogical-reasoning` |
| `03-memory` | 4 | `vector-search`, `rag-retrieval`, `embedding-generation`, `context-management` |
| `04-action-execution` | 1 | `error-recovery` |
| `05-code` | 1 | `code-generation` |
| `07-tool-use` | 2 | `function-calling`, `api-integration` |
| `09-agentic-patterns` | 24 | `workflow-automation`, `react-pattern`, `cot`, `tot`, `reflection-pattern`, `plan-and-execute`, `rag-pattern`, `agent-as-tool`, `agent-handoffs`, `agentic-rag`, `bootstrapping-pattern`, `constitutional-ai`, `critic-agent`, `debate-pattern`, `interruptible-agent-flows`, `lats`, `mcts-pattern`, `memory-augmented-agent`, `mixture-of-agents`, `rag-pipeline`, `self-play-pattern`, `subagent-delegation`, `time-travel-debugging`, `tool-use-loop` |
| `10-computer-use` | 1 | `browser-automation` |
| `11-web` | 1 | `web-scraping` |
| `12-data` | 1 | `data-extraction` |
| `15-orchestration` | 2 | `llm-orchestration`, `multi-agent-coordination` |
| **TOTAL** | **47** | — |

---

## Edge Distribution by Type

| Edge Type | Count |
|---|---|
| REQUIRES | 51 |
| RECOMMENDED_WITH | 28 |
| LEARN_BEFORE | 10 |
| SUPPORTS | 4 |
| **TOTAL** | **93** |

---

## Top Hub Nodes (by total degree)

| Rank | Node ID | In | Out | Total | Centrality |
|---|---|---|---|---|---|
| 1 | `skill:prompt-engineering` | 10 | 1 | 11 | 0.2391 |
| 2 | `skill:cot` | 5 | 2 | 7 | 0.1522 |
| 2 | `skill:react-pattern` | 4 | 3 | 7 | 0.1522 |
| 2 | `skill:llm-orchestration` | 7 | 0 | 7 | 0.1522 |
| 5 | `skill:multi-agent-coordination` | 4 | 2 | 6 | 0.1304 |
| 5 | `skill:reflection-pattern` | 4 | 2 | 6 | 0.1304 |
| 5 | `skill:critic-agent` | 4 | 2 | 6 | 0.1304 |

---

## Sink Nodes (in-degree = 0 — no prerequisites mapped)

These nodes have no incoming edges, meaning nothing currently `REQUIRES` or `LEARN_BEFORE` them in the graph. They are entry points.

| Node ID | Category | Out-Degree |
|---|---|---|
| `skill:code-generation` | `05-code` | 2 |
| `skill:browser-automation` | `10-computer-use` | 2 |
| `skill:agentic-rag` | `09-agentic-patterns` | 3 |
| `skill:bootstrapping-pattern` | `09-agentic-patterns` | 2 |
| `skill:lats` | `09-agentic-patterns` | 3 |
| `skill:memory-augmented-agent` | `09-agentic-patterns` | 3 |
| `skill:mixture-of-agents` | `09-agentic-patterns` | 3 |
| `skill:self-play-pattern` | `09-agentic-patterns` | 3 |
| `skill:time-travel-debugging` | `09-agentic-patterns` | 3 |
| `skill:self-consistency` | `02-reasoning` | 2 |
| `skill:step-back-prompting` | `02-reasoning` | 2 |
| `skill:least-to-most` | `02-reasoning` | 2 |
| `skill:meta-prompting` | `02-reasoning` | 2 |
| `skill:hypothesis-generation` | `02-reasoning` | 2 |
| `skill:goal-decomposition` | `02-reasoning` | 3 |
| `skill:reasoning-under-uncertainty` | `02-reasoning` | 2 |
| `skill:analogical-reasoning` | `02-reasoning` | 2 |

---

## Terminal Nodes (out-degree = 0 — nothing flows from them)

| Node ID | Category | In-Degree |
|---|---|---|
| `skill:vector-search` | `03-memory` | 4 |
| `skill:llm-orchestration` | `15-orchestration` | 7 |
| `skill:error-recovery` | `04-action-execution` | 5 |
| `skill:context-management` | `03-memory` | 4 |
| `skill:api-integration` | `07-tool-use` | 2 |
| `skill:data-extraction` | `12-data` | 1 |

---

## Graph Integrity Checks

| Check | Result |
|---|---|
| Duplicate node IDs | ✅ None detected |
| Edges referencing non-existent nodes | ✅ None detected |
| Schema version consistency | ✅ 1.3 throughout |
| statistics block matches array counts | ✅ Matches (47 nodes, 93 edges) |
| DAG integrity (REQUIRES + LEARN_BEFORE only) | ✅ No directed cycles detected |

---

## Categories With 0 Nodes (gaps)

`01-perception`, `06-knowledge`, `08-planning`, `13-execution`, `14-evaluation`

---

*Audit version: 2.0.0 — 2026-06-21 Governance Reconciliation*
