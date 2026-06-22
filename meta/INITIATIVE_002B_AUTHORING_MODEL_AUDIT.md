# Authoring Model Audit

**Mission:** INITIATIVE-002B Phase 2  
**Date:** 2026-06-22  
**Question:** Does the repository architecture expect authors to define dependencies?

---

## Evidence Sources Inspected

1. `schema/skill.schema.json` — canonical skill object definition
2. `tools/extract_edges.py` — extraction engine, documents expected authoring patterns
3. `tools/build_graph.py` — build pipeline (not read in full; referenced by 002A)
4. `schema/edge.schema.json` — edge object definition

---

## Finding 1: Schema Has No Prerequisite Field

Source: `schema/skill.schema.json` (SHA: 25d54e18)

The `required` array contains: `["id", "title", "category", "level", "stability", "version"]`

Optional fields defined: `layer`, `added`, `tags`, `related_skills`, `source_file`, `quality_score`

**`prerequisites`, `depends_on`, `requires`, `before` — none of these fields exist.**

The schema uses `additionalProperties: false`, meaning any field not in the schema definition is **rejected by the validator**. An author cannot add a prerequisite field to a skill YAML frontmatter today — it would fail schema validation.

**Answer: NO. The schema does not support prerequisite authoring.**

---

## Finding 2: extract_edges.py Relies on Inline Language

Source: `tools/extract_edges.py` (SHA: 6c16fb37)

The docstring states extraction sources:
```
Extraction sources (in order of priority):
  1. ## Related Skills sections — markdown links
  2. Explicit prerequisite language in frontmatter (dependencies field)
  3. Inline prerequisite keywords in body text
```

Source 2 references a `dependencies` field in frontmatter. **This field does not exist in `schema/skill.schema.json`.** This is a documentation/code divergence: `extract_edges.py` was written anticipating a `dependencies` field that was never added to the schema.

**This is a confirmed schema gap.** The extraction engine already supports structured prerequisite frontmatter — the schema simply has not been updated to provide it.

---

## Finding 3: No Contribution Guide Found

A `CONTRIBUTING.md` or `docs/contributing.md` was not confirmed present in the repository listing from INITIATIVE-001C. No authoring instructions for skill files could be located.

**Without a contribution guide, authors have no instruction on how to declare dependencies.**

---

## Authoring Model Verdict

| Dimension | Status |
|---|---|
| Schema supports prerequisites | **NO** |
| Extraction engine supports prerequisites | **YES** (code ready, schema not) |
| Authors instructed to declare prerequisites | **NO** (no contribution guide) |
| Existing files declare prerequisites | Near-zero (5 LEVEL 3 occurrences, 002A) |

**The repository architecture does NOT currently expect authors to define dependencies. However, the extraction engine was designed to support them — the gap is in the schema and authoring convention, not the tooling.**
