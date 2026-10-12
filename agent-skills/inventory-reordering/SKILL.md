---
name: inventory-reordering
description: Compute reorder points and order quantities from demand history, lead time, and safety stock with every formula input recorded so replenishment decisions rest on stated math rather than gut feel.
metadata:
  source: skills/16-domain-specific/inventory-reordering.md
  category: 16-domain-specific
  version: "v1"
---

# Inventory Reordering

Category: Domain-Specific | Level: intermediate | Stability: experimental | Version: v1

## Description

Reordering is arithmetic pretending to be intuition. The skill makes the math explicit: demand statistics from history, a reorder point from demand rate times lead time plus safety stock, an order quantity from policy (economic order quantity or a stated rule), and a comparison against stock on hand that emits a concrete reorder list. Every input — history window, lead time, service level — is recorded with the decision, so the same numbers regenerate the same order.

## When to Use

Use for any stocked item where running out has a cost and overstocking has another — spare parts, consumables, retail or warehouse inventory.

Do not use on sparse or stale demand history; a reorder point computed from three data points is a guess with extra decimals.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `demand_history` | `list[qty per period]` | Yes | Recent demand series for the item |
| `lead_time_days` | `number` | Yes | Expected replenishment delay |
| `stock_on_hand` | `number` | Yes | Current available quantity |
| `policy` | `map` | Yes | Safety stock rule, service level, and order quantity rule |

## Procedure

1. Fix the history window and clean the series — stockouts and promotions are noted, not silently averaged in.
2. Compute demand rate and variability; record the window and both statistics with the decision.
3. Compute the reorder point as demand rate times lead time plus safety stock, from the recorded inputs only.
4. Derive the order quantity from the stated policy — economic order quantity or a rule — with its formula and inputs recorded.
5. Compare stock on hand against the reorder point; items at or below it enter the reorder list with the computed quantity.
6. Emit the decision record: item, inputs, formulas, quantities, and date, so the order is reproducible.

## Outputs

| Output | Type | Description |
|---|---|---|
| `reorder_list` | `list[(item, qty)]` | Items to reorder now and their quantities |
| `reorder_points` | `map[item -> qty]` | Computed thresholds per item |
| `decision_record` | `map` | Inputs, formulas, and parameters used |

## Runnable Example

```python
def reorder_decision(demand, lead_time_days, stock_on_hand, safety_stock):
    """Compute the reorder point and decide whether to order."""
    demand_rate = sum(demand) / len(demand)
    reorder_point = demand_rate * lead_time_days + safety_stock
    if stock_on_hand <= reorder_point:
        return {"order": True, "reorder_point": round(reorder_point, 1)}
    return {"order": False, "reorder_point": round(reorder_point, 1)}

demand = [4, 6, 5, 7, 5, 3, 5]
print(reorder_decision(demand, lead_time_days=10, stock_on_hand=62, safety_stock=10))
print(reorder_decision(demand, lead_time_days=10, stock_on_hand=40, safety_stock=10))
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Stale history | Demand from a discontinued pattern drives the point | Refresh the window; flag aged series |
| Ignored lead-time variance | Only the mean lead time used | Size safety stock for lead-time variability |
| Double counting | In-transit orders counted as on hand | Exclude in-transit stock from the comparison |
| Seasonality blindness | An annual cycle flattened by the average | Use seasonal windows or explicit season factors |
| Unrecorded inputs | The order cannot be explained later | Emit the full decision record with every run |

## Security and Authority Boundary

Reordering math supports the operational decision; supplier risk, cash constraints, and contract terms remain with procurement. A computed quantity is a recommendation with provenance, not a purchase order.

## Evidence

This skill is grounded in dated public implementation references:

1. Wikipedia's overview of inventory management (https://en.wikipedia.org/wiki/Inventory_management).
2. Wikipedia's overview of the economic order quantity model (https://en.wikipedia.org/wiki/Economic_order_quantity).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Invoice Processing](invoice-processing.md) — the purchasing documents that follow reorder decisions.
- [Stock Lookup](stock-lookup.md) — current holdings data feeding the comparison.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
