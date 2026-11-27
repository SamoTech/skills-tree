---
title: "Data Aggregation"
category: 12-data
level: advanced
stability: stable
version: v2
description: "Aggregate records into declared group-by measures with explicit grain, null handling, and reconciled totals."
added: "2025-03"
related: [data-summarization, cohort-analysis, funnel-analysis]
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-12-data-data-aggregation.json)

# Data Aggregation

**Category:** `data`
**Skill Level:** `advanced`
**Stability:** `stable`
**Added:** 2025-03

### Description

Aggregate records into declared group-by measures with explicit grain, null handling, and reconciled totals. The data step is contract-first: validate the input contract before transforming, and verify the output against explicit expectations rather than trusting the pipeline.

### Inputs / Outputs

| Direction | Field | Type | Contract |
|---|---|---|---|
| Input | records | list of object | Row-level data with declared grain and measures |
| Input | aggregation_spec | object | Group-by keys, measures, and aggregation functions |
| Output | aggregates | list of object | One row per group with computed measures |
| Output | reconciliation | object | Source row count vs summed group counts |

### Procedure
1. State the grain (one row per what?) before choosing group-by keys.
2. Declare each measure and its aggregation function (sum, mean, count).
3. Aggregate deterministically: same input, same key order, same output.
4. Handle nulls and empty groups explicitly, never by silent exclusion.
5. Reconcile: summed group counts must equal the source row count.

### Example

```python
rows = [{'region': 'east', 'sales': 10}, {'region': 'east', 'sales': 5}, {'region': 'west', 'sales': 7}]
agg = {}
for r in rows:
    agg[r['region']] = agg.get(r['region'], 0) + r['sales']
assert agg == {'east': 15, 'west': 7}
assert sum(1 for r in rows) == 3
print(agg)
```

### Related Skills

- [Data Summarization](data-summarization.md) - summarize aggregates for readers
- [Cohort Analysis](cohort-analysis.md) - aggregate by time-defined cohorts
- [Funnel Analysis](funnel-analysis.md) - aggregate stage-to-stage conversion

## Failure Modes

- Double counting when a group-by key is missing from some rows.
- Mixing grains (user-day vs user) in one aggregate.
- Nulls silently excluded, making totals not reconcile with the source.
- Nondeterministic ordering causing different results across runs.

## Changelog
- v2 (2026-11): Structural modernization; added the input/output contract table, a skill-specific execution procedure, a deterministic example, and corpus-verified related links (replaced the unresolvable cross-category related references).
- v1 (2025-03): Initial entry.

## Evidence

- https://agentskills.io/specification

Evidence status: implementation guidance only; runtime behavior must be checked against the executing pipeline's documentation; no benchmark claim is made without reproducible evidence.
