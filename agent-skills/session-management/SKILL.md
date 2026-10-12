---
name: session-management
description: Create, rotate, and expire agent sessions with server-side state, opaque identifiers, and re-authentication on privilege change so identity evidence stays fresh instead of indefinitely trusted.
metadata:
  source: skills/14-security/session-management.md
  category: 14-security
  version: "v1"
---

# Session Management

Category: Security | Level: intermediate | Stability: experimental | Version: v1

## Description

A session is a server-side record plus a token that points at it; the token is evidence, not the identity itself. Session management keeps the record authoritative: opaque identifiers, rotation on login and privilege change, idle plus absolute expiry, and invalidation that actually invalidates. A leaked old token stops working because the record moved on — not because someone hoped it would.

## When to Use

Use when an agent or service maintains state across requests on behalf of an identity — web sessions, agent run sessions, or API tokens issued per engagement.

Do not use sessions as long-term authorization storage; a session says who someone was recently, and privilege should be re-established when the risk window grows.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `identity` | `string` | Yes | Authenticated identity the session represents |
| `idle_timeout` | `duration` | Yes | Max gap between requests before expiry |
| `absolute_ttl` | `duration` | Yes | Max total lifetime regardless of activity |
| `store` | `map[session_id -> record]` | Yes | Server-side session state |

## Procedure

1. Store session state server-side; issue only an opaque, high-entropy identifier to the client.
2. Set both idle and absolute expiry; whichever fires first ends the session.
3. Rotate the identifier on login, on privilege change, and on any suspected disclosure.
4. Invalidate the server record on logout; a client-side cookie clear is not invalidation.
5. Require re-authentication for sensitive operations even inside a valid session.
6. Record creation, rotation, and expiry events in the audit log with actor and time.

## Outputs

| Output | Type | Description |
|---|---|---|
| `session_id` | `string | null` | Opaque identifier for the active session |
| `status` | `string` | active, expired_idle, expired_absolute, or revoked |
| `events` | `list[(time, kind)]` | Session lifecycle events for auditing |

## Runnable Example

```python
def check_session(record, now, idle_timeout, absolute_ttl):
    """Evaluate a session record against idle and absolute limits."""
    if record["revoked"]:
        return "revoked"
    if now - record["last_seen"] > idle_timeout:
        return "expired_idle"
    if now - record["created"] > absolute_ttl:
        return "expired_absolute"
    return "active"

record = {"created": 100, "last_seen": 320, "revoked": False}
print(check_session(record, now=360, idle_timeout=30, absolute_ttl=300))
print(check_session(record, now=290, idle_timeout=30, absolute_ttl=300))
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Client-side session trust | State stored where the client can edit it | Keep the record server-side; issue opaque IDs |
| Eternal sessions | Only idle expiry configured | Enforce absolute TTL on top of idle timeout |
| Missing rotation | Same identifier across privilege changes | Rotate on login and privilege change |
| Predictable identifiers | Sequential or low-entropy session IDs | Use high-entropy random identifiers |
| Logout theater | Cookie cleared client-side, record alive | Invalidate the server record on logout |

## Security and Authority Boundary

A session carries recent identity evidence; it is not proof of continued presence or intent. Re-authentication, step-up verification, and the decision to trust a session at all remain with the identity provider and the calling service.

## Evidence

This skill is grounded in dated public implementation references:

1. The OWASP Session Management Cheat Sheet (https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html).
2. MDN's reference on the Set-Cookie header and session attributes (https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Set-Cookie).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Input Guardrails](input-guardrails.md) — request-level validation before session state is trusted.
- [Audit Logging](audit-logging.md) — where lifecycle events are recorded.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
