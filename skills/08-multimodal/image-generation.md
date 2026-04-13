![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-08-multimodal-image-generation.json)

# Image Generation

**Category:** `multimodal`  
**Skill Level:** `intermediate`  
**Stability:** `stable`
**Added:** 2025-03

### Description

Generate new images from natural language text prompts using diffusion or autoregressive models.

### Example

```python
from openai import OpenAI
client = OpenAI()
response = client.images.generate(
    model='dall-e-3',
    prompt='A futuristic city skyline at sunset, cyberpunk style',
    size='1024x1024',
    quality='hd'
)
print(response.data[0].url)
```

### Frameworks / Models

- DALL-E 3 (OpenAI)
- Stable Diffusion (open-source)
- Midjourney
- Ideogram, Flux

### Related Skills

- [Image Captioning](image-captioning.md)
- [Image Editing](image-editing.md)
