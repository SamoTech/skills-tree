---
title: "Cost-Benefit Analysis"
category: 02-reasoning
level: intermediate
stability: experimental
description: "Compare options by monetized and non-monetized effects over a stated horizon, with explicit discounting, distribution of costs and benefits, and named losers."
added: "2026-10"
version: v1
related: ["trade-off-analysis", "decision-making"]
---

# Cost-Benefit Analysis

Category: Reasoning | Level: intermediate | Stability: experimental | Version: v1

## Description

A cost-benefit analysis puts options on one comparable footing: what each costs, what it returns, over what horizon, and who pays versus who benefits. This skill structures the comparison — full-cost inventory, effect monetization where honest, explicit discounting, and named distributional effects — and keeps non-monetizable impacts visible instead of treating them as zero.

## When to Use

Use when choosing among options with different cost and effect profiles — build versus buy, adopt versus wait — where a defensible comparison must survive scrutiny.

Do not collapse everything into one number; the analysis is the table of costs, benefits, and who bears them, not just the net present value.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `options` | `list` | Yes | Candidate options under comparison |
| `horizon` | `duration` | Yes | Analysis period |
| `discount_rate` | `float` | No | Annual rate used to compare future and present values |
| `effects` | `list` | Yes | Cost and benefit items per option, monetized where possible |

## Procedure

1. Inventory the full cost set per option — direct, indirect, transition, and operating — before any benefit is counted.
2. Monetize effects where a defensible basis exists and mark the basis used; leave non-monetizable effects as explicit rows.
3. Convert flows to present values over the stated horizon with the stated discount rate, showing how the rate affects the ranking.
4. Compute per-option summaries — net value, payback, benefit-cost ratio — and compare on the same assumptions.
5. Name the distribution: who pays, who benefits, and when, because net-positive totals can hide transfers.
6. State the decision rule in advance — minimum ratio, maximum payback — and apply it to the computed table.

## Outputs

| Output | Type | Description |
|---|---|---|
| `comparison` | `map` | Per-option costs, benefits, and present values |
| `summary` | `map` | Net value, payback, and ratio per option |
| `distribution` | `map` | Who bears which costs and receives which benefits |

## Runnable Example

```python
def present_value(flows, rate):
    return {year: round(amount / ((1 + rate) ** year), 2) for year, amount in flows.items()}

def net_present_value(costs, benefits, rate):
    pv_costs = sum(present_value(costs, rate).values())
    pv_benefits = sum(present_value(benefits, rate).values())
    return {"npv": round(pv_benefits - pv_costs, 2), "ratio": round(pv_benefits / pv_costs, 2)}

costs = {0: 100.0, 1: 10.0, 2: 10.0}
benefits = {1: 70.0, 2: 80.0}
print(net_present_value(costs, benefits, 0.1))
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Hidden costs | Only direct costs are counted | Inventory indirect, transition, and operating costs |
| Forced monetization | Non-monetizable effects get invented numbers | Keep them as explicit non-monetized rows |
| Rate silence | The discount rate is unstated or arbitrary | State the rate and show ranking sensitivity to it |
| Buried transfers | A net-positive total hides who loses | Name payers and beneficiaries per row |
| Post-hoc rule fit | The decision rule is chosen after seeing results | Fix the rule before computing |

## Security and Authority Boundary

Cost-benefit tables over security controls monetize breach risk and can pressure under-investment. Treat security-benefit estimates as decision inputs, not commitments, and never use monetized risk to justify skipping controls required by policy or law.

## Evidence

This skill is grounded in dated public implementation references:

1. Wikipedia's overview of cost-benefit analysis (https://en.wikipedia.org/wiki/Cost%E2%80%93benefit_analysis).
2. Wikipedia's overview of net present value used for time-discounted comparison (https://en.wikipedia.org/wiki/Net_present_value).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Trade-off Analysis](trade-off-analysis.md) — the multi-criteria comparison this skill monetizes.
- [Decision Making](decision-making.md) — the selection layer that applies the stated decision rule.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
