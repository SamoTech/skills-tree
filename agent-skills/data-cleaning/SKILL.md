---
name: data-cleaning
description: Detect and resolve data defects with declared rules, recorded changes, and re-validation of the cleaned output.
metadata:
  source: skills/12-data/data-cleaning.md
  category: 12-data
  version: "v2"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-12-data-data-cleaning.json)

# Data Cleaning

**Category:** `data`
**Skill Level:** `advanced`
**Stability:** `stable`
**Added:** 2025-03

### Description

Detect and resolve data defects with declared rules, recorded changes, and re-validation of the cleaned output. The data step is contract-first: validate the input contract before transforming, and verify the output against explicit expectations rather than trusting the pipeline.

### Inputs / Outputs

| Direction | Field | Type | Contract |
|---|---|---|---|
| Input | dataset | list of object | Raw records with the defect classes to scan for |
| Input | cleaning_rules | object | Declared repairs: dedupe keys, null policy, range checks |
| Output | clean_dataset | list of object | Repaired records, each change traceable |
| Output | change_log | list | Every modification with the rule that triggered it |

### Procedure
1. Profile the data first: measure null rates, duplicates, and range violations.
2. Declare each repair rule before applying it; never clean ad hoc.
3. Deduplicate on declared keys, keeping a record of dropped duplicates.
4. Apply the null policy (drop, impute, flag) consistently per column.
5. Log every change with the rule and the affected record.
6. Re-validate the cleaned output against the original constraints.

### Example

```python
rows = [{'id': 1, 'qty': 5}, {'id': 1, 'qty': 5}, {'id': 2, 'qty': None}]
seen, clean, dropped = set(), [], []
for r in rows:
    if r['id'] in seen:
        dropped.append(r['id'])
        continue
    seen.add(r['id'])
    clean.append({**r, 'qty': r['qty'] if r['qty'] is not None else 0})
assert len(clean) == 2 and dropped == [1] and clean[1]['qty'] == 0
print({'kept': len(clean), 'deduped': dropped})
```

### Related Skills

- [Missing Data Imputation](missing-data-imputation.md) - fill gaps under a declared policy
- [Data Profiling](data-profiling.md) - measure defects before cleaning
- [Data Validation](data-validation.md) - re-validate cleaned output

## Failure Modes

- Deduplicating on non-unique keys and deleting valid records.
- Imputing without recording it, corrupting later statistics.
- Cleaning rules applied inconsistently across batches of the same data.
- No change log, so repairs cannot be audited or reversed.

## Changelog
- v2 (2026-11): Structural modernization; added the input/output contract table, a skill-specific execution procedure, a deterministic example, and corpus-verified related links (replaced the unresolvable cross-category related references).
- v1 (2025-03): Initial entry.

## Evidence

- https://agentskills.io/specification

Evidence status: implementation guidance only; runtime behavior must be checked against the executing pipeline's documentation; no benchmark claim is made without reproducible evidence.
