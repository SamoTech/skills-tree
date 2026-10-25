---
title: "Agent Gateway Protocol Compatibility Matrix Testing"
category: 17-infrastructure
level: advanced
stability: experimental
description: "Run a compatibility matrix test of a dual-protocol agent gateway against the MCP and A2A client versions it claims to serve."
added: "2026-10"
version: v1
related: [mcp-stateless-gateway-horizontal-scaling, multi-framework-agent-interop-testing]
tags: [agent, gateway, protocol, compatibility, matrix, testing]
---
# Agent Gateway Protocol Compatibility Matrix Testing

## Description
Run a compatibility matrix test of a dual-protocol agent gateway against the MCP and A2A client versions it claims to serve. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

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
3. Enumerate the declared client-version matrix for both protocols, execute the contract suite per cell, and fail the gateway release when any declared cell is untested or red.
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
def matrix(cells, results):
    bad = [c for c in cells if results.get(c) != "green"]
    if bad:
        raise AssertionError("matrix cells not green: " + repr(bad))
    return "release-ok"

cells = [("mcp", "2026-07-28"), ("a2a", "1.0")
assert matrix(cells, {("mcp","2026-07-28"):"green", ("a2a","1.0"):"green"}) == "release-ok"
```

## Failure Modes
- Only the newest client versions are tested and the supported older versions are declared but unverified.
- A red cell is shipped with a known-issue note instead of failing the release.
- Protocol combinations are tested separately and never together under load.
- The matrix is rebuilt from the docs at release time and untested cells are labeled by default.
- Client versions in the matrix are named loosely and a patch release reruns the wrong suite.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- AWS documents how AgentCore Gateway supports the MCP 2026-07-28 spec, making dual-protocol gateway compatibility a release surface (aws.amazon.com, dated October 2026) ([public signal](https://aws.amazon.com/blogs/machine-learning/how-agentcore-gateway-supports-the-mcp-2026-07-28-spec/))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [MCP Stateless Gateway Horizontal Scaling](../17-infrastructure/mcp-stateless-gateway-horizontal-scaling.md)
- [Multi-Framework Agent Interop Testing](../17-infrastructure/multi-framework-agent-interop-testing.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
