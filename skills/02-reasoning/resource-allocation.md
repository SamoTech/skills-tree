---
title: "Resource Allocation"
category: 02-reasoning
level: intermediate
stability: experimental
description: "Assign scarce resources — budget, capacity, attention — across competing demands by stating the objective, constraints, and the cost of what is left unfunded."
added: "2026-10"
version: v1
related: ["prioritization", "constraint-satisfaction"]
---

# Resource Allocation

Category: Reasoning | Level: intermediate | Stability: experimental | Version: v1

## Description

Resource allocation is deciding what does not get done. This skill structures that decision: state the objective explicitly, inventory demands with their expected returns and constraints, solve or approximate the assignment, and surface the marginal cost — what the objective loses at the boundary — so trade-offs are argued in the open rather than settled by whoever pushes hardest.

## When to Use

Use when demands exceed capacity — team time across projects, compute across workloads, budget across candidates — and an explicit assignment is more defensible than implicit juggling.

Do not allocate without recording what was left unfunded; an allocation with no visible remainder hides its own cost.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `capacity` | `map` | Yes | Available amounts per constrained resource |
| `demands` | `list` | Yes | Candidate demands with expected return and resource needs |
| `objective` | `enum` | Yes | Maximize total return, minimize shortfall, or meet a stated target |

## Procedure

1. State the objective and constraints as explicit expressions before looking at demands.
2. Inventory demands with their resource needs and expected returns, including uncertainty on both.
3. Rank demands by return per unit of the scarcest resource and test a greedy assignment as a baseline.
4. Where demands interact — dependencies, mutual exclusion, diminishing returns — solve with the interaction represented or state the approximation.
5. Record what the allocation left unfunded and the estimated cost of the top unfunded item.
6. State marginal values: what one more unit of each resource would be worth under this allocation.

## Outputs

| Output | Type | Description |
|---|---|---|
| `assignment` | `map` | Allocated amounts per demand |
| `unfunded` | `list` | Demands left unmet with their estimated cost |
| `shadow_prices` | `map` | Marginal value of one more unit per resource |

## Runnable Example

```python
def greedy_allocation(capacity, demands):
    ranked = sorted(demands, key=lambda d: -d["return"] / d["cost"])
    allocation, unfunded = {}, []
    for d in ranked:
        if d["cost"] <= capacity:
            allocation[d["id"]] = d["cost"]
            capacity -= d["cost"]
        else:
            unfunded.append(d["id"])
    return {"assignment": allocation, "unfunded": unfunded, "left": capacity}

demands = [
    {"id": "A", "cost": 40, "return": 100},
    {"id": "B", "cost": 50, "return": 90},
    {"id": "C", "cost": 30, "return": 45},
]
print(greedy_allocation(80, demands))
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Implicit allocation | Resources shift toward whoever argues loudest | State the objective and solve explicitly |
| Hidden remainder | The unfunded list is never recorded | Report what was left unfunded and its cost |
| Point estimates | Returns are treated as certain | Carry uncertainty and re-rank under adverse draws |
| Objective drift | The objective changes to fit a preferred answer | Fix the objective before demands are argued |
| Static plan | The allocation is never revisited as returns are realized | Re-allocate at stated checkpoints |

## Security and Authority Boundary

Allocation decisions encode priorities and can reveal strategic direction — reserved capacity, defense budgets, sensitive workloads. Treat allocation tables as sensitive when the demands are, and apply the same access control as the underlying plans.

## Evidence

This skill is grounded in dated public implementation references:

1. Wikipedia's overview of resource allocation (https://en.wikipedia.org/wiki/Resource_allocation).
2. Wikipedia's overview of the knapsack problem, the canonical constrained-assignment model (https://en.wikipedia.org/wiki/Knapsack_problem).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Prioritization](prioritization.md) — the ranking layer that feeds demand ordering.
- [Constraint Satisfaction](constraint-satisfaction.md) — the feasibility layer that defines what allocations are possible.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
