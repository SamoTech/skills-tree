---
name: web-login
description: Perform an authorized web login flow using supplied credentials or approved authentication mechanisms without exposing or persisting secrets unnecessarily.
metadata:
  source: skills/11-web/web-login.md
  category: 11-web
---

## Description

Perform an authorized web login flow using supplied credentials or approved authentication mechanisms without exposing or persisting secrets unnecessarily.

## When to Use

Use only within an authorized web scope with explicit origin, session, data, and action boundaries.

## Inputs / Outputs / Failure Modes

| Area | Contract |
|---|---|
| Inputs | authorized login endpoint, credential source, session policy, and expected authenticated state. |
| Outputs | verified authenticated session state without returning raw credentials or session secrets. |
| Failure modes | Wrong origin, unsafe redirect, oversized response, stale page state, credential leakage, access-control bypass, or unverified postcondition. |

## Procedure

1. Establish the authorized origin and resource scope.
2. Validate redirects, content type, size, and session boundaries.
3. Execute with explicit timeout, page, script, or artifact limits.
4. Preserve provenance and avoid logging secrets or sensitive session state.
5. Verify the final resource or authenticated state before reporting success.
6. Stop when authorization or security boundaries are encountered.

## Runnable Example

```python
task = {"capability": "web-login", "authorized": True, "budget": 4}
assert task["authorized"] and task["budget"] > 0
print({"status": "bounded_web_operation", "capability": task["capability"]})
```

## Failure Modes

- Authorization or final origin cannot be verified.
- Redirects leave the allowed scope.
- Response or screenshot exceeds resource bounds.
- Credentials, cookies, or tokens are exposed.
- Authentication or anti-bot controls are bypassed.
- Final state is not verified.

## Safety Boundary

Do not bypass authentication, CAPTCHA/anti-bot controls, paywalls, rate limits, robots restrictions, or other access controls. Never hard-code, log, or return passwords, session tokens, or private cookies.

## Evidence

Canonical repository skill: this file. Structural conformance is governed by the repository schema, validation workflows, Agent Skills contract, and security gates. Web-specific claims require reproducible implementation evidence or authoritative primary documentation.

## Related

- 11-web
- input-guardrails
- output-guardrails
