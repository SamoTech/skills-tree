---
title: "MCP Invocation Approval Binding Memory"
category: 03-memory
level: advanced
stability: experimental
description: "Record which approved MCP invocation each approval header was bound to so later requests cannot reuse a stale approval."
added: "2026-10"
version: v1
related: [permission-grant-history-memory, memory-provenance-tracking]
tags: [mcp, invocation, approval, binding, memory]
---
# MCP Invocation Approval Binding Memory

## Description
Record which approved MCP invocation each approval header was bound to so later requests cannot reuse a stale approval. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

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
3. Store each approval with the exact invocation fingerprint it was granted for, verify the fingerprint on every reuse attempt, and expire approvals that outlive their invocation.
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
def bind_approval(approvals, req):
    fp = req["tool"] + ":" + ",".join(sorted(req["args"]))
    rec = approvals.get(req["approval_id"])
    if rec is None or rec["fingerprint"] != fp:
        raise ValueError("approval not bound to this invocation")
    return rec

apps = {"a1": {"fingerprint": "search:q,scope"}}
req = {"approval_id":"a1","tool":"search","args":["scope","q"]}
assert bind_approval(apps, req)["fingerprint"] == "search:q,scope"
```

## Failure Modes
- An approval is stored without an invocation fingerprint and any later call reuses it.
- Argument order differences produce different fingerprints and valid reuse is blocked while broad reuse passes.
- Approvals are never expired and a grant from a retired tool version stays valid.
- The binding record omits the approver identity and the audit cannot attribute the grant.
- Fingerprint comparison is case-insensitive and two distinct arguments are treated as the same invocation.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- Agent Framework .NET 1.24.0 binds MCP approval headers to the approved invocation, the exact defect class this contract addresses (releasebot.io, dated October 7, 2026) ([public signal](https://releasebot.io/updates/microsoft/agent-framework))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Permission Grant History Memory](../03-memory/permission-grant-history-memory.md)
- [Memory Provenance Tracking](../03-memory/memory-provenance-tracking.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
