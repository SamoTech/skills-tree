---
title: "Least-Privilege Scoping"
category: 14-security
level: intermediate
stability: experimental
description: "Scope every agent action to the minimum permission set the current step needs, with deny-by-default grants, explicit expiry, and per-action audit records so lateral movement stays contained."
added: "2026-10"
version: v1
related: ["permission-checking", "approval-before-destructive-tools"]
---

# Least-Privilege Scoping

Category: Security | Level: intermediate | Stability: experimental | Version: v1

## Description

A credential that can do everything will eventually do something you did not intend. Least-privilege scoping treats authorization as a narrow, expiring grant instead of ambient power: each step names the capability and resources it needs, receives exactly that, and loses it on completion. Deny-by-default evaluation, per-grant expiry, and revocation mean a compromised step can only reach what that step was already allowed to touch.

## When to Use

Use when an agent or automation holds credentials that can read, write, or delete beyond the single action it is performing — tool tokens, cloud roles, or API scopes.

Do not use as a substitute for permission checks at the point of use; scoping narrows what a grant covers, and each call still needs its own decision.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `requested_action` | `string` | Yes | The capability the step wants to invoke |
| `resources` | `list[resource_id]` | Yes | The specific objects the action targets |
| `policy` | `map[action -> allowed_resources]` | Yes | The standing policy grants are checked against |
| `expiry` | `duration` | No | Lifetime of the grant; defaults to the step boundary |

## Procedure

1. Start from deny-by-default: an unlisted action is rejected before any tool call is attempted.
2. Enumerate the exact capability and resource IDs the step needs; wildcard scopes require explicit justification.
3. Check the request against the standing policy, then issue a grant scoped to those resources with an expiry.
4. Evaluate each subsequent tool call against the active grant — resource by resource, not by coarse role.
5. Revoke the grant at step completion, and treat any post-revocation call as a policy violation to log.
6. Record issued grants and their use in an audit trail that answers: who, what scope, which resources, how long.

## Outputs

| Output | Type | Description |
|---|---|---|
| `grant` | `scope | null` | The issued grant, or null when denied |
| `decision` | `string` | Allow or deny with the policy rule that decided it |
| `audit_record` | `map` | Issuer, scope, resources, expiry, and usage count |

## Runnable Example

```python
def evaluate_grant(requested_action, resources, policy, expiry_seconds=300):
    """Deny by default; grant only what the policy explicitly allows."""
    if requested_action not in policy:
        return {"decision": "deny", "reason": "action not in policy"}
    allowed = policy[requested_action]
    if "*" in allowed:
        scope = list(resources)
    elif set(resources).issubset(set(allowed)):
        scope = list(resources)
    else:
        return {"decision": "deny", "reason": "resource outside policy"}
    return {
        "decision": "allow",
        "grant": {"scope": scope, "expires_in": expiry_seconds},
    }

policy = {"read_issue": ["issue/12", "issue/13"], "delete_issue": []}
print(evaluate_grant("read_issue", ["issue/12"], policy))
print(evaluate_grant("delete_issue", ["issue/12"], policy))
print(evaluate_grant("read_issue", ["issue/99"], policy))
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Standing admin token | One long-lived credential reused across steps | Issue per-step grants with expiry |
| Wildcard scope | Convenience grants like resource `*` | Require explicit justification and review |
| Scope creep | Step reuses a grant for adjacent resources | Evaluate each call against the grant, not the role |
| Orphaned grants | Completion paths that skip revocation | Revoke in a cleanup path and audit usage after expiry |
| Silent denies | Denials logged nowhere | Record every decision with the deciding rule |

## Security and Authority Boundary

Scoping limits what a compromised step can reach; it does not decide whether an action is correct. A perfectly scoped grant can still perform a wrong action — purpose review and destructive-action approval remain separate, human-owned checks.

## Evidence

This skill is grounded in dated public implementation references:

1. RFC 6749 defining scoped OAuth 2.0 access (https://www.rfc-editor.org/rfc/rfc6749).
2. Wikipedia's overview of the principle of least privilege (https://en.wikipedia.org/wiki/Principle_of_least_privilege).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Permission Checking](permission-checking.md) — the decision layer each scoped call still passes through.
- [Approval Before Destructive Tools](approval-before-destructive-tools.md) — the human gate that scope cannot replace for destructive actions.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
