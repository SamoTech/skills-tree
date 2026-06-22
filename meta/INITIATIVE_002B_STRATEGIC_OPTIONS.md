# Strategic Options: Dependency Model

**Mission:** INITIATIVE-002B Phase 4  
**Date:** 2026-06-22

---

## Context

- 367 nodes, 773 edges, 0 REQUIRES edges (confirmed)
- `recommend.py` BFS is blocked without REQUIRES edges
- Extraction engine (`extract_edges.py`) is ready — schema and authoring convention are the gaps
- 5 LEVEL 3 candidates exist across the entire corpus

---

## Option A — Continue Extracting REQUIRES Edges from Existing Content

**Description:** Run `extract_edges.py` against all 367 skill files as-is. Accept only LEVEL 3 matches. No schema changes, no authoring changes.

| Dimension | Assessment |
|---|---|
| Implementation effort | Very low — tool already built |
| Maintenance burden | High — dependency information lives only in prose; changes to prose silently lose edges |
| Accuracy | Very low — only 5 candidates found from 367 nodes (1.4% coverage) |
| Scalability | Does not scale — requires authors to write prose in exact keyword patterns |
| Governance impact | Minimal — no schema changes needed |

**Verdict:** Produces a negligible REQUIRES graph. `recommend.py` remains non-functional. **Not recommended as sole strategy.**

---

## Option B — Add Prerequisite Metadata to Skill Schema

**Description:** Add a `prerequisites` array field to `schema/skill.schema.json`. Update all skill `.md` files to declare prerequisites in frontmatter. Extract_edges.py already has code for frontmatter source (Source 2 in its docstring).

| Dimension | Assessment |
|---|---|
| Implementation effort | High — schema change + backfill of 367 skill files + validation pipeline update |
| Maintenance burden | Low — prerequisites are explicit, machine-readable, version-controlled, validated |
| Accuracy | High — human-authored, not regex-extracted |
| Scalability | High — every new skill declares its own prerequisites at authoring time |
| Governance impact | Medium — requires schema version bump, contribution guide update, CI validation |

**Verdict:** Correct long-term architecture. High upfront cost. **Recommended as the target model.** However, backfilling 367 files is a large initiative that should not block `recommend.py` in the short term.

---

## Option C — Hybrid Model

**Description:** 
1. **Immediately:** Use extraction (Option A) to add the 5 confirmed LEVEL 3 candidates. Unblocks pilot testing of `recommend.py`.
2. **Medium term:** Add `prerequisites` field to schema (Option B). Update contribution guide. Add CI schema validation.
3. **Long term:** Incrementally backfill prerequisites per category, starting with high-centrality nodes.

| Dimension | Assessment |
|---|---|
| Implementation effort | Low immediate / High medium-term |
| Maintenance burden | Decreases over time as schema-based prerequisites replace extracted ones |
| Accuracy | Low initially, improves with each schema-based skill update |
| Scalability | Scales with Option B adoption |
| Governance impact | Requires phased schema change with migration path |

**Verdict:** Pragmatic path that unblocks `recommend.py` without waiting for full backfill. **Recommended.** Extraction and schema authoring are complementary, not competing — the hybrid uses extraction as a bootstrap and schema authoring as the long-term source of truth.

---

## Decision Matrix

| Criterion | Option A | Option B | Option C |
|---|---|---|---|
| Time to first REQUIRES edges | Days | Weeks–months | Days |
| `recommend.py` viability | No (1.4% coverage) | Yes (full backfill) | Partial → full |
| Schema integrity | Maintained | Improved | Improved (phased) |
| Author experience | Unchanged (poor) | Clear expectation | Improved (phased) |
| **Recommended** | — | Long-term target | **YES** |
