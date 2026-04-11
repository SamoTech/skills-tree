# Image Generation Tool

**Category:** `tool-use`  
**Skill Level:** `intermediate`  
**Stability:** `stable`

### Description

Generate images from text prompts as an agent tool, returning image URLs or base64 data.

### Example

```python
from openai import OpenAI

def generate_image(prompt: str, size='1024x1024') -> str:
    client = OpenAI()
    r = client.images.generate(model='dall-e-3', prompt=prompt, size=size)
    return r.data[0].url
```

### Related Skills

- [Image Generation](../08-multimodal/image-generation.md)
- [OpenAI API](openai-api.md)
