---
name: json-transformation
description: Transform JSON documents through explicit mapping rules with recorded defaults, deliberate drops, and target-schema validation.
metadata:
  source: skills/12-data/json-transformation.md
  category: 12-data
  version: "v2"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-12-data-json-transformation.json)

# Json Transformation

**Category:** `data`
**Skill Level:** `advanced`
**Stability:** `stable`
**Added:** 2025-03

### Description

Transform JSON documents through explicit mapping rules with recorded defaults, deliberate drops, and target-schema validation. The data step is contract-first: validate the input contract before transforming, and verify the output against explicit expectations rather than trusting the pipeline.

### Inputs / Outputs

| Direction | Field | Type | Contract |
|---|---|---|---|
| Input | document | object | Source JSON with its declared structure |
| Input | transform_spec | object | Explicit mapping rules: paths, renames, defaults, types |
| Output | transformed | object | The mapped document matching the target schema |
| Output | diff_report | list | Fields added, dropped, or defaulted by the transform |

### Procedure
1. Parse the source with a real JSON parser; never transform text with regex.
2. Declare each mapping rule as an explicit path-to-path transform.
3. Apply defaults for missing fields and record every default applied.
4. Drop undeclared fields deliberately and list them in the diff report.
5. Validate the output against the target schema before emitting it.

### Example

```python
doc = {'user': {'full_name': 'Ada L', 'email': 'a@x.io'}, 'extra': 1}
flat = {'name': doc['user']['full_name'], 'email': doc['user']['email']}
dropped = [k for k in doc if k != 'user']
assert flat == {'name': 'Ada L', 'email': 'a@x.io'} and dropped == ['extra']
print({'mapped': sorted(flat), 'dropped': dropped})
```

### Related Skills

- [Schema Inference](schema-inference.md) - derive the target structure
- [Response Schema Validation](response-schema-validation.md) - validate transformed output
- [Csv Processing](csv-processing.md) - tabular counterpart for flat data

## Failure Modes

- Regex-based text transforms breaking on nested or reordered JSON.
- Undeclared fields silently carried into the output.
- Missing fields filled with wrong defaults and never reported.
- Output shape drift because no target schema validation exists.

## Changelog
- v2 (2026-11): Structural modernization; added the input/output contract table, a skill-specific execution procedure, a deterministic example, and corpus-verified related links (replaced the unresolvable cross-category related references).
- v1 (2025-03): Initial entry.

## Evidence

- https://agentskills.io/specification

Evidence status: implementation guidance only; runtime behavior must be checked against the executing pipeline's documentation; no benchmark claim is made without reproducible evidence.
