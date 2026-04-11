# Image Understanding

**Category:** `perception`  
**Skill Level:** `intermediate`  
**Stability:** `stable`

### Description

Describe, classify, and analyze images using vision-language models. Understands objects, scenes, text, and spatial relationships.

### Example

```python
from openai import OpenAI
client = OpenAI()
response = client.chat.completions.create(
    model='gpt-4o',
    messages=[{'role': 'user', 'content': [
        {'type': 'text', 'text': 'What is in this image?'},
        {'type': 'image_url', 'image_url': {'url': image_url}}
    ]}]
)
```

### Frameworks / Models

- GPT-4o (OpenAI)
- Claude 3.7 Sonnet (Anthropic)
- Gemini 2.5 Pro (Google)
- LLaVA (open-source)

### Related Skills

- [OCR](ocr.md)
- [Visual Question Answering](../08-multimodal/vqa.md)
- [Screen Reading](screen-reading.md)
