---
name: data-joining
description: Combine datasets on declared keys with the correct join type, duplicate-key handling, and a full match report.
metadata:
  source: skills/12-data/data-joining.md
  category: 12-data
  version: "v2"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-12-data-data-joining.json)

# Data Joining

**Category:** `data`
**Skill Level:** `advanced`
**Stability:** `stable`
**Added:** 2025-03

### Description

Combine datasets on declared keys with the correct join type, duplicate-key handling, and a full match report. The data step is contract-first: validate the input contract before transforming, and verify the output against explicit expectations rather than trusting the pipeline.

### Inputs / Outputs

| Direction | Field | Type | Contract |
|---|---|---|---|
| Input | left | list of object | Primary dataset with declared join keys |
| Input | right | list of object | Secondary dataset with declared join keys |
| Output | joined | list of object | Rows with matched fields and unmatched flags |
| Output | match_report | object | Matched, unmatched-left, unmatched-right, and duplicate-key counts |

### Procedure
1. Confirm the join keys are unique on the expected side before joining.
2. Declare the join type (inner, left, right, full) and match multiplicity.
3. Detect duplicate keys that would fan out rows; resolve them explicitly.
4. Join with a real join operation; never zip rows by position.
5. Report matched, unmatched-left, and unmatched-right counts.

### Example

```python
left = [{'id': 1, 'name': 'a'}, {'id': 2, 'name': 'b'}]
right = [{'id': 1, 'price': 9}, {'id': 3, 'price': 4}]
rmap = {}
for r in right:
    rmap.setdefault(r['id'], []).append(r)
joined = [{**l, 'price': rmap[l['id']][0]['price']} for l in left if l['id'] in rmap]
unmatched_left = [l['id'] for l in left if l['id'] not in rmap]
unmatched_right = [r['id'] for r in right if r['id'] not in {l['id'] for l in left}]
assert len(joined) == 1 and unmatched_left == [2] and unmatched_right == [3]
print({'matched': len(joined), 'unmatched_left': unmatched_left, 'unmatched_right': unmatched_right})
```

### Related Skills

- [Sql Execution](sql-execution.md) - join with set-based database operations
- [Data Cleaning](data-cleaning.md) - fix keys before joining
- [Schema Inference](schema-inference.md) - confirm key types on both sides

## Failure Modes

- Duplicate join keys fanning out rows and inflating counts silently.
- Wrong join type (inner where left was needed) dropping records.
- Positional zipping instead of key-based matching.
- Key type mismatches (int vs str id) producing zero matches.

## Changelog
- v2 (2026-11): Structural modernization; added the input/output contract table, a skill-specific execution procedure, a deterministic example, and corpus-verified related links (replaced the unresolvable cross-category related references).
- v1 (2025-03): Initial entry.

## Evidence

- https://agentskills.io/specification

Evidence status: implementation guidance only; runtime behavior must be checked against the executing pipeline's documentation; no benchmark claim is made without reproducible evidence.
