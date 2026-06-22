# extract_edges.py Alignment

**Mission:** INITIATIVE-004 Phase 3  
**Date:** 2026-06-22  
**Decision:** Implement Source 1 (prerequisites frontmatter) in `extract_edges.py`

---

## Problem Statement (from INITIATIVE-003)

`extract_edges.py` docstring listed three extraction sources:
```
1. ## Related Skills sections — markdown links
2. Explicit prerequisite language in frontmatter (dependencies field)
3. Inline prerequisite keywords in body text
```

However, the implementation only handled Source 1. Source 2 referenced a non-existent `dependencies` field. Source 3 was not implemented as a separate path (keywords in body text outside `## Related Skills` were not scanned).

This was a code/documentation divergence confirmed in `meta/DEPENDENCY_TOOL_ALIGNMENT.md`.

---

## Decision

**Implement Source 1 (prerequisites frontmatter) as the first extraction source.**

Rationale:
- Schema v3.1 now defines `prerequisites` as the canonical field (not `dependencies`)
- `build_graph.py` already owns REQUIRES edge generation from frontmatter (as of this commit)
- `extract_edges.py` is used as a standalone audit/inspection tool, so it must also emit REQUIRES edges from `prerequisites` to give accurate output
- Source 3 (inline keywords in body text outside Related Skills) remains out of scope — no evidence this pattern is used in the repository

---

## Changes Made

### 1. Added `parse_frontmatter()` function

Identical logic to the version in `build_graph.py`. Placed before the trigger patterns block for readability. Handles both simple key:value and YAML block sequences.

### 2. Updated `extract_from_file()` to implement Source 1

Before: function opened the file, searched for `## Related Skills`, returned edges from markdown links only.

After: function first parses frontmatter, loops over `prerequisites`, emits REQUIRES edges (with `source_method: "frontmatter_prerequisite"`), then continues to Source 2 (Related Skills section).

Deduplication: a `seen` set tracks `(source, target, type)` tuples. A prerequisite that also appears in `## Related Skills` will only generate one REQUIRES edge (from the frontmatter, which is processed first).

### 3. Updated docstring

Source order corrected:
```
1. prerequisites frontmatter field — generates REQUIRES edges
2. ## Related Skills sections — typed edges by keyword context
```

The old "Source 2: frontmatter dependencies field" and "Source 3: inline keywords" are removed. The docstring now accurately describes what the code does.

---

## Verification Criterion

Running:
```
python tools/extract_edges.py --category 00-sandbox
```
Against the pilot fixture (`skills/00-sandbox/pipeline-test.md`) should produce:
```json
[{
  "source": "00-sandbox/pipeline-test",
  "target": "02-reasoning/chain-of-thought",
  "type": "REQUIRES",
  "evidence": "prerequisites: 02-reasoning/chain-of-thought",
  "source_file": "skills/00-sandbox/pipeline-test.md",
  "confidence": "high",
  "source_method": "frontmatter_prerequisite"
}]
```
