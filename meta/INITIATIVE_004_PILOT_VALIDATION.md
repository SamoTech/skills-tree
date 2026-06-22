# Pilot Validation

**Mission:** INITIATIVE-004 Phase 4  
**Date:** 2026-06-22

---

## Pilot Fixture

File: `skills/00-sandbox/pipeline-test.md`  
Field declared:
```yaml
prerequisites:
  - 02-reasoning/chain-of-thought
```

---

## Expected REQUIRES Edge

```json
{
  "source": "00-sandbox/pipeline-test",
  "target": "02-reasoning/chain-of-thought",
  "type": "REQUIRES",
  "evidence": "prerequisites: 02-reasoning/chain-of-thought",
  "source_file": "skills/00-sandbox/pipeline-test.md",
  "confidence": "high",
  "source_method": "frontmatter_prerequisite"
}
```

---

## Pipeline Path (end-to-end trace)

1. `build_graph.py` discovers `skills/00-sandbox/pipeline-test.md`
2. `parse_frontmatter()` reads `prerequisites: ["02-reasoning/chain-of-thought"]`
3. `build_node()` stores list in `node["prerequisites"]`
4. `build_prerequisite_edges(node)` iterates the list, emits 1 REQUIRES edge
5. Edge is added to `edges[]` alongside RELATED_TO edges from body text
6. `validate_graph()` checks the edge — target `02-reasoning/chain-of-thought` must exist in `known_ids` or it becomes an UNRESOLVED_TARGET warning
7. Graph is written with `meta.requires_count >= 1`

---

## Before State

| Metric | Value | Source |
|---|---|---|
| REQUIRES edges | 0 | `meta/INITIATIVE_001C_AUDIT_REPORT.md` |
| `meta.schema_version` | `3.0` | `data/SKILLS_GRAPH.json` pre-INITIATIVE-004 |
| `source_method` field in edges | ABSENT | pre-INITIATIVE-004 |

---

## After State (expected, post-workflow trigger)

| Metric | Expected value |
|---|---|
| REQUIRES edges | ≥ 1 (from pilot fixture) |
| `meta.schema_version` | `3.1` |
| `meta.requires_count` | ≥ 1 |
| Pilot REQUIRES edge present | YES |

**Note:** The actual `data/SKILLS_GRAPH.json` is a generated artifact produced by the GitHub Actions workflow (`build-graph.yml`). It will be regenerated automatically when the updated `build_graph.py` and pilot fixture are committed. The validation above describes what the workflow run should produce. Actual counts depend on whether `02-reasoning/chain-of-thought` resolves as a known node ID in the full graph.

---

## Removal Condition

`skills/00-sandbox/pipeline-test.md` should be removed in INITIATIVE-005 after at least one real skill in `09-agentic-patterns` declares `prerequisites` and the pipeline is confirmed live with real data. The `00-sandbox` category itself may also be removed at that point if no other fixtures exist.
