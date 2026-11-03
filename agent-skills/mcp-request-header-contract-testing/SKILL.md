---
name: mcp-request-header-contract-testing
description: ""
metadata:
  source: skills/17-infrastructure/mcp-request-header-contract-testing.md
  category: 17-infrastructure
  version: "v1"
---

# Mcp Request Header Contract Testing

## Description
Contract-test the HTTP headers a stateless MCP deployment requires, such as protocol version and method, so gateway misconfiguration fails loudly. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- An MCP server sits behind gateways or proxies and header drift has already produced silent method routing failures.
- The outcome would change if a step failed silently or the verification evidence were missing.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | the header contract, the deployed gateway chain, and the conformance test fixtures. |
| Outputs | A structured record with the decision, rejected alternatives, and the verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Write down the required headers and their allowed values for every MCP method the server exposes.
2. Build fixtures that call each method with valid headers and record the expected responses.
3. Add negative fixtures per header, such as missing version and unknown method, expecting defined errors.
4. Run the suite against the gateway chain, not only the server directly.
5. On a fixture failure, block the gateway change and report the divergent header behavior.
6. Emit a structured result with fixture outcomes and the gateway chain tested.

## Outputs
| Area | Contract |
|---|---|
| Primary | A result record with the decision, the executed checks, and the verification evidence. |
| Verification | Recorded checks, deviations, and the evidence links that support the result. |
| Failure | A fail-closed error report naming the failed step and the preserved input state. |

## Runnable Example
```python
def check_headers(headers, required):
    missing = [h for h in required if h not in headers]
    if missing:
        return {"ok": False, "missing": missing}
    if not headers["MCP-Protocol-Version"].startswith("2026"):
        return {"ok": False, "missing": ["MCP-Protocol-Version"]}
    return {"ok": True}
req = ["MCP-Protocol-Version", "MCP-Method"]
assert check_headers({"MCP-Protocol-Version": "2026-07-28", "MCP-Method": "tools/call"}, req)["ok"] is True
assert check_headers({"MCP-Method": "tools/call"}, req)["missing"] == ["MCP-Protocol-Version"]
```

## Failure Modes
- Header conformance is tested against the server directly, bypassing the gateway chain.
- Missing-version requests are accepted and routed with an assumed protocol version.
- A gateway strips unknown custom headers and nothing fails until a method 404s.
- Negative fixtures do not exist, so undefined error behavior goes unnoticed.
- Fixture expectations are updated to match whatever the gateway returns.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- the stateless MCP specification carrying protocol version and method as HTTP headers that infrastructure must pass through, described in the Google and Cloudflare deployment write-ups (Google Developers Blog, dated August 5, 2026) ([public signal](https://developers.googleblog.com/scaling-ai-agent-infrastructure-with-the-mcp-stateless-updates/))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Session Pinning Migration Diagnostics](session-pinning-migration-diagnostics.md)
- [Elicitation Mrtr Migration](elicitation-mrtr-migration.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |
