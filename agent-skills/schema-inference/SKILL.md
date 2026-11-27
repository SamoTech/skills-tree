---
name: schema-inference
description: Infer candidate schemas from representative samples with type-conflict flagging, nullability thresholds, and held-out validation.
metadata:
  source: skills/12-data/schema-inference.md
  category: 12-data
  version: "v2"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-12-data-schema-inference.json)

# Schema Inference

**Category:** `data`
**Skill Level:** `advanced`
**Stability:** `stable`
**Added:** 2025-03

### Description

Infer candidate schemas from representative samples with type-conflict flagging, nullability thresholds, and held-out validation. The data step is contract-first: validate the input contract before transforming, and verify the output against explicit expectations rather than trusting the pipeline.

### Inputs / Outputs

| Direction | Field | Type | Contract |
|---|---|---|---|
| Input | sample | list of object | Representative records (or a declared sample) to infer from |
| Input | inference_rules | object | Type mapping, nullability threshold, and confidence rules |
| Output | schema | object | Inferred fields with types, nullability, and confidence |
| Output | inference_notes | list | Ambiguities, conflicts, and records that disagree |

### Procedure
1. Sample data deliberately; never infer a schema from a single record.
2. Infer types per field and record conflicts (int vs str) instead of coercing.
3. Compute nullability from observed null rates with a declared threshold.
4. Flag low-confidence fields for human confirmation, not silent acceptance.
5. Validate the inferred schema against a held-out slice before committing it.

### Example

```python
records = [{'qty': 1, 'tag': 'a'}, {'qty': 2, 'tag': None}, {'qty': 3, 'tag': 'b'}]
fields = {}
for k in ('qty', 'tag'):
    vals = [r[k] for r in records if r[k] is not None]
    types = {type(v).__name__ for v in vals}
    nulls = sum(1 for r in records if r[k] is None)
    fields[k] = {'type': types.pop() if len(types) == 1 else 'conflict', 'nulls': nulls}
assert fields['qty'] == {'type': 'int', 'nulls': 0}
assert fields['tag'] == {'type': 'str', 'nulls': 1}
print(fields)
```

### Related Skills

- [Json Transformation](json-transformation.md) - map documents into the inferred schema
- [Data Validation](data-validation.md) - validate data against the schema
- [Data Profiling](data-profiling.md) - profile fields before inference

## Failure Modes

- Inferring from one record and missing the field's real variation.
- Type conflicts coerced silently instead of flagged.
- Nullability underestimated from a small or biased sample.
- An inferred schema never validated against held-out data.

## Changelog
- v2 (2026-11): Structural modernization; added the input/output contract table, a skill-specific execution procedure, a deterministic example, and corpus-verified related links (replaced the unresolvable cross-category related references).
- v1 (2025-03): Initial entry.

## Evidence

- https://agentskills.io/specification

Evidence status: implementation guidance only; runtime behavior must be checked against the executing pipeline's documentation; no benchmark claim is made without reproducible evidence.
