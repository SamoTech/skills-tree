---
name: image-gen-tool
description: Use an image-generation provider as a bounded agent capability. Validate prompts and parameters, keep credentials secret, and verify returned assets before downstream use.
---

# Image Generation Tool

## Description
Use an image-generation provider as a bounded agent capability. Validate prompts and parameters, keep credentials secret, and verify returned assets before downstream use.

## When to Use
Use this capability when the workflow explicitly requires image generation tool and the target interface is documented and authorized.

## Inputs / Outputs
- Inputs: validated task data, documented tool parameters, and authorization context.
- Outputs: structured provider result plus evidence needed to verify the outcome.

## Failure Modes
- Invalid or ambiguous inputs.
- Missing permissions, unavailable provider, rate limits, or transport failures.
- Credential exposure or excessive tool scope.
- Treating an acknowledgement as proof of a completed side effect.

## Runnable Example

```python
request = {"capability": "image-gen-tool", "validated": True}
assert request["validated"]
print("invoke only after validating the tool contract")
```

## Evidence
Repository-backed guidance; see the canonical skill under skills/07-tool-use/image-gen-tool.md and its cited provider documentation.

## Related
- 07-tool-use
- tool-guardrails
