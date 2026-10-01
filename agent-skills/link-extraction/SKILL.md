---
name: link-extraction
description: Extract and normalize hyperlinks from authorized web content with explicit domain and URL filtering rules. Use explicit authorization, bounded execution, provenance, and postcondition verification.
---

# Link Extraction

## Description

Extract and normalize hyperlinks from authorized web content with explicit domain and URL filtering rules.

## When to Use

Use only within an authorized web scope with explicit resource and action boundaries.

## Inputs / Outputs

- Inputs: authorized origin/session, task constraints, and bounded web operation parameters.
- Outputs: verified web observation or artifact with source provenance and failure context.

## Procedure

1. Establish origin, session, and scope.
2. Validate targets and requested actions.
3. Execute within request, page, script, redirect, or data limits.
4. Preserve provenance.
5. Verify the result and postcondition.
6. Stop at authorization or anti-automation boundaries.

## Failure Modes

- Authorization cannot be verified.
- Page state becomes stale.
- Credentials or session data are exposed.
- Access controls or anti-bot controls are bypassed.
- Resource bounds are exceeded.
- Output is accepted without validation.

## Runnable Example

```python
task = {"capability": "link-extraction", "authorized": True, "budget": 4}
assert task["authorized"] and task["budget"] > 0
print({"status": "bounded_web_operation", "capability": task["capability"]})
```

## Evidence

Canonical repository skill: skills/11-web/link-extraction.md. Repository schema, validation workflows, Agent Skills contract, and security gates define local conformance. Web-specific claims require reproducible implementation evidence or authoritative primary documentation.

## Related

- 11-web
- input-guardrails
- output-guardrails
