---
title: "Enterprise Tool Catalog Discovery Portal Implementation"
category: 11-web
level: advanced
stability: experimental
description: "Implement an internal portal where agents discover registered tools, their owners, and enablement state from a governed catalog."
added: "2026-11"
version: v1
related: [registry-server-metadata-discovery, api-discovery]
tags: [web, portals, discovery, governance]
---
# Enterprise Tool Catalog Discovery Portal Implementation

## Description
Implement an internal portal where agents discover registered tools, their owners, and enablement state from a governed catalog. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- Agents and teams need a web surface to discover governed tools and owners.
- Enablement state must be visible so agents do not plan around disabled tools.
- The portal must serve catalog data from the registry, not a copy.

## Inputs
| Area | Contract |
|---|---|
| Inputs | The registry API, the portal requirements, and the access policy. |
| Outputs | A portal implementation serving tool, owner, and enablement views from the registry. |
| Safety | Fail closed by refusing to serve registry data to identities outside the access policy. |

## Procedure
1. Define the portal routes for tool search, tool detail, and owner views.
2. Bind each route to the registry API as the single source of truth.
3. Render enablement state and owner metadata on every tool view.
4. Enforce the access policy so only authorized identities can query the catalog.
5. Cache registry responses with invalidation on registry event updates.
6. Emit the implementation with route tests and registry contract checks.

## Outputs
| Area | Contract |
|---|---|
| Primary | A discovery portal serving tools, owners, and enablement state from the registry. |
| Verification | Recorded route tests against registry fixtures that reproduce each view. |
| Failure | A fail-closed error report naming the unauthorized identity and the refused query. |

## Runnable Example
```python
def serve_tool_view(identity, tool_id, registry, policy):
    if identity not in policy["readers"]:
        return {"status": 403, "body": {"error": "forbidden"}}
    entry = registry.get(tool_id)
    if entry is None:
        return {"status": 404, "body": {"error": "unknown_tool"}}
    return {"status": 200, "body": {"tool": tool_id, "owner": entry["owner"], "enabled": entry["enabled"]}}

registry = {"search_flights": {"owner": "search-team", "enabled": False}}
policy = {"readers": {"agent-1", "dana"}}
ok = serve_tool_view("agent-1", "search_flights", registry, policy)
assert ok["status"] == 200 and ok["body"]["enabled"] is False and ok["body"]["owner"] == "search-team"
assert serve_tool_view("anonymous", "search_flights", registry, policy)["status"] == 403
assert serve_tool_view("agent-1", "ghost", registry, policy)["status"] == 404
```

## Failure Modes
- The portal serves a stale copy of the catalog and agents plan around removed tools.
- Enablement state is hidden and agents discover disabled tools only at invocation time.
- Access policy is not enforced and any internal identity can enumerate the catalog.
- Cache invalidation is missing and registry events never refresh the portal views.
- Owner metadata is dropped and discovery results cannot be routed for review.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- Uber's MCP Registry acts as the control plane maintaining tool definitions, schemas, ownership, and enablement that discovery surfaces consume (InfoQ, November 2, 2026, dated November 2, 2026) ([public signal](https://www.infoq.com/news/2026/11/uber-mcp-gateway-ai-agents/))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Registry Server Metadata Discovery](registry-server-metadata-discovery.md)
- [API Discovery](api-discovery.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |
