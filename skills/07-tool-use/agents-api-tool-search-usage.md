---
title: "Agents API Tool Search Usage"
category: 07-tool-use
level: advanced
stability: experimental
description: "Use Agents API tool search to discover and select tools at runtime against a pinned candidate catalog."
added: "2026-11"
version: v1
related: [mcp-tool, tool-capability-cataloging]
tags: [tools, api, search, discovery]
---
# Agents API Tool Search Usage

## Description
Use Agents API tool search to discover and select tools at runtime against a pinned candidate catalog. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- An agent must choose among many available tools at runtime.
- Tool search results must be vetted before invocation.
- The candidate catalog must be pinned for the run.

## Inputs
| Area | Contract |
|---|---|
| Inputs | The task need, the pinned tool catalog, and the search query. |
| Outputs | A tool selection record naming the query, ranked candidates, and chosen tool. |
| Safety | Fail closed by refusing to invoke any tool outside the pinned catalog. |

## Procedure
1. Pin the candidate tool catalog for the run with its version.
2. Form the search query from the task need, not from free text history.
3. Search the catalog and rank candidates by need match.
4. Vet each candidate for scope and permission fit.
5. Invoke only vetted candidates inside the pinned catalog.
6. Record the query, candidates, and invocation decisions.

## Outputs
| Area | Contract |
|---|---|
| Primary | A tool selection record naming the query, ranked candidates, and chosen tool. |
| Verification | Recorded search and vetting decisions that reproduce the selection. |
| Failure | A fail-closed refusal naming the out-of-catalog tool. |

## Runnable Example
```python
def search_and_pick(catalog, query, tools):
    hits = [t for t in tools if query in t["keywords"]]
    vetted = [t["name"] for t in hits if t["name"] in catalog]
    if not vetted:
        return {"invoke": None, "refused": hits[0]["name"] if hits else None}
    return {"invoke": vetted[0]}
cat = {"weather-api"}
tls = [{"name": "weather-api", "keywords": ["forecast"]},
       {"name": "random-tool", "keywords": ["forecast"]}]
assert search_and_pick(cat, "forecast", tls)["invoke"] == "weather-api"
```

## Failure Modes
- Search results are invoked without vetting for scope or permission.
- The catalog pin is skipped so new tools join mid-run.
- The query is built from raw conversation text and drifts.
- Out-of-catalog hits are invoked because they rank first.
- The selection record omits the search query.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- OpenAI DevDay 2026 brought tool search into the Agents API alongside multi-agent capabilities, tool calling, and context compaction (OpenAI DevDay 2026 Recap, dated November 5, 2026) ([public signal](https://openai.com/index/devday-2026-recap/))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [MCP Tool](mcp-tool.md)
- [Tool Capability Cataloging](tool-capability-cataloging.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |
