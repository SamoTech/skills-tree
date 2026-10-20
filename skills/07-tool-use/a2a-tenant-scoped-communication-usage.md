---
title: "A2A Tenant Scoped Communication Usage"
category: 07-tool-use
level: advanced
stability: experimental
description: "Use A2A tenant-scoped communication so cross-agent delegation carries tenant identity and isolation across every hop."
added: "2026-10"
version: v1
related: [a2a-agent-card-authoring, a2a-signed-agent-card-verification]
tags: [a2a, tenancy, delegation, isolation]
---
# A2A Tenant Scoped Communication Usage

## Description
Use A2A tenant-scoped communication so cross-agent delegation carries tenant identity and isolation across every hop. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- An agent delegates work to another organization's agent and tenant separation must survive the delegation.
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
3. Build the A2A request with the tenant fields from the v1.0 contract, verify the remote agent card before delegation, and record the tenant context and the remote signature in the delegation record.
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
def tenant_request(tenant, task):
    return {"task": task, "tenant": tenant}
def hop(req):
    assert "tenant" in req, "tenant context required"
    return req["tenant"]
assert hop(tenant_request("acme", "run-report")) == "acme"
try:
    hop({"task": "run-report"})
    assert False
except AssertionError:
    pass
```

## Failure Modes
- Tenant fields are dropped mid-chain and a later hop executes with ambient authority.
- The remote agent card is used from cache and a key rotation is missed.
- Tenant identity is derived from the request path and is spoofable.
- Delegation records omit the remote signature and cannot be verified later.
- One tenant's context is reused for another tenant's task after an identifier collision.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- 2026 A2A v1.0 adds tenant fields and signed agent cards to the cross-agent communication contract (omidsaffari.com, dated October 2026) ([public signal](https://omidsaffari.com/blog/a2a-protocol))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [A2a Agent Card Authoring](../07-tool-use/a2a-agent-card-authoring.md)
- [A2a Signed Agent Card Verification](../07-tool-use/a2a-signed-agent-card-verification.md)

## Changelog
| Version | Date | Notes |
|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
