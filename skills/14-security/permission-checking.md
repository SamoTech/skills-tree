---
title: "Permission Checking"
category: 14-security
level: advanced
stability: stable
description: "Authorize agent actions against explicit identities, capabilities, resource scopes, and policy constraints before executing tools or accessing data."
added: "2025-03"
updated: "2026-10"
version: v2
related: [audit-logging, human-in-loop, input-sanitization]
---

# Permission Checking

## Description

Permission checking is the authorization boundary between an agent's intent and an executable action. Evaluate the authenticated actor, requested action, target resource, granted scope, and policy constraints before invoking a tool or mutating state.

Prefer deny-by-default authorization with narrowly scoped capabilities. Authentication identifies the actor; authorization decides what that actor may do.

## Inputs / Outputs

| Input | Type | Required | Description |
|---|---|---:|---|
| `actor_id` | string | yes | Authenticated agent/service identity |
| `action` | string | yes | Requested operation |
| `resource` | string | yes | Target resource |
| `scopes` | set[str] | yes | Granted capabilities/scopes |
| `policy` | dict | yes | Resource and action constraints |

| Output | Type | Description |
|---|---|---|
| `allowed` | bool | Whether the action may proceed |
| `reason` | string | Safe decision explanation |
| `policy_id` | string | Policy version used for the decision |

## Runnable Example

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Decision:
    allowed: bool
    reason: str

GRANTS = {"agent-reader": {"read:orders"}, "agent-writer": {"read:orders", "write:orders"}}

def authorize(actor: str, action: str) -> Decision:
    if action in GRANTS.get(actor, set()):
        return Decision(True, "scope granted")
    return Decision(False, "scope not granted")

print(authorize("agent-reader", "write:orders"))
```

## Failure Modes

| Failure | Cause | Mitigation |
|---|---|---|
| Privilege escalation | Broad wildcard permissions | Use least-privilege scopes and resource constraints |
| Confused deputy | Agent uses a privileged service on behalf of an untrusted caller | Propagate caller identity and intent |
| TOCTOU | Resource changes between check and use | Revalidate immediately before sensitive operations |
| Stale grants | Long-lived cached authorization | Bound cache lifetime and invalidate on policy changes |
| Missing tenant boundary | Resource ID alone does not encode ownership | Include tenant/owner scope in authorization |
| Fail-open behavior | Authorization service unavailable | Default to deny for sensitive actions |

## Design Rules

1. Keep authentication and authorization separate.
2. Use explicit action/resource scopes.
3. Deny when the identity or policy cannot be established.
4. Revalidate high-risk operations immediately before execution.
5. Log authorization outcomes without leaking sensitive policy data.
6. Test both allowed and denied paths.

## References

- OWASP Authorization Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html
- OWASP API Security Top 10: https://owasp.org/API-Security/editions/2023/en/0x11-t10/

Evidence status: guidance is grounded in the cited OWASP authorization material; no framework-specific security guarantee is implied.

## Related Skills

- [Audit Logging](audit-logging.md)
- [Human In Loop](human-in-loop.md)
- [Input Sanitization](input-sanitization.md)
