---
name: mcp-oauth-token-redirect-response-parsing
description: Parse MCP OAuth token-redirect responses so credential delivery is validated against the registered endpoint rather than the server claim.
metadata:
  source: skills/01-perception/mcp-oauth-token-redirect-response-parsing.md
  category: 01-perception
  version: "v1"
---

# MCP OAuth Token Redirect Response Parsing

## Description
Parse MCP OAuth token-redirect responses so credential delivery is validated against the registered endpoint rather than the server claim. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A client connects to an MCP server and the OAuth token destination must be verified against the registration, not the server metadata.
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
3. Validate each token-redirect response against the client-registered redirect endpoint list, reject unregistered destinations with a fail-closed record, and log the accepted destination in the connection record.
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
def accepted(destination, registered):
    return destination in registered
reg = ["https://client.example/callback"]
assert accepted("https://client.example/callback", reg) is True
try:
    accepted("https://evil.example/callback", reg)
    assert False
except AssertionError:
    pass
```

## Failure Modes
- The server-supplied redirect destination is trusted and tokens flow to an attacker endpoint.
- The registered endpoint list is stale and a rotated registration silently mismatches.
- Redirect validation happens only at first sign-in and stored tokens are never re-checked.
- Validation failures are retried against the unregistered destination to avoid breaking the session.
- The connection record omits the accepted destination and later audits cannot reconstruct the flow.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- 2026 both official MCP SDKs publish high-severity advisories for a flaw letting a malicious MCP server redirect OAuth credential delivery (dev.to, dated October 2026) ([public signal](https://dev.to/fabwaseem/mcp-security-in-2026-the-oauth-sdk-cves-tested-and-how-to-lock-down-your-server-3lln))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Agent Card Parsing](../01-perception/agent-card-parsing.md)
- [Webhook Payload Parsing](../01-perception/webhook-payload-parsing.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
