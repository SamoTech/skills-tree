# INITIATIVE-004W — Phase 4: Build Validation

**Date:** 2026-06-22  
**Source:** `tools/build_graph.py` SHA `32cb15092275229ff5ed77f8b904b50322241907`  
**Evidence basis:** Direct code inspection. No execution.

---

## Build Command Validation

Workflow invocation:
```bash
python tools/build_graph.py --output data/SKILLS_GRAPH.json
```

Script argparse interface:
```python
parser.add_argument("--dry-run", action="store_true", ...)
parser.add_argument("--output", default=str(DATA_DIR / "SKILLS_GRAPH.json"), ...)
```

**Result:** Command matches interface exactly. ✅

---

## SCHEMA_VERSION Constant

```python
SCHEMA_VERSION = "3.1"   # bumped from 3.0 — INITIATIVE-004
```

**Result:** Running current `build_graph.py` WILL produce `schema_version: "3.1"`. ✅

---

## pipeline-test Node Production

`main()` iterates:
```python
for cat_dir in sorted(SKILLS_DIR.iterdir()):
    if not cat_dir.is_dir(): continue
    category = cat_dir.name
    if not re.match(r"^[0-9]{2}-", category): continue
```

`skills/00-sandbox/` — `00-sandbox` matches `^[0-9]{2}-` (YES: `00` = two digits, `-` matches). ✅

`pipeline-test.md` will be discovered. Frontmatter (SHA `1976abd5`):
```yaml
---
title: Pipeline Test Fixture
prerequisites:
  - 02-reasoning/chain-of-thought
---
```

`parse_frontmatter()` block-sequence parser correctly reads this as `["02-reasoning/chain-of-thought"]`. ✅  
`build_node()` stores `"prerequisites": ["02-reasoning/chain-of-thought"]`. ✅

**Result:** `00-sandbox/pipeline-test` node WILL appear in graph. ✅

---

## REQUIRES Edge Production

`build_prerequisite_edges()` for pipeline-test node emits:
```json
{
  "source": "00-sandbox/pipeline-test",
  "target": "02-reasoning/chain-of-thought",
  "type": "REQUIRES",
  "confidence": "high",
  "source_method": "frontmatter_prerequisite"
}
```
No self-loop. Target confirmed present in graph. Edge WILL be emitted. ✅

---

## Build Validation Summary

| Check | Expected Output | Evidence |
|---|---|---|
| schema_version | `"3.1"` | `SCHEMA_VERSION = "3.1"` constant in script |
| pipeline-test node present | YES | `00-sandbox` matches category regex; frontmatter valid |
| prerequisites parsed correctly | YES | `parse_frontmatter()` handles block sequences |
| REQUIRES edge emitted | YES | `build_prerequisite_edges()` iterates prerequisites |
| Target node exists | YES | `02-reasoning/chain-of-thought` in current graph |
| requires_count in meta | >= 1 | Counted and written to graph meta |
| initiative field | `"INITIATIVE-004"` | Hardcoded in script |

**Verdict: Current repository state WILL generate a correct v3.1 graph with REQUIRES edges when the workflow runs.** ✅
