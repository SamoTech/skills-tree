# Dependency Tool Alignment Audit

**Mission:** INITIATIVE-003 Phase 3  
**Date:** 2026-06-22  
**Sources:** `tools/extract_edges.py` (SHA: 6c16fb37), `tools/build_graph.py` (SHA: f84c8e00)

---

## Question: Can `prerequisites` already be consumed?

### tools/extract_edges.py

**Answer: PARTIAL — code supports frontmatter intent, but field name mismatch.**

The `extract_edges.py` docstring states:

```
Extraction sources (in order of priority):
  1. ## Related Skills sections — markdown links
  2. Explicit prerequisite language in frontmatter (dependencies field)
  3. Inline prerequisite keywords in body text
```

However, inspection of the full `extract_edges.py` source reveals that **Source 2 is not implemented in the current code body**. The function `extract_from_file()` only searches for the `## Related Skills` section (Source 1). There is no frontmatter parsing code in `extract_edges.py`.

**Finding:** Source 2 in the docstring is aspirational documentation — the implementation was not added. This is a second confirmed code/documentation divergence (first was the missing schema field).

**Required change for INITIATIVE-004:**
```python
# In extract_from_file(), after parsing frontmatter:
prerequisites = fm.get("prerequisites", [])  # new field from schema v3.1
for prereq_id in prerequisites:
    edges.append({
        "source": source_id,
        "target": prereq_id,
        "type": "REQUIRES",
        "evidence": f"prerequisites: {prereq_id}  # frontmatter declaration",
        "source_file": rel_path,
        "confidence": "high",
    })
```

Note: `extract_edges.py` does not currently parse YAML frontmatter — it only reads body text. A frontmatter parser must be added (same pattern as `build_graph.py`'s `parse_frontmatter()`).

---

### tools/build_graph.py

**Answer: NO — `prerequisites` field is not consumed.**

The `build_node()` function hardcodes the fields it copies from frontmatter:

```python
return {
    "id": skill_id,
    "title": fm.get("title", ...),
    "category": category,
    "layer": LAYER_MAP.get(category, "systems"),
    "level": fm.get("level", "basic"),
    "stability": fm.get("stability", "stable"),
    "version": fm.get("version", "v1"),
    "added": fm.get("added", None),
    "tags": [],                    # <-- NOT read from frontmatter
    "related_skills": [],          # <-- NOT read from frontmatter
    "source_file": ...,
    "quality_score": None,
    # prerequisites: NOT HERE
}
```

Four observations:
1. `prerequisites` is not read from frontmatter
2. `tags` is hardcoded to `[]` (not read from frontmatter either — separate known gap)
3. `related_skills` is hardcoded to `[]` (same issue)
4. `extract_edges_from_file()` in `build_graph.py` duplicates extraction logic from `extract_edges.py` — another divergence

**Required change for INITIATIVE-004:**
```python
# In build_node(), add prerequisites to node:
"prerequisites": fm.get("prerequisites", []),

# In extract_edges_from_file() or a new section, add REQUIRES edge generation:
for prereq_id in fm.get("prerequisites", []):
    edges.append({
        "source": source_id,
        "target": prereq_id,
        "type": "REQUIRES",
        "evidence": f"prerequisites: {prereq_id}",
        "source_file": rel_path,
        "confidence": "high",
    })
```

---

## Summary

| Tool | Can consume `prerequisites`? | Changes required |
|---|---|---|
| `extract_edges.py` | **NO** — frontmatter parser absent, docstring claim not implemented | Add frontmatter parser + Source 2 loop |
| `build_graph.py` | **NO** — `build_node()` does not read `prerequisites` | Add `prerequisites` to `build_node()` + REQUIRES edge loop |
| `schema/skill.schema.json` | **YES** (as of this commit) | ✅ Done |
| `schema/edge.schema.json` | **YES** — `REQUIRES` type already in enum | No change needed |

**INITIATIVE-004 scope:** Update `build_graph.py` and `extract_edges.py` to consume the `prerequisites` field and emit `REQUIRES` edges. This is a tool behaviour change — no schema changes required.
