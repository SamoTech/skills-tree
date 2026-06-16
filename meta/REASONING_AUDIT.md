# REASONING_AUDIT.md — Phase 1 Audit of skills/02-reasoning/

> **Task:** TASK-003 Pre-execution audit
> **Date:** 2026-06-16
> **Auditor:** Perplexity / SamoTech Architect
> **Status:** COMPLETE — cleared for node additions

---

## Audit Scope

Directory: `skills/02-reasoning/`
Graph category: `02-reasoning`
Graph nodes mapped to this category before TASK-003: **1** (`skill:prompt-engineering`)

---

## Anti-Drift Check (TASK-003 Critical)

The following nodes already exist in `data/SKILLS_GRAPH.json` and **must NOT be re-added**:

| Node ID | Category in Graph | Risk |
|---|---|---|
| `skill:cot` | `09-agentic-patterns` | HIGH — file `chain-of-thought.md` exists in 02-reasoning |
| `skill:tot` | `09-agentic-patterns` | HIGH — file `tree-of-thought.md` exists in 02-reasoning |
| `skill:react-pattern` | `09-agentic-patterns` | HIGH — file `react.md` exists in 02-reasoning |
| `skill:reflection-pattern` | `09-agentic-patterns` | MEDIUM — file `self-reflection.md` exists in 02-reasoning |
| `skill:prompt-engineering` | `02-reasoning` | MEDIUM — already the 1 mapped node |

**Decision:** All five above are SKIPPED. TASK-003 adds only the 9 specified target nodes.

---

## File Inventory (39 files in 02-reasoning/)

| File | Graph Node Exists? | TASK-003 Target? | Duplicate Risk | Notes |
|---|---|---|---|---|
| `README.md` | N/A | No | None | Category readme |
| `abductive.md` | No | No | Low | Phase 2 candidate |
| `analogical.md` | No | **YES** | None | Maps to `skill:analogical-reasoning` |
| `analogy-generation.md` | No | No | HIGH | Conceptual overlap with analogical.md — do not duplicate |
| `argument-structure-analysis.md` | No | No | Low | Phase 2 candidate |
| `bayesian-reasoning.md` | No | No | Low | Phase 2 candidate |
| `causal.md` | No | No | Low | TASK-004 scope (causal reasoning) |
| `chain-of-thought.md` | **YES** (`skill:cot`) | No | **CRITICAL** | Duplicate risk — node already in graph as `09-agentic-patterns` |
| `commonsense.md` | No | No | Low | Phase 2 candidate |
| `constraint-satisfaction.md` | No | No | Low | Phase 2 candidate |
| `counterfactual-reasoning.md` | No | No | Low | TASK-004 scope |
| `decision-making.md` | No | No | Low | Phase 2 candidate |
| `deductive-reasoning.md` | No | No | Low | Phase 2 candidate |
| `ethical-reasoning.md` | No | No | Low | Phase 2 candidate |
| `goal-setting.md` | No | No | MEDIUM | Conceptual overlap with `goal-decomposition` — reviewed, distinct |
| `hypothesis-generation.md` | No | **YES** | None | Maps to `skill:hypothesis-generation` |
| `inductive-reasoning.md` | No | No | Low | Phase 2 candidate |
| `mathematical-reasoning.md` | No | No | Low | Phase 2 candidate |
| `meta-cognition.md` | No | No | MEDIUM | Partial overlap with `meta-prompting` — reviewed, distinct |
| `multi-step-planning.md` | No | No | MEDIUM | Overlap with `planning-decomposition` — reviewed, distinct (planning-decomposition is the target) |
| `numerical-estimation.md` | No | No | Low | Phase 2 candidate |
| `planning.md` | No | No | MEDIUM | `plan-and-execute` already in graph; `planning-decomposition` is the cognitive sub-skill |
| `prioritization.md` | No | No | Low | Phase 2 candidate |
| `probabilistic-reasoning.md` | No | No | Low | Phase 2 candidate |
| `problem-decomposition.md` | No | No | MEDIUM | Partial overlap with `goal-decomposition` — reviewed, distinct |
| `react.md` | **YES** (`skill:react-pattern`) | No | **CRITICAL** | Duplicate risk — node in graph |
| `risk-assessment.md` | No | No | Low | Phase 2 candidate |
| `root-cause-analysis.md` | No | No | Low | Phase 2 candidate |
| `scenario-planning.md` | No | No | Low | Phase 2 candidate |
| `self-consistency.md` | No | **YES** | None | Maps to `skill:self-consistency` |
| `self-correction.md` | No | No | MEDIUM | `reflection-pattern` covers correction loop; self-correction is a sub-behaviour |
| `self-reflection.md` | **YES** (`skill:reflection-pattern`) | No | **CRITICAL** | Duplicate risk — node in graph |
| `socratic-questioning.md` | No | No | Low | Phase 2 candidate |
| `spatial-reasoning.md` | No | No | Low | Phase 2 candidate |
| `systems-thinking.md` | No | No | Low | Phase 2 candidate |
| `task-decomposition.md` | No | No | MEDIUM | Reviewed vs `goal-decomposition` — distinct (task-decomposition is execution-level) |
| `temporal-reasoning.md` | No | No | Low | Phase 2 candidate |
| `trade-off-analysis.md` | No | No | Low | Phase 2 candidate |
| `tree-of-thought.md` | **YES** (`skill:tot`) | No | **CRITICAL** | Duplicate risk — node in graph |
| `uncertainty-quantification.md` | No | No | MEDIUM | Overlap with `reasoning-under-uncertainty` — reviewed, distinct (RuU is reasoning approach; UQ is a measurement technique) |

---

## TASK-003 Target Node Mapping

| Target Node ID | Source File | Category | Justification |
|---|---|---|---|
| `skill:self-consistency` | `self-consistency.md` | `02-reasoning` | Wang et al. 2022; used in LangChain, DSPy, Claude |
| `skill:step-back-prompting` | *(new file)* | `02-reasoning` | Zheng et al. 2023; used in production RAG pipelines |
| `skill:least-to-most` | *(new file)* | `02-reasoning` | Zhou et al. 2022; used in LangChain decomposition chains |
| `skill:meta-prompting` | *(new file)* | `02-reasoning` | Zhang et al. 2024; used in AutoGen, Semantic Kernel |
| `skill:planning-decomposition` | `multi-step-planning.md` (extends) | `02-reasoning` | LangGraph planning nodes, CrewAI task breakdown |
| `skill:hypothesis-generation` | `hypothesis-generation.md` | `02-reasoning` | Used in research agents (GPT-Researcher, AutoGen) |
| `skill:goal-decomposition` | *(new file)* | `02-reasoning` | LangGraph SubGraph, AutoGen nested agents, BabyAGI |
| `skill:reasoning-under-uncertainty` | *(new file)* | `02-reasoning` | GPT-4 reasoning, Anthropic extended thinking, LangChain |
| `skill:analogical-reasoning` | `analogical.md` | `02-reasoning` | Used in code translation agents, domain adaptation |

---

## Duplicate Risk Assessment Summary

| Risk Level | Count | Action |
|---|---|---|
| CRITICAL (node already exists) | 5 files | SKIP — do not add |
| HIGH (conceptual overlap) | 2 files | SKIP — covered by existing or target nodes |
| MEDIUM (partial overlap, reviewed) | 6 files | SKIP in TASK-003, Phase 2 candidates |
| Low (no overlap) | 26 files | Phase 2/3 candidates |

---

## Pre-Execution Gate

- [x] Anti-drift check complete
- [x] 5 existing nodes identified and locked out
- [x] 9 target nodes confirmed unique (no ID conflict, no conceptual duplicate)
- [x] Source files mapped
- [x] Cleared for TASK-003 execution

---

*REASONING_AUDIT.md — Generated by TASK-003 Phase 1 audit — 2026-06-16*
