---
name: tool-context-inflation-mitigation-reasoning
description: Reason about how to keep large tool catalogs out of agent context by choosing incremental discovery and selective schema retrieval.
metadata:
  source: skills/02-reasoning/tool-context-inflation-mitigation-reasoning.md
  category: 02-reasoning
  version: "v1"
---
# Tool Context Inflation Mitigation Reasoning

## Description
Reason about how to keep large tool catalogs out of agent context by choosing incremental discovery and selective schema retrieval. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A tool catalog has grown past what fits usefully in the agent context window.
- A task must decide which tools to search, discover, and load.
- Context savings must be weighed against extra discovery round trips.

## Inputs
| Area | Contract |
|---|---|
| Inputs | The catalog size, the task description, and the context budget. |
| Outputs | A loading plan naming the discovery queries, tools to load, and skipped remainder. |
| Safety | Fail closed by refusing plans that load the full catalog into context. |

## Procedure
1. Estimate the token cost of loading the full catalog definitions.
2. Compare that cost against the task's context budget and reject full loads that do not fit.
3. Derive discovery queries from the task description and rank catalog servers by relevance.
4. Plan incremental retrieval of only the tool schemas the task may invoke.
5. Add a fallback that loads one additional schema only when a step fails without it.
6. Record the plan with the estimated token savings and the skipped catalog portion.

## Outputs
| Area | Contract |
|---|---|
| Primary | A loading plan naming discovery queries, selected tools, and skipped catalog portion. |
| Verification | Recorded token estimates and query rankings that reproduce the plan. |
| Failure | A fail-closed error report naming the full-load attempt and the withheld plan. |

## Runnable Example
```python
def plan_loading(catalog, task, budget):
    full = sum(t["schema_tokens"] for t in catalog)
    if full > budget:
        queries = [w for w in task.split() if len(w) > 4][:3]
        ranked = sorted(catalog, key=lambda t: -t["relevance"])
        selected = [t for t in ranked if t["relevance"] > 0.3][:5]
        return {"mode": "incremental", "queries": queries, "load": [t["name"] for t in selected], "full_tokens": full}
    return {"mode": "full", "load": [t["name"] for t in catalog], "full_tokens": full}

catalog = [{"name": "search", "schema_tokens": 800, "relevance": 0.9}, {"name": "pay", "schema_tokens": 700, "relevance": 0.1}]
plan = plan_loading(catalog, "find flights for the trip", budget=1000)
assert plan["mode"] == "incremental" and plan["load"] == ["search"] and plan["queries"][0] == "flights"
```

## Failure Modes
- The full catalog is loaded and the task context budget is silently exceeded.
- Discovery queries are generic and every server is ranked equally relevant.
- Schema retrieval is planned but the extra round-trip latency is never accounted for.
- The fallback loads the entire catalog after a single step failure.
- Token savings are claimed without recording the estimate that produced them.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- Uber found that loading definitions for thousands of tools into agent context becomes inefficient and built Omni MCP to support incremental discovery where agents search for servers, discover relevant tools, and retrieve individual schemas (InfoQ, November 2, 2026, dated November 2, 2026) ([public signal](https://www.infoq.com/news/2026/11/uber-mcp-gateway-ai-agents/))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Token Efficiency Decision Modeling](token-efficiency-decision-modeling.md)
- [Budget Aware Reasoning](budget-aware-reasoning.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |
