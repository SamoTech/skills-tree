---
title: "Missing Data Imputation"
category: 12-data
level: intermediate
stability: experimental
description: "Profile per-column missingness, choose an explicit imputation strategy per column, fit fill values on training rows only, and record an imputation mask so later analyses can audit the change."
added: "2026-10"
version: v1
related: ["data-cleaning", "statistical-analysis", "schema-inference"]
---

# Missing Data Imputation

Category: Data | Level: intermediate | Stability: experimental | Version: v1

## Description

How values are missing carries as much signal as the values themselves, and a single global fill rule such as zero-for-everything destroys that signal. This skill defines the disciplined loop: profile per-column missingness, pick a strategy per column, fit fill values on training rows only, and record an imputation mask so every filled cell stays identifiable for later audit.

## When to Use

Use when training or reporting data has missing cells and the fill rule affects the result.

Do not use for already-masked experimental data where missingness is part of the design; that case is analysis configuration, not imputation.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `rows` | `list` | Yes | Records with absent cells represented as null |
| `columns` | `list` | Yes | Columns to profile and fill |
| `strategies` | `object` | Yes | Per-column strategy such as median, mode, constant, or none |
| `fit_scope` | `list` | No | Row subset used to fit fill values, defaulting to training rows |

## Procedure

1. Profile every column: missing count, missing rate, and the pattern of co-missingness across rows.
2. Classify each column’s missingness mechanism before choosing a strategy; uniform filling across mechanisms is a smell.
3. Choose a strategy per column and record why it was chosen.
4. Fit fill values on the declared fit scope only; never let test or future rows influence a fill value.
5. Apply fills to a copy; the original rows stay untouched for audit.
6. Record an imputation mask alongside the filled data so every filled cell is identifiable later.
7. Re-profile after filling and compare distributions; a fill that moves a distribution needs a second look.
8. Document the mask’s retention period; the mask is analytical metadata, not a permanent record.

## Outputs

| Output | Type | Description |
|---|---|---|
| `filled_rows` | `list` | Copies with missing cells filled per strategy |
| `mask` | `list` | Row-column positions that were filled |
| `profile` | `object` | Per-column missingness before and after filling |
| `fill_values` | `object` | Fitted fill values with their fit scope |

## Runnable Example

```python
def profile_missing(rows, columns):
    """Report per-column missingness counts and rates."""
    total = len(rows)
    profile = {}
    for column in columns:
        missing = sum(1 for row in rows if row.get(column) is None)
        profile[column] = {
            "missing": missing,
            "rate": round(missing / total, 2) if total else 0.0,
        }
    return profile

def impute_column(rows, column, strategy, fit_rows=None):
    """Apply a per-column strategy fitted only on the declared scope."""
    scope = rows if fit_rows is None else fit_rows
    present = [row[column] for row in scope if row.get(column) is not None]
    if strategy == "median" and present:
        ordered = sorted(present)
        mid = len(ordered) // 2
        if len(ordered) % 2:
            filler = ordered[mid]
        else:
            filler = (ordered[mid - 1] + ordered[mid]) / 2
    else:
        filler = strategy
    filled = []
    for row in rows:
        copy = dict(row)
        if copy.get(column) is None:
            copy[column] = filler
        filled.append(copy)
    return filled

rows = [{"age": 30}, {"age": None}, {"age": 40}, {"age": None}]
print(profile_missing(rows, ["age"]))
print(impute_column(rows, "age", "median"))
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Global fill | One rule is applied to every column | Choose a strategy per column and record why |
| Test leakage | Fill values are fitted on all rows | Fit on training rows only |
| Mask loss | Filled data ships without its mask | Ship the mask beside the filled data |
| Distribution shift | The fill moves the column’s shape | Re-profile after filling and compare |
| In-place overwrite | Original rows are mutated | Fill copies and keep the originals untouched |

## Security and Authority Boundary

Imputing values grants no authority to invent records. Filled cells are estimates and must remain identifiable as such through the mask. Data subject to privacy or retention limits keeps those limits through the whole loop: profiling, filling, and the mask inherit them.

## Evidence

This skill is grounded in dated public implementation references:

1. The pandas user guide on missing data (https://pandas.pydata.org/docs/user_guide/missing_data.html).
2. Wikipedia’s article on missing data (https://en.wikipedia.org/wiki/Missing_data).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Data Cleaning](data-cleaning.md) — normalizes and repairs records; this skill governs the fill step specifically.
- [Statistical Analysis](statistical-analysis.md) — consumes the filled data; the mask keeps its sensitivity to fills auditable.
- [Schema Inference](schema-inference.md) — types the columns whose missingness this skill profiles.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
