---
name: cohort-analysis
description: Segment records into cohorts by a shared anchor event, measure retention and behavior across periods, and compare cohort trajectories with explicit handling of censoring and cohort size.
metadata:
  source: skills/12-data/cohort-analysis.md
  category: 12-data
  version: "v1"
---

# Cohort Analysis

Category: Data | Level: basic | Stability: experimental | Version: v1

## Description

Cohort analysis compares groups defined by when they started, not by who they are. The skill covers assigning entities to cohorts by their first anchor event, binning cohorts by the calendar rule, computing period-by-period retention relative to cohort size, and censoring the trailing periods where not enough time has elapsed to observe the window. Comparisons are always normalized rates with cohort sizes attached, never raw counts.

## When to Use

Use when behavior must be compared across groups defined by a starting event: signup month, first purchase, activation week, or onboarding batch.

Do not compare raw counts across cohorts of different sizes. Normalize to rates and report cohort sizes alongside every comparison.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `events` | `table` | Yes | Timestamped records with an entity key and an event type |
| `cohort_def` | `object` | Yes | The anchor event and the binning rule defining cohort membership |
| `periods` | `int` | No | Number of periods after the anchor to measure; bounded by default |

## Procedure

1. Assign each entity to a cohort by its first occurrence of the anchor event.
2. Bin cohorts by the rule in the definition: calendar month, week, or event index.
3. For each cohort, compute the size at the anchor and the survivors in each later period.
4. Convert counts to rates relative to cohort size; never report raw counts alone.
5. Flag censored trailing periods where not enough time has elapsed to observe the window.
6. Compare trajectories across cohorts and annotate every difference with cohort sizes.

## Outputs

| Output | Type | Description |
|---|---|---|
| `cohort_table` | `table` | Cohorts by period with sizes and survivor counts |
| `retention_curves` | `array` | Per-cohort retention rates over the measured periods |
| `censored_periods` | `list` | Periods excluded from comparison for insufficient elapsed time |

## Runnable Example

```python
def retention_by_cohort(signups, actives):
    """signups: {cohort: size}; actives: {cohort: [active per period]}"""
    out = {}
    for cohort, size in signups.items():
        rates = [round(a / size, 3) for a in actives.get(cohort, [])]
        out[cohort] = {"size": size, "retention": rates}
    return out

print(retention_by_cohort(
    {"2026-07": 200, "2026-08": 150},
    {"2026-07": [200, 120, 66], "2026-08": [150, 60]},
))
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Survivorship bias | Only fully observed histories compared | Include censored periods and mark them in every chart |
| Small-cohort volatility | Tiny cohorts read as dramatic trends | Report sizes and aggregate tiny cohorts before comparing |
| Anchor event misdefined | Cohorts assigned by first record instead of the anchor | Validate the anchor against a hand-checked sample |
| Period edge effects | Partial trailing period treated as complete | Mark incomplete windows as censored, not as zero |
| Timezone drift | Cohort bins shift at month boundaries | Fix a timezone before binning and keep it fixed |

## Security and Authority Boundary

Cohort tables aggregate personal behavior. Use the minimum viable entity key, avoid rejoining identifiers after aggregation, and publish rates rather than raw per-entity histories wherever the decision allows.

## Evidence

This skill is grounded in dated public implementation references:

1. The pandas pivot table reference used to build cohort tables (https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.pivot_table.html).
2. The Wikipedia article defining cohort studies (https://en.wikipedia.org/wiki/Cohort_study).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Time Series](time-series.md) — the temporal layer that cohort bins index into.
- [Data Aggregation](data-aggregation.md) — the grouping primitives that build per-cohort summaries.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
