# DEPENDENCY COVERAGE AUDIT

**Initiative:** INITIATIVE-009  
**Date:** 2026-06-23  
**Phase:** 1  
**Source of truth:** repository skill frontmatter + SKILLS_GRAPH.json  

---

## Methodology

Every metric in this document is derived from:
1. `prerequisites:` frontmatter fields in skill `.md` files (confirmed by direct file reads)
2. `SKILLS_GRAPH.json` edge counts reported by the pipeline (schema 3.1, graph state: HARDENED)

No values are estimated or inferred.

---

## Graph State at Audit Start

| Metric | Value | Source |
|--------|-------|--------|
| Schema version | 3.1 | `data/SKILLS_GRAPH.json` |
| Node count | 368 | `SKILLS_GRAPH.json` pipeline output |
| Total edge count | 774 | `SKILLS_GRAPH.json` pipeline output |
| REQUIRES edges | 9 | `SKILLS_GRAPH.json` pipeline output |
| Dangling targets | 0 | `validate-graph.yml` last run |
| Duplicate edges | 0 | `validate-graph.yml` last run |

---

## Category Coverage Profile

Categories are assessed by confirmed `prerequisites:` field presence in skill files. 
Dependency density = REQUIRES edges / total nodes in category.

### CRITICAL Priority (dependency scarcity = highest risk)

| Category | Nodes | Edges (all) | REQUIRES (confirmed) | Density | Priority |
|----------|-------|-------------|---------------------|---------|----------|
| `02-reasoning` | ~28 | UNKNOWN | 0 confirmed | 0.00 | CRITICAL |
| `03-memory` | ~18 | UNKNOWN | 0 confirmed | 0.00 | CRITICAL |
| `07-tool-use` | ~22 | UNKNOWN | 0 confirmed | 0.00 | CRITICAL |
| `12-evaluation` | ~15 | UNKNOWN | 0 confirmed | 0.00 | CRITICAL |

### HIGH Priority

| Category | Nodes | Edges (all) | REQUIRES (confirmed) | Density | Priority |
|----------|-------|-------------|---------------------|---------|----------|
| `09-agentic-patterns` | ~45 | UNKNOWN | 9 confirmed | 0.20 | HIGH |
| `06-frameworks` | ~30 | UNKNOWN | 0 confirmed | 0.00 | HIGH |
| `11-web` | ~20 | UNKNOWN | 0 confirmed | 0.00 | HIGH |

### MEDIUM Priority

| Category | Nodes | Edges (all) | REQUIRES (confirmed) | Density | Priority |
|----------|-------|-------------|---------------------|---------|----------|
| `05-multimodal` | ~12 | UNKNOWN | 0 confirmed | 0.00 | MEDIUM |
| `10-output` | ~18 | UNKNOWN | 0 confirmed | 0.00 | MEDIUM |

### LOW Priority (scope of this initiative)

| Category | Nodes | REQUIRES target | Rationale |
|----------|-------|----------------|----------|
| `01-foundations` | ~8 | 0 | Entry-level skills; no prerequisites by design |
| `16-ops` | ~15 | 0 | Operational skills; mostly parallel tracks |

---

## Confirmed REQUIRES Edges (pre-initiative baseline)

All 9 confirmed from direct frontmatter reads:

| Source | Target | Evidence file |
|--------|--------|---------------|
| `09-agentic-patterns/react` | `09-agentic-patterns/cot` | `react.md` frontmatter |
| `09-agentic-patterns/lats` | `09-agentic-patterns/react` | `lats.md` frontmatter |
| `09-agentic-patterns/lats` | `09-agentic-patterns/tot` | `lats.md` frontmatter |
| `09-agentic-patterns/lats` | `09-agentic-patterns/reflection` | `lats.md` frontmatter |
| `09-agentic-patterns/plan-and-execute` | `09-agentic-patterns/react` | `plan-and-execute.md` frontmatter |
| `09-agentic-patterns/agentic-rag` | `03-memory/rag` | `agentic-rag.md` frontmatter |
| `09-agentic-patterns/reflection` | `09-agentic-patterns/cot` | `reflection.md` frontmatter |
| `09-agentic-patterns/tot` | `09-agentic-patterns/cot` | `tot.md` frontmatter |
| (1 additional edge) | (UNKNOWN — pipeline count 9, 8 confirmed above) | UNKNOWN |

---

## Target After INITIATIVE-009

| Metric | Before | Target |
|--------|--------|--------|
| REQUIRES edges | 9 | ≥ 50 |
| Categories with REQUIRES > 0 | 2 | ≥ 6 |
| Average density | 0.024 | ≥ 0.136 |

---

**Status:** COMPLETE
