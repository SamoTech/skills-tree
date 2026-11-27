---
name: pandas-operations
description: Apply reproducible pandas transformations with dtype and shape verification at each step and no silent NaN propagation.
metadata:
  source: skills/12-data/pandas-operations.md
  category: 12-data
  version: "v2"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-12-data-pandas-operations.json)

# Pandas Operations

**Category:** `data`
**Skill Level:** `advanced`
**Stability:** `stable`
**Added:** 2025-03

### Description

Apply reproducible pandas transformations with dtype and shape verification at each step and no silent NaN propagation. The data step is contract-first: validate the input contract before transforming, and verify the output against explicit expectations rather than trusting the pipeline.

### Inputs / Outputs

| Direction | Field | Type | Contract |
|---|---|---|---|
| Input | dataframe | object | A loaded DataFrame with declared dtypes and index |
| Input | operation_plan | object | Ordered operations with expected shapes per step |
| Output | result | object | The transformed DataFrame with verified dtypes and shape |
| Output | shape_trace | list | Input/output shape of each operation for reconciliation |

### Procedure
1. Verify dtypes and shape right after loading, before any operation.
2. Chain operations in a declared order with the expected shape per step.
3. Avoid chained assignment; use explicit .loc or vectorized operations.
4. Check for silent NaN propagation after merges and aggregations.
5. Assert the final shape and dtypes against expectations before export.

### Example

```python
col = [1, 2, 3, 4]
op_plan = [{'op': 'filter>2', 'expect': 2}, {'op': 'sum', 'expect': 7}]
filtered = [v for v in col if v > 2]
total = sum(filtered)
assert len(filtered) == op_plan[0]['expect'] and total == op_plan[1]['expect']
print({'shape_after_filter': len(filtered), 'sum': total})
```

### Related Skills

- [Csv Processing](csv-processing.md) - load tabular input correctly
- [Statistical Analysis](statistical-analysis.md) - analyze the prepared frame
- [Data Cleaning](data-cleaning.md) - repair defects before analysis

## Failure Modes

- Chained assignment producing SettingWithCopyWarning and no real update.
- dtype drift (object where numeric was expected) breaking vectorized ops.
- Silent NaN introduction after merges or groupby on missing keys.
- No shape assertions, so an accidental row drop goes unnoticed.

## Changelog
- v2 (2026-11): Structural modernization; added the input/output contract table, a skill-specific execution procedure, a deterministic example, and corpus-verified related links (replaced the unresolvable cross-category related references).
- v1 (2025-03): Initial entry.

## Evidence

- https://agentskills.io/specification

Evidence status: implementation guidance only; runtime behavior must be checked against the executing pipeline's documentation; no benchmark claim is made without reproducible evidence.
