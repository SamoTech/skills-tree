---
title: "Supplier Agent Access Delegation Design"
category: 09-agentic-patterns
level: advanced
stability: experimental
description: "Design delegation of supplier-side agent access with named boundary owners, scoped grants, and expiry-bound sessions."
added: "2026-10"
version: v1
related: [approval-bound-tool-invocation-pattern, persistent-agent-identity-binding-patterns]
tags: [supplier, agent, access, delegation, design]
---
# Supplier Agent Access Delegation Design

## Description
Design delegation of supplier-side agent access with named boundary owners, scoped grants, and expiry-bound sessions. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

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
3. For each supplier, name the boundary owner, declare the scoped grant and its expiry, and record the revocation path before any delegation executes.
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
def design_delegation(suppliers, now_day):
    out = []
    for s in suppliers:
        valid = s["start_day"] <= now_day < s["start_day"] + s["ttl_days"]
        out.append({"supplier": s["name"], "owner": s["owner"],
                    "status": "active" if valid else "expired",
                    "revocation": s["revoke_path"] is not None})
    return out

sup = [{"name":"parts-co","owner":"procurement","start_day":1,"ttl_days":30,"revoke_path":"registry/parts-co"}]
out = design_delegation(sup, now_day=31)
assert out[0]["status"] == "expired" and out[0]["revocation"] is True
```

## Failure Modes
- Delegation is granted without a named boundary owner and nobody revokes it after the contract ends.
- Grants have no expiry and supplier access survives the supplier relationship.
- The revocation path is declared but never tested and fails during an incident.
- Supplier agents receive the org-wide role instead of a scoped grant.
- Third-party delegations are not inventoried so a breached supplier path is discovered during an incident.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- The Norforge campaign entered at least one organization through a third-party supplier, making supplier-side agent delegation a recorded attack surface (agenticexpo.ai, dated October 23, 2026) ([public signal](https://www.agenticexpo.ai/news/weekly-roundup-23-october-2026))
- The roundup states that granting third-party agents access without equivalent scrutiny builds defences around the wrong perimeter (agenticexpo.ai, dated October 23, 2026) ([public signal](https://www.agenticexpo.ai/news/weekly-roundup-23-october-2026))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Approval Bound Tool Invocation Pattern](../09-agentic-patterns/approval-bound-tool-invocation-pattern.md)
- [Persistent Agent Identity Binding Patterns](../09-agentic-patterns/persistent-agent-identity-binding-patterns.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
