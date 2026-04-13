---
title: "Visual Question Answering"
category: 08-multimodal
level: intermediate
stability: stable
description: "Apply visual question answering (VQA) in AI agent workflows."
added: "2025-03"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-08-multimodal-vqa.json)

# Visual Question Answering (VQA)

**Category:** `multimodal`  
**Skill Level:** `intermediate`  
**Stability:** `stable`
**Added:** 2025-03

### Description

Answer natural language questions about the content of an image. Combines visual understanding with language reasoning to handle factual, spatial, counting, and commonsense questions about visual scenes.

### Example

```python
from openai import OpenAI

client = OpenAI()
response = client.chat.completions.create(
    model='gpt-4o',
    messages=[{'role': 'user', 'content': [
        {'type': 'text', 'text': 'How many people are in this image and what are they doing?'},
        {'type': 'image_url', 'image_url': {'url': 'https://example.com/park.jpg'}}
    ]}]
)
print(response.choices[0].message.content)
```

### Structured VQA Output

```python
response = client.chat.completions.create(
    model='gpt-4o',
    messages=[{'role': 'user', 'content': [
        {'type': 'text', 'text': 'Answer as JSON: {"count": int, "activity": str, "setting": str}'},
        {'type': 'image_url', 'image_url': {'url': 'https://example.com/scene.jpg'}}
    ]}],
    response_format={'type': 'json_object'}
)
```

### Frameworks / Models

- GPT-4o, Claude 3.5 Sonnet (general VQA)
- LLaVA, InstructBLIP, PaliGemma (open-source)
- Google Gemini Vision
- Hugging Face `visual-question-answering` pipeline

### Related Skills

- [Image Captioning](image-captioning.md)
- [Image Understanding](../01-perception/image-understanding.md)
- [Object Detection](object-detection.md)
