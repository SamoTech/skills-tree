![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-13-creative-image-gen-prompt.json)

**Category:** Creative
**Skill Level:** `advanced`
**Stability:** stable
**Added:** 2025-03

### Description
Engineers detailed, model-specific prompts for image generation systems such as DALL-E, Stable Diffusion, and Midjourney. Applies techniques for subject, style, lighting, composition, aspect ratio, and negative prompt construction.

### Example
```python
import anthropic

client = anthropic.Anthropic()

def craft_image_prompt(concept: str, style: str, model: str = "sdxl") -> str:
    resp = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=300,
        messages=[{"role": "user", "content": (
            f"Create a detailed {model} image generation prompt for: '{concept}'.\n"
            f"Style: {style}. Include subject, lighting, composition, "
            "camera settings, and a concise negative prompt."
        )}]
    )
    return resp.content[0].text

print(craft_image_prompt("futuristic city at dawn", "cinematic realism"))
```

### Related Skills
- [Image Generation](../08-multimodal/image-generation.md)
- [Creative Writing](creative-writing.md)
