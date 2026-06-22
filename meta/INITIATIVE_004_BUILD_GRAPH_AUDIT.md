# build_graph.py Audit

**Mission:** INITIATIVE-004 Phase 1  
**Date:** 2026-06-22  
**Source:** `tools/build_graph.py` (SHA: f84c8e008ad17ba2f357107f7df98fab2f80fa44)

---

## Frontmatter Parser

**Function:** `parse_frontmatter(md_path)`

A frontmatter parser already existed in `build_graph.py` prior to INITIATIVE-004. However, it only supported simple `key: value` lines. It did not support YAML block sequences:

```yaml
# Unsupported before INITIATIVE-004:
prerequisites:
  - 02-reasoning/chain-of-thought
  - 02-reasoning/planning
```

The parser iterated lines and used `key, _, val = line.partition(":")` to split. For a block sequence key (empty val after colon), it would store `result["prerequisites"] = ""` — a string, not a list.

**Change made:** Extended `parse_frontmatter()` to track list state. When a key has an empty value, it initialises a list and appends subsequent `- item` lines to it. The updated parser correctly returns:
```python
{"prerequisites": ["02-reasoning/chain-of-thought", "02-reasoning/planning"]}
```

---

## Node Construction Path

**Function:** `build_node(md_path, category)`

Before INITIATIVE-004, `build_node()` did not read `prerequisites` from frontmatter:
```python
# Before:
"tags": [],
"related_skills": [],
```

**Change made:** Added prerequisites extraction:
```python
raw_prereqs = fm.get("prerequisites", [])
prerequisites = raw_prereqs if isinstance(raw_prereqs, list) else []
return {
    ...
    "prerequisites": prerequisites,
    ...
}
```

The `isinstance` guard ensures that if the parser returns a string (malformed frontmatter), it is silently treated as an empty list rather than causing downstream errors.

---

## Edge Construction Path

**New function:** `build_prerequisite_edges(node)`

Added as a dedicated function separate from `extract_edges_from_file()` to maintain clear separation of concerns:
- `extract_edges_from_file()` — handles `## Related Skills` section (body text)
- `build_prerequisite_edges()` — handles frontmatter `prerequisites` field

Generated edge shape:
```json
{
  "source": "09-agentic-patterns/plan-and-execute",
  "target": "02-reasoning/chain-of-thought",
  "type": "REQUIRES",
  "evidence": "prerequisites: 02-reasoning/chain-of-thought",
  "source_file": "skills/09-agentic-patterns/plan-and-execute.md",
  "confidence": "high",
  "source_method": "frontmatter_prerequisite"
}
```

The `source_method` field distinguishes frontmatter-derived REQUIRES edges from body-text-derived REQUIRES edges for future auditing.

---

## Main Loop Changes

In `main()`, after body-text edge extraction, a second loop processes all nodes for prerequisite edges:

```python
# Source 2: frontmatter prerequisites → REQUIRES edges
for node in nodes:
    prereq_edges = build_prerequisite_edges(node)
    edges.extend(prereq_edges)
```

This runs after all nodes are built, so `known_ids` is fully populated before any REQUIRES edge is generated.

---

## Schema Version Bump

`SCHEMA_VERSION` constant updated: `"3.0"` → `"3.1"`

This means newly generated `data/SKILLS_GRAPH.json` will have `meta.schema_version = "3.1"`.

---

## Graph Meta Additions

`meta` section of `SKILLS_GRAPH.json` now includes:
- `requires_count`: integer count of REQUIRES edges
- `initiative`: updated to `"INITIATIVE-004"`
