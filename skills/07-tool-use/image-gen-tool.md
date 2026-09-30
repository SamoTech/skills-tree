---
title: "Image Generation Tool"
category: 07-tool-use
level: intermediate
stability: stable
description: "Use an image-generation API as an agent tool with validated prompts, explicit model parameters, and verified outputs."
added: "2026-09"
related: [07-tool-use, 08-multimodal]
---

# Image Generation Tool

## Description
Use an image-generation provider as a bounded agent tool. Validate the request before invocation, keep credentials server-side, make model and output parameters explicit, and verify that the returned asset can actually be consumed by the next workflow step.

## When to Use
- Generate an image from a text or structured prompt.
- Produce a controlled variant of an existing asset when the provider supports image editing.
- Return a provider response to an agent without exposing provider credentials.

## Inputs / outputs / failure modes

| Area | Guidance |
|---|---|
| Prompt | Specific visual intent, constraints, and required exclusions. |
| Model | Explicit provider model identifier; do not assume availability. |
| Parameters | Size, quality, format, and count only when supported by the selected model. |
| Output | Asset identifier, URL, or binary payload returned by the provider. |
| Security | Keep API keys in environment-managed secrets. |
| Verification | Confirm the response contains the expected asset before downstream use. |
| Failure modes | Invalid prompt, unsupported parameter, quota error, policy rejection, timeout, or unusable output. |

## Runnable Example

```python
import os
from openai import OpenAI

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

result = client.images.generate(
    model=os.environ["IMAGE_MODEL"],
    prompt="A clean technical illustration of an AI agent tool pipeline",
    size="1024x1024",
)

assert result.data and result.data[0]
print("image response received")
```

## Failure modes
- Hard-coding credentials or returning them through tool output.
- Assuming a model, size, or response field is supported without checking provider documentation.
- Treating an accepted request as proof that the asset is usable.
- Sending uncontrolled user input directly into a privileged image workflow.
- Persisting provider URLs without considering their lifetime or access requirements.

## Evidence
- OpenAI Images API documentation: https://platform.openai.com/docs/guides/images
- Repository schema and tool-use validation workflows are authoritative for repository conformance.

## Related
- 07-tool-use
- 08-multimodal
- input-guardrails
- output-guardrails
