# REQUIRES_CONFIDENCE_MODEL.md
**Mission:** INITIATIVE-002A — Phase 3
**Date:** 2026-06-22
**Based on:** Patterns confirmed in `REQUIRES_PATTERN_CATALOG.md`

---

## Model Definition

Only evidence from the `## Related Skills` section of skill `.md` files is admitted.
No semantic inference. No AI-guessed dependency. Only explicit textual evidence.

---

## Classification Levels

### LEVEL 1 — Explicit Prerequisite Statement
**Definition:** The skill file contains the exact words "prerequisite", "requires", "must understand",
"before learning", or "depends on" followed by a link or named skill.

**Admitted for REQUIRES edge:** YES — unconditionally.
**Confidence assignment in graph:** `"high"`
**Confirmed count in corpus:** 0 (zero files read contain this pattern)

---

### LEVEL 2 — Structured Prerequisite Field
**Definition:** A YAML frontmatter field explicitly named `prerequisites`, `requires`, `depends_on`,
or `before_learning` containing one or more skill references.

**Admitted for REQUIRES edge:** YES — unconditionally.
**Confidence assignment in graph:** `"high"`
**Confirmed count in corpus:** 0 (INITIATIVE_001C confirmed frontmatter fields for all 367 nodes;
no `prerequisites` field exists in the schema or any node)

---

### LEVEL 3 — Strong Dependency Wording
**Definition:** The `## Related Skills` bullet description contains directional language that
unambiguously implies ordered learning or execution dependency.

**Admitted trigger phrases (case-insensitive):**
| Phrase | Edge Direction | Interpretation |
|---|---|---|
| "X **extends** Y" | Y → X (Y REQUIRED_BY X) | X cannot exist without Y |
| "**built on** Y" | Y → X | X built on top of Y |
| "**executes** [the/a] plan/steps from Y" | Y → X | X requires Y output as input |
| "**precedes** X" | Y → X | Explicit ordering statement |
| "**foundation for** X" | Y → X | Y is foundational prerequisite |
| "**advanced version of** Y" | Y → X | X is advanced extension of Y |
| "**requires** Y" | Y → X | Direct dependency |
| "**builds on** Y" | Y → X | Incremental extension |

**Admitted for REQUIRES edge:** YES — with mandatory human review flag on each candidate.
**Confidence assignment in graph:** `"medium"`
**Confirmed count in read files:** 5 (across 2 files)

---

### LEVEL 4 — Weak Recommendation Wording
**Definition:** Language indicating relatedness but NOT ordering or dependency.

**Rejected trigger phrases:**
| Phrase | Reason for rejection |
|---|---|
| "analogue of" | Lateral relationship, not hierarchical |
| "similar to" | Equivalence, not dependency |
| "see also" | Navigation hint only |
| "compare with" | No ordering implied |
| "complements" | Bidirectional, not directed |
| "applies X to Y" | Method application, not prerequisite |
| "related to" | Generic — insufficient |

**Admitted for REQUIRES edge:** NO.
**Use:** RELATED_TO edges only (already represented in graph).

---

## Decision Table

| Level | Admitted? | Confidence | Review Required? |
|---|---|---|---|
| LEVEL 1 | ✅ YES | `high` | No |
| LEVEL 2 | ✅ YES | `high` | No |
| LEVEL 3 | ✅ YES | `medium` | YES — human review flag |
| LEVEL 4 | ❌ NO | n/a | n/a |

---

## Extraction Rules

1. Edge direction: if file A says "B precedes A" or "A extends B" → edge is `B → A` (REQUIRES).
2. If file A says "A executes plans from B" → edge is `B → A` (REQUIRES).
3. If the relationship is described mutually as "analogue" in both files → RELATED_TO only.
4. A single LEVEL 3 phrase is sufficient to generate one candidate edge.
5. No edge generated from `## Description` prose — only `## Related Skills` section.
6. No edge generated from `## Production Applications` section.
7. Target node must exist in `data/SKILLS_GRAPH.json` node IDs — else edge is DEFERRED.
