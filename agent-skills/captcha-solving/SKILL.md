---
name: captcha-solving
description: Handle CAPTCHA encounters in authorized automation by detecting the challenge and escalating to an approved human or site-provided verification path.
metadata:
  source: skills/11-web/captcha-solving.md
  category: 11-web
---

## Description

Handle CAPTCHA encounters in authorized automation by detecting the challenge and escalating to an approved human or site-provided verification path.

## When to Use

Use only within an authorized web scope with explicit URL, session, data, and action boundaries.

## Inputs / Outputs / Failure Modes

| Area | Contract |
|---|---|
| Inputs | authorized browser session, challenge state, and permitted escalation method. |
| Outputs | challenge status and completed authorized verification or escalation result. |
| Failure modes | Wrong origin, stale page state, authentication leakage, anti-automation controls, malformed content, unbounded crawling, or unverified postconditions. |

## Procedure

1. Establish the authorized origin, session scope, and target resource.
2. Validate the requested URL, selector, payload, or content against that scope.
3. Execute with bounded requests, pages, scripts, redirects, or data volume.
4. Preserve source URLs, timestamps, and relevant request/response provenance.
5. Validate the result and expected postcondition before continuing.
6. Stop on authorization, anti-automation, or ambiguity boundaries rather than bypassing them.

## Runnable Example

```python
task = {"capability": "captcha-solving", "authorized": True, "budget": 4}
assert task["authorized"] and task["budget"] > 0
print({"status": "bounded_web_operation", "capability": task["capability"]})
```

## Failure Modes

- Target origin or authorization cannot be verified.
- Page state changes between observation and action.
- Session tokens or personal data are exposed.
- Anti-bot, CAPTCHA, robots, or access controls are bypassed.
- Redirects, recursion, or data volume exceed the declared bounds.
- Output is accepted without validation.

## Safety Boundary

Do not bypass authentication, paywalls, CAPTCHA/anti-bot controls, rate limits, robots restrictions, or other access controls. Use only authorized sites and data, and never log credentials, session tokens, or sensitive cookies.

## Evidence

Canonical repository skill: this file. Structural conformance is governed by the repository schema, validation workflows, Agent Skills contract, and security gates. Web-specific claims require reproducible implementation evidence or authoritative primary documentation.

## Related

- 11-web
- input-guardrails
- output-guardrails
