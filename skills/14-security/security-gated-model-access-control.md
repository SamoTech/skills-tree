---
title: "Security Gated Model Access Control"
category: 14-security
level: advanced
stability: experimental
description: "Control access to security-capable models through an explicit entitlement gate with recorded grants, scoping, and revocation checks."
added: "2026-11"
version: v1
related: [gated-security-scope-reasoning, deterministic-publish-gate-execution]
tags: [access-control, gating, security]
---

# Security Gated Model Access Control

## Description
Control access to security-capable models through an explicit entitlement gate with recorded grants, scoping, and revocation checks. Access is bounded by recorded grants with expiry and scope rather than account-level trust.

## When to Use
- A security-capable model must only serve entitled customers.
- Grants need expiry and scope, not blanket access.
- Revocation must be verified, not assumed.

## Inputs
| Area | Contract |
|---|---|
| Inputs | The request context, the grant ledger, and the revocation list. |
| Outputs | An access decision naming the grant used, its scope, and its expiry state. |
| Safety | Fail closed by denying access when no unexpired in-scope grant exists. |

## Procedure
1. Resolve the requester's identity and requested capability scope.
2. Look up grants in the ledger matching the requester.
3. Reject grants that are expired, revoked, or out of scope.
4. Deny access when no valid grant remains.
5. Record the decision with the grant id and expiry state.
6. Emit the access decision with audit fields.

## Outputs
| Area | Contract |
|---|---|
| Primary | An access decision with grant id, scope, and expiry state. |
| Verification | The grant ledger entry that reproduces the decision. |
| Failure | A denial record with the missing-grant reason. |

## Runnable Example
```python
def decide(request, grants, now):
    valid = [g for g in grants
             if g["holder"] == request["holder"]
             and g["scope"] == request["scope"]
             and g["expires"] > now
             and not g.get("revoked")]
    if not valid:
        return {"allow": False, "deny": "no_valid_grant"}
    return {"allow": True, "grant": valid[0]["id"], "expires": valid[0]["expires"]}

grants = [{"holder": "daybreak-red", "scope": "security-research", "expires": 200, "id": "g1"},
          {"holder": "daybreak-red", "scope": "security-research", "expires": 50, "id": "g0", "revoked": True}]
req = {"holder": "daybreak-red", "scope": "security-research"}
assert decide(req, grants, 100)["allow"] is True
assert decide({"holder": "other", "scope": "security-research"}, grants, 100)["deny"] == "no_valid_grant"
assert decide(req, [{"holder": "daybreak-red", "scope": "security-research", "expires": 50, "id": "gx"}], 100)["deny"] == "no_valid_grant"
```

## Failure Modes
- Access is granted at the account level without scope.
- Expired grants continue to authorize requests.
- Revocation is issued but never verified against the ledger.
- Denial reasons are not recorded, blocking audits.
- Grant scope covers capabilities the customer did not request.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- GPT-6 Cyber is gated to Daybreak Red customers as a restricted security research release (AIBriefs, November 7, 2026) ([public signal](https://aibriefs.news/ai-news-today))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Gated Security Scope Reasoning](gated-security-scope-reasoning.md)
- [Deterministic Publish Gate Execution](deterministic-publish-gate-execution.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2022026-11-20` | Initial evidence-backed contract. |
