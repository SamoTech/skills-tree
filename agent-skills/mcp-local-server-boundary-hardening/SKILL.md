---
name: mcp-local-server-boundary-hardening
description: Harden local MCP server boundaries by declaring what each local server may reach, since the stdio transport is not a sandbox.
metadata:
  source: skills/14-security/mcp-local-server-boundary-hardening.md
  category: 14-security
  version: "v1"
---

# Mcp Local Server Boundary Hardening

## Description
Harden local MCP server boundaries by declaring what each local server may reach, since the stdio transport is not a sandbox. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A team runs local MCP servers on developer machines and must treat the stdio transport as an open boundary, not a sandbox.
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
3. Inventory each local server's reachable files, processes, and network endpoints, then declare and enforce the allowed set and fail closed when a server reaches beyond its declared boundary.
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
def enforce(call, boundary):
    if call["target"] not in boundary["allowed"]:
        return {"allowed": False, "reason": "outside-boundary"}
    return {"allowed": True, "reason": None}
b = {"allowed": {"~/.config/app", "/tmp/mcp"}}
assert enforce({"target": "/etc/shadow"}, b)["allowed"] is False
assert enforce({"target": "/tmp/mcp"}, b)["allowed"]
```

## Failure Modes
- A local server is trusted because it runs on localhost and it reads user files unchallenged.
- The declared boundary is recorded but not enforced at runtime and stays documentation.
- A server is granted the user's home directory wholesale to avoid friction.
- Prompt-injected tool output changes the server's working directory and exfiltrates outside the boundary.
- The boundary inventory is done once and new reachable endpoints appear after package updates unnoticed.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- the MCP project's Local Server Security guide added on October 5 covers what a local server can reach on a machine and notes the stdio transport is not a sandbox (eSEOspace State of MCP October 2026 report, dated October 28, 2026) ([public signal](https://eseospace.com/blog/state-of-mcp-october-2026/))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Sovereign Model Deployment Security](sovereign-model-deployment-security.md)
- [Agent Credential Vault Scope Minimization](agent-credential-vault-scope-minimization.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
