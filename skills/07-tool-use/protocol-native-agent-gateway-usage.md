---
title: "Protocol Native Agent Gateway Usage"
category: 07-tool-use
level: advanced
stability: experimental
description: "Use a protocol-native agent gateway to reach MCP tools and A2A remote agents through one governed entry point."
added: "2026-10"
version: v1
related: [mcp-stateless-tool-invocation-pattern, a2a-remote-agent-tool-invocation]
tags: [protocol, native, agent, gateway, usage]
---
# Protocol Native Agent Gateway Usage

## Description
Use a protocol-native agent gateway to reach MCP tools and A2A remote agents through one governed entry point. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- An operator needs this capability to proceed safely and verifiably.
- The outcome would change if a step failed silently or the verification evidence were missing.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | the declared input set, policy thresholds, and explicit acceptance criteria. |
| Outputs | A structured record with the decision, rejected alternatives, and the verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Register each downstream tool or agent with the gateway under its native protocol, route invocations through the gateway's policy layer, and require the gateway's audit record for every routed call.
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
def route_call(gateway, target):
    entry = gateway["registry"].get(target["name"])
    if entry is None:
        raise ValueError("target not registered: " + target["name"])
    proto = entry["protocol"]
    if proto not in ("mcp", "a2a"):
        raise ValueError("unsupported protocol: " + proto)
    return {"routed": target["name"], "protocol": proto, "audited": True}

gw = {"registry": {"search": {"protocol": "mcp"}, "planner": {"protocol": "a2a"}}}
assert route_call(gw, {"name": "planner"})["protocol"] == "a2a"
```

## Failure Modes
- A tool is called directly around the gateway and its policy and audit layers are bypassed.
- MCP and A2A targets share one gateway credential and authority crosses protocol boundaries.
- The audit record is fetched asynchronously and a dropped record is never noticed.
- Gateway-level rate limits are treated as tool failures and retried past the quota.
- A target's protocol changes on redeploy and the gateway routes it under the stale protocol.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- Google Cloud shipped the first protocol-native agent gateway that understands both MCP and A2A (tech.yahoo.com, dated October 2026) ([public signal](https://tech.yahoo.com/ai/gemini/articles/google-cloud-ships-first-protocol-064707782.html))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [MCP Stateless Tool Invocation Pattern](../07-tool-use/mcp-stateless-tool-invocation-patterns.md)
- [A2A Remote Agent Tool Invocation](../07-tool-use/a2a-remote-agent-tool-invocation.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
