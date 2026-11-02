---
title: "Stateless Session Tool Routing"
category: 07-tool-use
level: advanced
stability: experimental
description: "Route tool calls across stateless MCP sessions behind load balancers without sticky session workarounds."
added: "2026-11"
version: v1
related: [mcp-well-known-capability-discovery, tool-confidence-score-interpretation]
tags: [tools, mcp, routing, scale]
---
# Stateless Session Tool Routing

## Description
Route tool calls across stateless MCP sessions behind load balancers without sticky session workarounds. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- Tool calls must be served by any replica behind a load balancer, which requires session state to be handled explicitly.
- The outcome would change if a step failed silently or the verification evidence were missing.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | the tool call, the session context, and the declared session handoff mechanism. |
| Outputs | A structured record with the decision, rejected alternatives, and the verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Identify which parts of the session context the tool call actually depends on and externalize them.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Attach the externalized context to the call so any replica can serve it, and record the routing decision.
4. Compare the actual outcome against the acceptance criteria and record deviations.
5. On a replica that cannot resolve the context, fail closed with a re-dispatch instruction, and never pin the session to one replica.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Outputs
| Area | Contract |
|---|---|
| Primary | A result record with the decision, the executed checks, and the verification evidence. |
| Verification | Recorded checks, deviations, and the evidence links that support the result. |
| Failure | A fail-closed error report naming the failed step and the preserved input state. |

## Runnable Example
```python
def route_call(call, replicas):
    if "context" not in call:
        raise ValueError("stateless call missing context")
    picked = replicas[hash(call["session"]) % len(replicas)]
    return {"replica": picked, "pinned": False}
r = route_call({"session": "s1", "context": "ctx"}, ["r1", "r2", "r3"])
assert r["replica"] == "r1" and r["pinned"] is False
```

## Failure Modes
- Session state stays in replica memory so a load balancer failover loses the session.
- Sticky sessions are configured instead of externalizing the context.
- A call without context is served anyway and produces session-dependent behavior.
- Session handoff is declared but the receiving replica has no path to fetch the context.
- Retries land on a different replica and behave differently because state never left the first one.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- the 2026 MCP roadmap describing stateful sessions fighting load balancers and calling for an evolved transport and session model so servers can scale horizontally without holding state (the 2026 MCP Roadmap, Model Context Protocol Blog, October 2026) ([public signal](https://blog.modelcontextprotocol.io/posts/2026-mcp-roadmap/))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Mcp Well Known Capability Discovery](mcp-well-known-capability-discovery.md)
- [Tool Confidence Score Interpretation](tool-confidence-score-interpretation.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |
