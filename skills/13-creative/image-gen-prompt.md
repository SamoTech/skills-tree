**Category:** Creative
**Skill Level:** Intermediate
**Stability:** stable
**Added:** 2025-03

### Description
Crafts detailed, model-optimised prompts for image generation APIs (DALL·E 3, Stable Diffusion, Midjourney). Structures prompts with subject, style, lighting, colour palette, composition, and negative prompt components to reliably produce the desired visual.

### Example
```python
import anthropic
import openai

anthropics_client = anthropic.Anthropic()
openai_client = openai.OpenAI()

# Step 1 — generate an optimised prompt
planning = anthropics_client.messages.create(
    model="claude-opus-4-5",
    max_tokens=512,
    messages=[{"role": "user", "content": (
        "Write an optimised DALL-E 3 prompt for: "
        "a futuristic Tokyo street at night, cyberpunk aesthetic, "
        "neon reflections on wet pavement, ultra-detailed, cinematic."
    )}]
)
image_prompt = planning.content[0].text

# Step 2 — generate the image
response = openai_client.images.generate(
    model="dall-e-3",
    prompt=image_prompt,
    size="1024x1024",
    quality="hd",
    n=1,
)
print(response.data[0].url)
```

### Related Skills
- [Image Generation](../08-multimodal/image-generation.md)
- [Creative Writing](creative-writing.md)
- [SVG/Vector Art Generation](svg-generation.md)
