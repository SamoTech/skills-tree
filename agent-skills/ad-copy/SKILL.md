---
name: ad-copy
description: Apply ad copy as a bounded domain-specific AI capability with explicit scope, validation, and uncertainty handling.
---

# ad copy

## Description
Apply this domain-specific capability only within its declared scope. Preserve source context, validate inputs and outputs, and avoid unsupported certainty.

## When to Use
Use when the workflow explicitly requires this capability and the relevant domain, jurisdiction, and source material are established.

## Inputs / Outputs
- Inputs: validated source material, domain context, task constraints.
- Outputs: structured result with assumptions or uncertainty where material.

## Failure Modes
- Missing or ambiguous source context.
- Unsupported inference or domain-rule mismatch.
- Stale or conflicting evidence.
- Presenting generated output as professional advice without appropriate authorization.
- Skipping output verification.

## Runnable Example

```python
task = {"capability": "ad-copy", "validated": True}
assert task["validated"]
print("execute within declared domain scope")
```

## Evidence
Canonical repository skill: skills/16-domain-specific/ad-copy.md. Repository schema and validation workflows define local conformance.

## Related
- 16-domain-specific
- input-guardrails
- output-guardrails
