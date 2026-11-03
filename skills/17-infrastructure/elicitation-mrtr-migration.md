---
title: "Elicitation Mrtr Migration"
category: 17-infrastructure
level: advanced
stability: experimental
description: "Migrate a server-side elicitation flow from open-stream requests to Multi Round-Trip Requests, returning input_required and completing on the retry."
added: "2026-11"
version: v1
related: [worker-native-mcp-handler-deployment, mcp-request-header-contract-testing]
tags: [elicitation, migration, mcp, infrastructure]
---
# Elicitation Mrtr Migration

## Description
Migrate a server-side elicitation flow from open-stream requests to Multi Round-Trip Requests, returning input_required and completing on the retry. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A tool server still holds streams open for elicitation and the stateless protocol makes that pattern a deployment blocker.
- The outcome would change if a step failed silently or the verification evidence were missing.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | the legacy elicitation flow, the server operation definitions, and the migration compatibility matrix. |
| Outputs | A structured record with the decision, rejected alternatives, and the verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Map every legacy elicitation point to the operation whose retry will complete it.
2. Define the input_required result schema for each point, including the missing-input declaration.
3. Reimplement each elicitation as a returned result with the original operation resumable on retry.
4. Test each point with a client that performs the round trip, including cancel and retry-exhaustion paths.
5. Retire the open-stream elicitation path and record the compatibility break for clients.
6. Emit a structured result with the migration map, test outcomes, and retired paths.

## Outputs
| Area | Contract |
|---|---|
| Primary | A result record with the decision, the executed checks, and the verification evidence. |
| Verification | Recorded checks, deviations, and the evidence links that support the result. |
| Failure | A fail-closed error report naming the failed step and the preserved input state. |

## Runnable Example
```python
def elicitation_flow(server, op, answer):
    r1 = server(op)
    if r1.get("status") == "input_required":
        if answer is None:
            return {"completed": False, "reason": "cancelled"}
        r2 = server(dict(op, inputs=answer))
        return {"completed": r2.get("status") == "completed"}
    return {"completed": r1.get("status") == "completed"}
def srv(op):
    if "inputs" not in op:
        return {"status": "input_required", "missing": "color"}
    return {"status": "completed"}
assert elicitation_flow(srv, {"op": "design"}, None)["reason"] == "cancelled"
assert elicitation_flow(srv, {"op": "design"}, {"color": "blue"})["completed"] is True
```

## Failure Modes
- The stream path is kept as a fallback and clients never migrate to the retry flow.
- The missing-input declaration is vague, so clients guess the schema and fail.
- Cancel paths are untested and the operation hangs server-side.
- The compatibility break is not recorded and old clients break silently in production.
- Retry exhaustion leaves the operation in an undefined state instead of closing it.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- the MCP 2026-07-28 specification reworking server-initiated elicitation with Multi Round-Trip Requests where the server returns input_required and the client retries the operation with the collected input (Cloudflare blog, dated November 2026) ([public signal](https://blog.cloudflare.com/mcp-v2/))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Worker Native Mcp Handler Deployment](worker-native-mcp-handler-deployment.md)
- [Mcp Request Header Contract Testing](mcp-request-header-contract-testing.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |
