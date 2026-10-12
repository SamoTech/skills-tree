---
title: "Pareto Analysis"
category: 02-reasoning
level: basic
stability: experimental
description: "Rank causes or contributors by their share of an effect, find the few inputs that produce most of the outcome, and act on that measured concentration."
added: "2026-10"
version: v1
related: ["prioritization", "trade-off-analysis"]
---

# Pareto Analysis

Category: Reasoning | Level: basic | Stability: experimental | Version: v1

## Description

Most effects are concentrated: a minority of causes produces the majority of results. Pareto analysis measures that concentration instead of assuming it — ranking contributors by measured share, identifying the set that crosses a stated threshold, and directing effort where leverage is real. The skill is about the measurement, not the folklore: not every distribution is 80/20, and the split must be computed, not quoted.

## When to Use

Use when effort must be allocated across many candidate causes — defect sources, error classes, cost drivers, usage patterns — and the budget cannot cover everything.

Do not cite the 80/20 ratio as a finding; measure the actual concentration and report the real split.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `contributions` | `map` | Yes | Measured contribution per cause |
| `threshold` | `float` | No | Cumulative share defining the vital few; default 0.8 |
| `labels` | `map` | No | Display names per cause |

## Procedure

1. Measure contributions on a single, stated scale; shares computed across mixed units are meaningless.
2. Sort causes by contribution, descending, and compute each one as a share of the total.
3. Accumulate shares in rank order and identify the smallest set that crosses the threshold.
4. Report the actual split — how many causes reach what cumulative share — instead of the assumed 80/20.
5. Check the tail: the long tail still matters when it aggregates, and concentration at the top does not make the rest zero.
6. Re-measure after acting on the vital few; the distribution shifts once the top contributors are addressed.

## Outputs

| Output | Type | Description |
|---|---|---|
| `ranking` | `list` | Causes in descending contribution order |
| `vital_few` | `list` | Smallest set crossing the cumulative threshold |
| `split` | `map` | Actual cause-count to cumulative-share split measured |

## Runnable Example

```python
def pareto(contributions, threshold=0.8):
    total = sum(contributions.values())
    ranked = sorted(contributions.items(), key=lambda kv: -kv[1])
    cumulative, vital = 0.0, []
    for cause, value in ranked:
        cumulative += value / total
        vital.append(cause)
        if cumulative >= threshold:
            break
    return {"vital_few": vital, "cumulative_share": round(cumulative, 2), "causes_total": len(ranked)}

errors = {"network": 120, "disk": 45, "cpu": 20, "memory": 10, "config": 5}
print(pareto(errors))
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Assumed split | The 80/20 ratio is quoted rather than measured | Compute and report the actual split |
| Mixed scales | Shares computed across incommensurable units | Measure on one stated scale |
| Static ranking | An old distribution guides new effort | Re-measure after each intervention |
| Tail neglect | The aggregated tail is dismissed as zero | Report tail totals alongside the vital few |
| Single-cause rounding | Near-equal causes split arbitrarily | Note ranks that are statistically indistinguishable |

## Security and Authority Boundary

Pareto rankings over incident, access, or failure data can reveal which components of a system are most fragile. Treat the ranking itself as sensitive when the underlying data is, and share it on a need-to-know basis.

## Evidence

This skill is grounded in dated public implementation references:

1. Wikipedia's overview of the Pareto principle (https://en.wikipedia.org/wiki/Pareto_principle).
2. Wikipedia's overview of the Pareto chart used for this analysis (https://en.wikipedia.org/wiki/Pareto_chart).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Prioritization](prioritization.md) — the ordering discipline that consumes this ranking.
- [Trade-off Analysis](trade-off-analysis.md) — the comparison layer for allocating effort across the measured set.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
