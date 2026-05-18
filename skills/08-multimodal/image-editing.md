---
title: "Image Editing"
category: 08-multimodal
level: advanced
stability: experimental
description: "Apply image editing and generation operations in AI agent workflows."
added: "2025-03"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-08-multimodal-image-editing.json)

# Image Editing
Category: multimodal | Level: advanced | Stability: experimental | Version: v1

## Description
Perform AI-driven image editing operations: inpainting, outpainting, style transfer, and background removal using diffusion models.

## Inputs
- `image`: PIL Image or file path
- `prompt`: text description of the desired edit
- `mask`: optional binary mask for inpainting
- `strength`: float 0–1 controlling edit intensity

## Outputs
- Edited `PIL.Image` object

## Example
```python
from diffusers import StableDiffusionInpaintPipeline
import torch

def inpaint(image, mask, prompt):
    pipe = StableDiffusionInpaintPipeline.from_pretrained(
        "runwayml/stable-diffusion-inpainting",
        torch_dtype=torch.float16,
    ).to("cuda")
    return pipe(prompt=prompt, image=image, mask_image=mask).images[0]
```

## Frameworks
| Framework | Method |
|---|---|
| 🤗 diffusers | `StableDiffusionInpaintPipeline`, `AutoPipelineForInpainting` |
| OpenAI | `images.edit` (DALL·E 3) |
| Replicate | hosted inpainting models via API |

## Dependencies
- package: diffusers
  tested_version: "0.33.1"
  confidence: verified
  notes: "Patched GHSA-98h9-4798-4q5v (arbitrary code execution via unsafe pickle in model loading). Use diffusers>=0.33.1 and only load models from trusted sources."

## Failure Modes
- VRAM exhaustion on consumer GPUs — use `torch_dtype=float16` and `enable_attention_slicing()`
- Mask misalignment produces artifacts — ensure mask is same resolution as image

## Related
- `image-understanding.md` · `multimodal-document-reading.md`

## Changelog
- v1 (2026-03): Initial entry
- v1.1 (2026-05): Bump diffusers to 0.33.1 (CVE patch)
