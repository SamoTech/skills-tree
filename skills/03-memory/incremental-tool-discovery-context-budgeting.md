---
title: "Incremental Tool Discovery Context Budgeting"
category: 03-memory
level: advanced
stability: experimental
description: "Budget agent context across incremental tool discovery by deciding which servers, tools, and schemas to keep resident."
added: "2026-11"
version: v1
related: [context-window-budget-planning, memory-retrieval-latency-budgeting]
tags: [memory, budgeting, mcp, discovery]
---
# Incremental Tool Discovery Context Budgeting

## Description
Budget agent context across incremental tool discovery by deciding which servers, tools, and schemas to keep resident. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- An agent discovers tools incrementally across a long session.
- Resident tool schemas must be evicted and reloaded against a context budget.
- Reload decisions must be recorded to avoid thrashing.

## Inputs
| Area | Contract |
|---|---|
| Inputs | The discovery results, the context budget, and the session task plan. |
| Outputs | A resident set naming loaded schemas, eviction candidates, and reload handles. |
| Safety | Fail closed by refusing to keep more schemas resident than the budget allows. |

## Procedure
1. Track the token cost of each loaded tool schema in the resident set.
2. Compare the resident cost against the context budget after each discovery step.
3. Rank schemas by planned usage from the session task plan.
4. Evict the lowest-ranked schemas when the budget is exceeded and record reload handles.
5. Reload an evicted schema only when the plan reaches a step that needs it.
6. Emit the resident set with costs, evictions, and reload counts for audit.

## Outputs
| Area | Contract |
|---|---|
| Primary | A resident tool-schema set with costs, eviction candidates, and reload handles. |
| Verification | Recorded cost accounting and eviction decisions that reproduce the resident set. |
| Failure | A fail-closed error report naming the budget breach and the withheld discovery step. |

## Runnable Example
```python
def budget_resident(loaded, plan_steps, budget):
    cost = sum(s["tokens"] for s in loaded)
    if cost <= budget:
        return {"resident": [s["name"] for s in loaded], "evicted": [], "cost": cost}
    ranked = sorted(loaded, key=lambda s: 0 if s["name"] in plan_steps else 1)
    evicted, kept, c = [], [], 0
    for s in ranked:
        if c + s["tokens"] > budget:
            evicted.append(s["name"])
        else:
            kept.append(s["name"]); c += s["tokens"]
    return {"resident": kept, "evicted": evicted, "cost": c}

loaded = [{"name": "search", "tokens": 400}, {"name": "pay", "tokens": 500}]
r = budget_resident(loaded, ["search"], budget=600)
assert r["resident"] == ["search"] and r["evicted"] == ["pay"] and r["cost"] == 400
```

## Failure Modes
- Discovery results are all kept resident and the budget is silently exceeded.
- Eviction ignores the task plan and needed schemas are reloaded repeatedly.
- Reload handles are dropped, so evicted schemas can never be restored.
- Eviction decisions are not recorded and thrashing cannot be diagnosed.
- The budget is treated as advisory and breaches are only noticed after failure.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- Uber's Omni MCP lets agents search for servers, discover relevant tools, retrieve individual schemas, and invoke selected tools as needed instead of loading thousands of definitions (InfoQ, November 2, 2026, dated November 2, 2026) ([public signal](https://www.infoq.com/news/2026/11/uber-mcp-gateway-ai-agents/))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Context Window Budget Planning](context-window-budget-planning.md)
- [Memory Retrieval Latency Budgeting](memory-retrieval-latency-budgeting.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |
