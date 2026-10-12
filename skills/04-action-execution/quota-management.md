---
title: "Quota Management"
category: 04-action-execution
level: intermediate
stability: experimental
description: "Track and enforce consumption limits — API calls, model tokens, spend, rate windows — with explicit budgets, remaining-capacity reporting, and early refusal at the boundary."
added: "2026-10"
version: v1
related: ["api-call", "http-request"]
---

# Quota Management

Category: Action Execution | Level: intermediate | Stability: experimental | Version: v1

## Description

Quotas turn a request to use resources responsibly into a number. This skill tracks consumption against an explicit budget per resource and window, reports remaining capacity before an operation starts, and refuses work at the boundary instead of discovering the limit inside an error response. The failure mode it exists to prevent is the silent approach to exhaustion, where an agent runs out mid-task.

## When to Use

Use when operations consume a metered resource — third-party API calls, model tokens, spend against a budget, writes per window — and running out mid-task is worse than declining work.

Do not rely on provider error responses as the quota signal; by the time the provider refuses, the workflow is already interrupted.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `budget` | `map` | Yes | Limit per resource per window |
| `usage` | `map` | Yes | Consumption so far in the current window |
| `operation` | `map` | Yes | The operation with its estimated resource cost |

## Procedure

1. Declare the budget per resource per window at configuration time, with the window boundary explicit.
2. Track consumption at the point of use, attributing it to the operation that spent it.
3. Before starting an operation, check remaining capacity against its estimated cost and decline early when insufficient.
4. Refuse at the boundary with a stated reason — which quota, how much remains, when the window resets — instead of attempting and failing.
5. Report remaining capacity to the caller and the plan layer so scheduling can route around exhausted quotas.
6. Reconcile tracked usage against provider-reported usage on a schedule; drift means the tracker is wrong.

## Outputs

| Output | Type | Description |
|---|---|---|
| `decision` | `map` | Proceed or refuse with the reason and remaining capacity |
| `remaining` | `map` | Per-resource remaining capacity and window reset |
| `ledger` | `list` | Attribution records of consumption by operation |

## Runnable Example

```python
def check_quota(operation, usage, budgets):
    remaining = {}
    for resource, limit in budgets.items():
        remaining[resource] = limit - usage.get(resource, 0)
    shortfalls = {r: c for r, c in operation["cost"].items() if c > remaining.get(r, 0)}
    if shortfalls:
        return {"decision": "refuse", "shortfalls": shortfalls, "remaining": remaining}
    return {"decision": "proceed", "remaining": remaining}

usage = {"api_calls": 950, "model_units": 4_000_000}
budgets = {"api_calls": 1000, "model_units": 5_000_000}
op = {"id": "sync", "cost": {"api_calls": 80, "model_units": 200_000}}
print(check_quota(op, usage, budgets))
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Discovery by error | The provider refusal is the first signal | Check before starting the operation |
| Unattributed spend | Consumption is not tied to operations | Attribute at the point of use |
| Drift unmeasured | The tracker diverges from provider totals | Reconcile on a schedule |
| Silent near-boundary | Callers learn capacity is gone only at refusal | Report remaining capacity proactively |
| Window confusion | Limits are compared across different reset windows | State window boundaries explicitly |

## Security and Authority Boundary

Quota refusal is a spending control, not an obstacle to route around. Workloads must not work around exhausted quotas by switching identities or credentials; that pattern should be flagged when detected.

## Evidence

This skill is grounded in dated public implementation references:

1. Wikipedia's overview of rate limiting, of which quota management is the accounting layer (https://en.wikipedia.org/wiki/Rate_limiting).
2. Wikipedia's overview of the token bucket algorithm used for windowed limits (https://en.wikipedia.org/wiki/Token_bucket).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [API Call](api-call.md) — the execution primitive whose metering this skill governs.
- [HTTP Request](http-request.md) — the transport layer that surfaces rate-limit responses.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
