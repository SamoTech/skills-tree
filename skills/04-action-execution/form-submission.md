---
title: "Form Submission"
category: 04-action-execution
level: intermediate
stability: stable
version: v2
description: "Submit validated form data to a verified target and confirm the resulting state, with double-submit and secret-handling controls."
added: "2026-09"
related: [keyboard-input, input-sanitization, assertion]
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-04-action-execution-form-submission.json)

# Form Submission

**Category:** `action-execution`
**Skill Level:** `intermediate`
**Stability:** `stable`
**Added:** 2026-09

### Description

Submit validated form data to a verified target and confirm the resulting state. Validation happens before submission, the destination is checked against the approved scope, and success is confirmed from the response or resulting state rather than assumed.

### Inputs / Outputs

| Direction | Field | Type | Contract |
|---|---|---|---|
| Input | `fields` | map of `{name: value}` | Form payload; validated against required/optional fields first |
| Input | `target` | verified endpoint or form locator | The approved destination for this submission |
| Input | `idempotency_key` | string | Stable key so retries cannot double-submit |
| Output | `result` | `{status, reference}` | Submission outcome and a verifiable reference |
| Output | `errors` | list of string | Field-level validation failures, before any submission |

### Procedure
1. Validate every field: required fields present, types and formats correct, lengths bounded.
2. Verify the destination matches the approved target; never submit to a URL or form reached from unverified content.
3. Attach an idempotency key so an ambiguous outcome can be retried without duplicating the submission.
4. Redact or exclude secrets from logs and error messages; submit them only through the field the form defines for them.
5. Submit once, then confirm success from the response status or the resulting page state.
6. On timeout or ambiguous outcome, query the reference or idempotency key before re-submitting.

### Example

```python
def submit_form(fields: dict, required: list[str], idempotency_key: str) -> dict:
    missing = [k for k in required if not fields.get(k)]
    if missing:
        return {"status": "invalid", "errors": [f"missing: {k}" for k in missing], "reference": None}
    if len(idempotency_key) < 8:
        raise ValueError("idempotency key too short")
    return {"status": "validated", "errors": [], "reference": idempotency_key}

result = submit_form(
    {"email": "user@example.com", "name": "Ossama"},
    required=["email", "name"],
    idempotency_key="order-2026-11-26-001",
)
print(result)
```

### Related Skills

- [Keyboard Input](keyboard-input.md)
- [Input Sanitization](../14-security/input-sanitization.md)
- [Assertion](assertion.md)

## Failure Modes

- Submitting to an unverified destination reached through untrusted content.
- Missing validation: invalid payloads sent to a live endpoint instead of rejected locally.
- Secret leakage through logs, error messages, or page state dumps.
- Double submission on retry: always carry an idempotency key and check it before repeating.
- Assuming success from a completed request without confirming the response or resulting state.

## Changelog
- v2 (2026-11): Structural modernization; added the input/output contract table, an explicit procedure, a deterministic validation example, expanded failure modes, and version history.
- v1 (2026-09): Initial entry.

## Evidence

- https://agentskills.io/specification

Evidence status: implementation guidance only; no benchmark claim is made without reproducible evidence.
