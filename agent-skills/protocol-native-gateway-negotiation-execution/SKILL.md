---
name: protocol-native-gateway-negotiation-execution
description: Execute client-to-gateway negotiation against a protocol-native agent gateway that speaks both MCP and A2A.
metadata:
  source: skills/04-action-execution/protocol-native-gateway-negotiation-execution.md
  category: 04-action-execution
  version: "v1"
---

# Protocol Native Gateway Negotiation Execution

## Description
Execute client-to-gateway negotiation against a protocol-native agent gateway that speaks both MCP and A2A. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

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
3. Send the declared protocol hello for each required surface, pin the negotiated protocol versions, and abort any session where the gateway response deviates from the declared profile.
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
def negotiate(supported, gateway):
    chosen = {}
    for proto in ("mcp", "a2a"):
        if proto not in supported or proto not in gateway:
            raise ValueError("gateway lacks protocol: " + proto)
        v = min(supported[proto], gateway[proto])
        if v != gateway[proto]:
            raise ValueError("version mismatch for " + proto)
        chosen[proto] = v
    return chosen

sup = {"mcp":"2026-07-28","a2a":"1.0"}
gw = {"mcp":"2026-07-28","a2a":"1.0"}
assert negotiate(sup, gw)["a2a"] == "1.0"
```

## Failure Modes
- The gateway advertises a protocol but the session proceeds without pinning the version.
- A downgraded protocol response is accepted and a newer client feature is used anyway.
- Negotiation failure is retried with progressively wider protocol allowances.
- The MCP and A2A sessions are negotiated separately but share one auth context and leak authority across surfaces.
- The negotiated profile is not recorded and later requests cannot be checked against it.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- Google Cloud shipped the first protocol-native agent gateway that understands both MCP and A2A (tech.yahoo.com, dated October 2026) ([public signal](https://tech.yahoo.com/ai/gemini/articles/google-cloud-ships-first-protocol-064707782.html))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [HTTP Request](../04-action-execution/http-request.md)
- [Agent Protocol Version Negotiation](../15-orchestration/agent-protocol-version-negotiation.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
