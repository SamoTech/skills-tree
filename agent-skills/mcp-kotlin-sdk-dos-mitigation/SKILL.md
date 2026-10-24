---
name: mcp-kotlin-sdk-dos-mitigation
description: Apply request-size and rate limits to an MCP Kotlin SDK server so unauthenticated request floods cannot exhaust it.
metadata:
  source: skills/07-tool-use/mcp-kotlin-sdk-dos-mitigation.md
  category: 07-tool-use
  version: "v1"
---
# Mcp Kotlin Sdk Dos Mitigation

## Description
Apply request-size and rate limits to an MCP Kotlin SDK server so unauthenticated request floods cannot exhaust it. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A Kotlin MCP SDK deployment is exposed to request floods and must apply the mitigations before the patched release lands.
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
3. Measure the current request ceiling, apply connection, request-size, and rate limits at the gateway, and verify the flood case is rejected before reaching tool execution.
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
def mitigate(requests, limits):
    allowed = []
    for r in requests:
        if r["size"] > limits["max_size"]:
            allowed.append({"id": r["id"], "result": "rejected_size"})
        elif r["client"] not in limits["rate_window"]:
            limits["rate_window"].add(r["client"])
            allowed.append({"id": r["id"], "result": "allowed"})
        else:
            allowed.append({"id": r["id"], "result": "rejected_rate"})
    return allowed

limits = {"max_size": 1024, "rate_window": set()}
out = mitigate([{"id": 1, "size": 512, "client": "a"}, {"id": 2, "size": 2048, "client": "a"}, {"id": 3, "size": 512, "client": "a"}], limits)
assert [o["result"] for o in out] == ["allowed", "rejected_size", "rejected_rate"]
```

## Failure Modes
- Rate limits are applied per connection instead of per client so floods multiply connections.
- Size limits reject the body but still buffer it fully in memory.
- Limits are tuned without measuring the actual request ceiling.
- The mitigation is applied on one endpoint while admin endpoints stay unlimited.
- The patched SDK is assumed to remove the need for gateway limits.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- The HaiND VulnCheck batch of October 2026 records an unauthenticated denial-of-service flaw in the official MCP Kotlin SDK among 22 agent and MCP CVEs (al-ice.ai, dated October 2026) ([public signal](https://al-ice.ai/posts/2026/10/haind-vulncheck-day-two-22-agent-mcp-cves-october-2026/))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Mcp Server Rate Limit Backoff](../07-tool-use/mcp-server-rate-limit-backoff.md)
- [Mcp Sdk Cve Batch Triage Operations](../14-security/mcp-sdk-cve-batch-triage-operations.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
