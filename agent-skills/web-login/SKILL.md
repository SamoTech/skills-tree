---
name: web-login
description: Perform an authorized web login flow using approved authentication mechanisms without exposing or persisting secrets unnecessarily. Use explicit authorization, bounded execution, provenance, and postcondition verification.
---

# Web Login

## Description

Perform an authorized web login flow using approved authentication mechanisms without exposing or persisting secrets unnecessarily.

## When to Use

Use only within an authorized web scope with explicit origin and session boundaries.

## Inputs / Outputs

- Inputs: authorized resource, policy constraints, session context, and resource limits.
- Outputs: verified web artifact or state with provenance and failure context.

## Procedure

1. Establish authorized scope.
2. Validate target and redirects.
3. Execute within explicit resource bounds.
4. Preserve provenance and protect secrets.
5. Verify the final resource or state.
6. Stop at access-control or authorization boundaries.

## Failure Modes

- Unauthorized or unexpected origin.
- Redirect escapes scope.
- Resource bounds exceeded.
- Credentials or session data exposed.
- Access controls bypassed.
- Final state unverified.

## Runnable Example

```python
task = {"capability": "web-login", "authorized": True, "budget": 4}
assert task["authorized"] and task["budget"] > 0
print({"status": "bounded_web_operation", "capability": task["capability"]})
```

## Evidence

Canonical repository skill: skills/11-web/web-login.md. Repository schema, validation workflows, Agent Skills contract, and security gates define local conformance. Web-specific claims require reproducible implementation evidence or authoritative primary documentation.

## Related

- 11-web
- input-guardrails
- output-guardrails
