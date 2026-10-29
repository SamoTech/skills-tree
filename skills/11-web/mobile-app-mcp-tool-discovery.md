---
title: "Mobile App Mcp Tool Discovery"
category: 11-web
level: advanced
stability: experimental
description: "Discover mobile-app MCP tools so that agents find app-provided functions with their schemas before calling them."
added: "2026-10"
version: v1
related: [offline-knowledge-pack-web-mirroring, appfunctions-mcp-tool-implementation]
tags: [mcp, discovery, mobile, tools]
---
# Mobile App Mcp Tool Discovery

## Description
Discover mobile-app MCP tools so that agents find app-provided functions with their schemas before calling them. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- An agent needs a capability that lives inside a mobile application exposed over MCP.
- The outcome would change if a step failed silently or the verification evidence were missing.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | the declared input set, policy thresholds, and explicit acceptance criteria. |
| Outputs | A structured record with the decision, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Enumerate the app's declared MCP tools, validate each advertised schema, and bind the chosen tool with its exact input contract recorded before the first call.
4. Compare the actual outcome against the acceptance criteria and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Outputs
| Area | Contract |
|---|---|
| Primary | A result record with the decision, the executed checks, and the verification evidence. |
| Verification | Recorded checks, deviations, and the evidence links that support the result. |
| Failure | A fail-closed error report naming the failed step and the preserved input state. |

## Runnable Example
```python
def discover(registry, need):
    hits = [t for t in registry if need in t["actions"] and t["schema"]]
    return hits[0] if hits else None
reg = [{"name": "orders", "actions": ["status"], "schema": {"order_id": "str"}}]
t = discover(reg, "status")
assert t["name"] == "orders" and discover(reg, "pay") is None
```

## Failure Modes
- A tool is called by name without validating its advertised schema.
- Schema-less entries are treated as callable and fail at runtime.
- The discovery cache is never invalidated and stale tools linger after app updates.
- Tool choice ignores the app's identity and calls a similarly named foreign tool.
- Discovered tool scopes are never compared to the agent's granted scope.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- the Android Dev Summit AppFunctions API uses the Model Context Protocol to turn standard mobile applications into interactive tools for system agents (blog.luandnh.com, dated October 29, 2026) ([public signal](https://blog.luandnh.com/en/ai-daily/2026-10-29/))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Offline Knowledge Pack Web Mirroring](offline-knowledge-pack-web-mirroring.md)
- [Appfunctions Mcp Tool Implementation](../05-code/appfunctions-mcp-tool-implementation.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
