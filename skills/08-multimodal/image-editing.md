---
title: "Image Editing"
category: 08-multimodal
level: advanced
stability: stable
description: "Apply image editing in AI agent workflows."
added: "2025-03"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-08-multimodal-image-editing.json)

# Image Editing

**Category:** `multimodal`  
**Skill Level:** `advanced`  
**Stability:** `stable`
**Added:** 2025-03

### Description

Modify existing images using natural language instructions. Supports inpainting (fill masked regions), outpainting (extend canvas), style transfer, background removal, object removal, and region-specific edits via diffusion models or instruction-tuned vision models.

### Example

```python
from openai import OpenAI
import base64

client = OpenAI()

with open('original.png', 'rb') as img, open('mask.png', 'rb') as mask:
    response = client.images.edit(
        model='dall-e-2',
        image=img,
        mask=mask,
        prompt='Replace the background with a sunny beach scene',
        size='1024x1024'
    )
print(response.data[0].url)
```

### Inpainting with Diffusers

```python
from diffusers import StableDiffusionInpaintPipeline
import torch
from PIL import Image

pipe = StableDiffusionInpaintPipeline.from_pretrained(
    'runwayml/stable-diffusion-inpainting', torch_dtype=torch.float16
).to('cuda')

image = Image.open('photo.png').convert('RGB')
mask = Image.open('mask.png').convert('RGB')
result = pipe(prompt='a red sports car', image=image, mask_image=mask).images[0]
result.save('edited.png')
```

### Frameworks / Models

- DALL-E 2 inpainting (OpenAI)
- Stable Diffusion Inpainting (Hugging Face / Diffusers)
- Adobe Firefly API
- Clipdrop / Stability AI API
- InstructPix2Pix (text-guided editing)

### Related Skills

- [Image Generation](image-generation.md)
- [Image Captioning](image-captioning.md)
- [Object Detection](object-detection.md)
