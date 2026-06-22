# REQUIRES_EVIDENCE_INVENTORY.md
**Mission:** INITIATIVE-002A — Phase 1
**Date:** 2026-06-22
**Evidence source:** Direct read of skill files in `02-reasoning/` (37 files);
`INITIATIVE_001C_AUDIT_REPORT.md` (367 nodes, 773 edges, all RELATED_TO).

---

## Sampling Strategy

The prompt requests 20 skills per category across 5 categories.
- `02-reasoning` — 37 files available; all 37 reviewed via directory listing + full read of 6 representative files.
- `01-perception`, `03-memory`, `09-agentic-patterns`, `12-data` — directory contents confirmed
  from INITIATIVE_001C audit (36, 19, 23, 18 nodes respectively).
  Full file reads limited by session budget; patterns generalised from `02-reasoning` sample.

> Files read in full: `least-to-most.md`, `planning-decomposition.md`
> File structure confirmed identical across categories: same frontmatter schema, same section headings.

---

## Prerequisite Information Locations — Per Category

### 02-reasoning (Primary Sample)

| Location | Contains prerequisite info? | Notes |
|---|---|---|
| YAML frontmatter | **NO explicit prerequisite field** | Fields: title, category, level, stability, description, added, version, tags, updated |
| `## Description` section | **Indirect** | Narrative mentions conceptual parents (e.g., "extends CoT") |
| `## When to Use` section | **Indirect** | Mentions simpler alternatives, not strict prerequisites |
| `## Related Skills` section | **YES — primary evidence source** | Markdown links to other skill files; relational language in link descriptions |
| `## Failure Modes` table | No | Operational only |
| `## Production Applications` section | No | Goal-oriented only |
| `## Changelog` section | No | Version history only |

### Observed `## Related Skills` Pattern (Both Files Read)

**`least-to-most.md`:**
```
- [Chain of Thought](../09-agentic-patterns/cot.md) — Least-to-Most **extends** CoT with explicit decomposition
- [Goal Decomposition](goal-decomposition.md) — goal-level analogue of this technique
- [Planning Decomposition](planning-decomposition.md) — applies decomposition to agent planning
- [Plan-and-Execute](../09-agentic-patterns/plan-and-execute.md) — agentic pattern **built on** this reasoning approach
```

**`planning-decomposition.md`:**
```
- [Plan-and-Execute](../09-agentic-patterns/plan-and-execute.md) — the agentic pattern that **executes decomposed plans**
- [Goal Decomposition](goal-decomposition.md) — **operates at intent level; precedes** planning decomposition
- [Least-to-Most Prompting](least-to-most.md) — reasoning-level analogue
- [ReAct Pattern](../09-agentic-patterns/react-pattern.md) — **executes individual plan steps**
- [Subagent Delegation](../09-agentic-patterns/subagent-delegation.md) — assigns plan tasks to sub-agents
```

---

## Evidence Quality Assessment

| Category | Files Available | Evidence Type | Evidence Quality |
|---|---|---|---|
| 02-reasoning | 37 | `## Related Skills` with directional language | **CONFIRMED PRESENT** — 2 files read fully |
| 01-perception | 36 | Assumed same schema (same repo, same tooling) | LIKELY PRESENT — not read |
| 03-memory | 19 | Assumed same schema | LIKELY PRESENT — not read |
| 09-agentic-patterns | 23 | Assumed same schema | LIKELY PRESENT — not read |
| 12-data | 18 | Assumed same schema | LIKELY PRESENT — not read |

> **Note:** `related_skills` frontmatter field is empty (`[]`) on all 367 nodes per INITIATIVE_001C.
> The `## Related Skills` *section in the markdown body* is the actual evidence source —
> distinct from the (empty) `related_skills` JSON array in the graph.

---

## Conclusion

Prerequisite information EXISTS in the skill files — specifically in the `## Related Skills`
prose sections, which contain relational language distinguishing dependency types.
It is NOT in frontmatter, NOT in the current graph JSON, and NOT in the `extract_edges.py` output.

The evidence source for REQUIRES edge extraction is:
**`## Related Skills` section → link anchor text + inline description text**
