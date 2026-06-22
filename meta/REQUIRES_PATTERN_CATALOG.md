# REQUIRES_PATTERN_CATALOG.md
**Mission:** INITIATIVE-002A — Phase 2
**Date:** 2026-06-22
**Method:** Exact text extracted from fully-read skill files; patterns generalised across sample.

---

## Extraction Method

All patterns sourced from `## Related Skills` section inline description text.
Pattern matching applied to the description fragment after the ` — ` separator in each bullet.

---

## Pattern Registry

### LEVEL 1 — Explicit Prerequisite Statements
> Direct "requires", "prerequisite", "must understand before" language.

| Occurrence | Exact Text | Source File | Candidate Edge Direction |
|---|---|---|---|
| 0 confirmed | — | — | — |

**Count: 0**
No "prerequisite:", "requires:", or "must understand" phrasing found in the two files read.
Cannot assert count for unread files without evidence.

---

### LEVEL 2 — Structured Prerequisite Fields
> A dedicated frontmatter or section field named `prerequisites`, `depends_on`, `requires`, `before_learning`.

| Occurrence | Exact Text | Source File |
|---|---|---|
| 0 confirmed | — | — |

**Count: 0**
YAML frontmatter fields confirmed: `title`, `category`, `level`, `stability`, `description`,
`added`, `version`, `tags`, `updated`. No `prerequisites` field exists.

---

### LEVEL 3 — Strong Dependency Wording
> Language implying ordered dependency: "extends", "precedes", "built on", "executes",
> "operates before", "foundation for", "builds on", "advanced version of".

| # | Exact Text | Source File | Pattern Keyword |
|---|---|---|---|
| 1 | "Least-to-Most **extends** CoT with explicit decomposition" | `02-reasoning/least-to-most.md` | extends |
| 2 | "the agentic pattern **built on** this reasoning approach" | `02-reasoning/least-to-most.md` | built on |
| 3 | "the agentic pattern that **executes** decomposed plans" | `02-reasoning/planning-decomposition.md` | executes |
| 4 | "**operates at intent level; precedes** planning decomposition" | `02-reasoning/planning-decomposition.md` | precedes |
| 5 | "**executes individual plan steps**" | `02-reasoning/planning-decomposition.md` | executes |
| 6 | "assigns plan tasks to sub-agents" | `02-reasoning/planning-decomposition.md` | assigns (weak) |

**Count in read files: 5 confirmed LEVEL 3 instances across 2 files**
**Projected across 37 `02-reasoning` files (avg 2.5/file): ~92 instances in `02-reasoning` alone** (ESTIMATED)
**Projected across all 367 files (avg 2.5/file): ~917 instances** (ESTIMATED — not evidenced)

---

### LEVEL 4 — Weak Recommendation Wording
> "related", "analogue", "similar to", "see also", "compare with", "complements".

| # | Exact Text | Source File | Pattern Keyword |
|---|---|---|---|
| 1 | "goal-level **analogue** of this technique" | `02-reasoning/least-to-most.md` | analogue |
| 2 | "reasoning-level **analogue**" | `02-reasoning/planning-decomposition.md` | analogue |
| 3 | "applies decomposition to agent planning" | `02-reasoning/least-to-most.md` | applies (neutral) |

**Count in read files: 3 confirmed LEVEL 4 instances across 2 files**

---

## Confirmed Counts (Evidence-Only)

| Level | Confirmed Count | Source Coverage |
|---|---|---|
| LEVEL 1 (explicit prerequisite) | 0 | 2 files (5.4% of 02-reasoning) |
| LEVEL 2 (structured field) | 0 | 367/367 nodes confirmed via INITIATIVE_001C |
| LEVEL 3 (strong dependency) | 5 | 2 files (5.4% of 02-reasoning) |
| LEVEL 4 (weak recommendation) | 3 | 2 files (5.4% of 02-reasoning) |

> **Projected** totals marked as estimates; only confirmed counts used for edge generation.
