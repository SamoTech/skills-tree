---
name: pdf-tool
description: Use pdf tool as a bounded agent capability with validated inputs, least-privilege access, and verified results.
---

# PDF Tool

## Description
Use pdf tool only through a documented and authorized interface. Validate inputs, keep credentials outside prompts and source, and verify important outcomes.

## When to Use
Use when the workflow explicitly requires pdf tool and the target resource is authorized.

## Inputs / Outputs
- Inputs: validated task data, provider identifiers, and authorization context.
- Outputs: structured provider result and evidence sufficient for downstream verification.

## Failure Modes
- Invalid or ambiguous inputs.
- Permission, rate-limit, transport, or provider failures.
- Credential or private-data exposure.
- Unverified side effects.

## Runnable Example

```python
capability = "pdf-tool"
assert capability
print("validate provider contract before invocation")
```

## Evidence
Repository-backed guidance. See the canonical skill at skills/07-tool-use/pdf-tool.md and its provider documentation.

## Related
- 07-tool-use
- tool-guardrails
