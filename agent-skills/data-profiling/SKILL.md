---
name: data-profiling
description: Measure a dataset before using it — row counts, distributions, null rates, cardinalities — so assumptions about the data are recorded facts instead of hopes.
metadata:
  source: skills/12-data/data-profiling.md
  category: 12-data
  version: "v1"
---

# Data Profiling

Category: Data | Level: intermediate | Stability: experimental | Version: v1

## Description

Every analysis rests on beliefs about its data: that ids are unique, that the date column is a date, that the two category columns relate the way they did last quarter. Profiling replaces those beliefs with measurements: counts, distinct values, null rates, ranges, and distribution shapes, recorded per column and compared over time. The profile is not the analysis — it is the ground the analysis stands on, and a profile that changed since last week is often the whole explanation for a number that stopped making sense.

## When to Use

Use when a dataset is new to you, before publication or reporting on it, and periodically on datasets assumed stable.

Do not profile a known-stable, schema-verified table on every read; repeated profiling of unchanged data is cost without information.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `dataset` | `table` | Yes | The data being profiled |
| `metrics` | `list` | Yes | Counts, null rates, distinct values, ranges to measure |
| `baseline` | `map` | No | A prior profile to diff against |

## Procedure

1. Profile structure first: column names, types, row count, and how those differ from any recorded schema.
2. Measure completeness per column — null rates and default values — and distinctness: cardinality and top values.
3. Profile ranges and distributions for numeric and temporal columns, recording min, max, and shape, not just the mean.
4. Diff against the baseline profile and flag every metric that moved beyond its historical band.
5. Record the profile with the dataset version and date, so future comparisons have something concrete to diff.
6. Turn anomalies into constraints: a property that surprised you is a rule for the validation boundary.

## Outputs

| Output | Type | Description |
|---|---|---|
| `profile` | `map` | Per-column measurements with dataset version and date |
| `diff` | `map` | Movements against the prior profile, empty when none |

## Runnable Example

```python
from collections import Counter

def profile_column(values):
    total = len(values)
    nulls = sum(1 for v in values if v is None)
    distinct = len(set(v for v in values if v is not None))
    return {
        "count": total,
        "null_rate": round(nulls / total, 3) if total else None,
        "distinct": distinct,
    }

def top_values(values, limit=3):
    counts = Counter(v for v in values if v is not None)
    return counts.most_common(limit)

column = ["paid", "paid", None, "refunded", "paid", None]
print(profile_column(column))
print(top_values(column))
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Assumed schemas | Analysis built on a shape nobody verified | Profile structure before any measurement |
| Mean-blindness | Averages hiding bimodal or skewed reality | Record distribution shape, not just the mean |
| Unrecorded profiles | Measurements made once and lost | Persist profiles with dataset version and date |
| Unbounded profiling | Whole-table scans repeated on every read | Profile new or changed data; sample what is stable |
| Anomaly blindness | A moved metric nobody diffs against history | Always diff against the prior profile |

## Security and Authority Boundary

Profiles are exfiltration-shaped: cardinalities, top values, and ranges of sensitive columns can disclose individual records, so profiling outputs on restricted data inherit its access scope and profiling jobs must not write measurements to stores more public than the data itself could reach.

## Evidence

This skill is grounded in dated public implementation references:

1. Wikipedia's overview of data profiling (https://en.wikipedia.org/wiki/Data_profiling).
2. Wikipedia's overview of descriptive statistics (https://en.wikipedia.org/wiki/Descriptive_statistics).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Statistical Analysis](statistical-analysis.md) — the deeper inference profiling feeds.
- [Data Cleaning](data-cleaning.md) — acting on what the profile exposes.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
