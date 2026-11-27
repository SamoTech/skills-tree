---
title: "Data Filtering"
category: 12-data
level: advanced
stability: stable
version: v2
description: "Filter datasets with declared predicates, explicit null semantics, and per-predicate exclusion counts."
added: "2025-03"
related: [data-cleaning, data-aggregation, sql-execution]
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-12-data-data-filtering.json)

# Data Filtering

**Category:** `data`
**Skill Level:** `advanced`
**Stability:** `stable`
**Added:** 2025-03

### Description

Filter datasets with declared predicates, explicit null semantics, and per-predicate exclusion counts. The data step is contract-first: validate the input contract before transforming, and verify the output against explicit expectations rather than trusting the pipeline.

### Inputs / Outputs

| Direction | Field | Type | Contract |
|---|---|---|---|
| Input | dataset | list of object | Records with typed fields to filter on |
| Input | filter_spec | object | Declared predicates, combinators, and null handling |
| Output | filtered | list of object | Records satisfying all declared predicates |
| Output | filter_report | object | Counts before, after, and excluded per predicate |

### Procedure
1. Declare each predicate with its field, operator, and null behavior.
2. Decide AND/OR composition up front; never mix it per row.
3. Apply predicates in a fixed order and count exclusions per predicate.
4. Treat nulls explicitly (exclude, include, or flag) per the spec.
5. Report counts before, after, and per predicate so filtering is reconcilable.

### Example

```python
rows = [{'id': 1, 'qty': 5}, {'id': 2, 'qty': 0}, {'id': 3, 'qty': None}]
spec = {'min_qty': 1, 'null_policy': 'exclude'}
kept, nulls = [], 0
for r in rows:
    if r['qty'] is None:
        nulls += 1
        continue
    if r['qty'] >= spec['min_qty']:
        kept.append(r['id'])
assert kept == [1] and nulls == 1
print({'kept': kept, 'excluded_nulls': nulls})
```

### Related Skills

- [Data Cleaning](data-cleaning.md) - repair records before filtering
- [Data Aggregation](data-aggregation.md) - aggregate the filtered set
- [Sql Execution](sql-execution.md) - push filters into the database

## Failure Modes

- Null semantics left implicit, so filters silently drop or keep rows.
- AND/OR ambiguity when predicates are combined without a declared combinator.
- Case or type mismatches (string vs numeric) making predicates never match.
- No exclusion counts, so a too-restrictive filter goes unnoticed.

## Changelog
- v2 (2026-11): Structural modernization; added the input/output contract table, a skill-specific execution procedure, a deterministic example, and corpus-verified related links (replaced the unresolvable cross-category related references).
- v1 (2025-03): Initial entry.

## Evidence

- https://agentskills.io/specification

Evidence status: implementation guidance only; runtime behavior must be checked against the executing pipeline's documentation; no benchmark claim is made without reproducible evidence.
