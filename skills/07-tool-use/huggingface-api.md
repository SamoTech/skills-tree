---
title: "HuggingFace API"
category: 07-tool-use
level: intermediate
stability: stable
description: "Apply huggingface api in AI agent workflows."
added: "2025-03"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-07-tool-use-huggingface-api.json)

# HuggingFace API

**Category:** `tool-use`  
**Skill Level:** `intermediate`  
**Stability:** `stable`
**Added:** 2025-03

### Description

Call HuggingFace Inference API to run open-source models for text, image, audio, and embedding tasks.

### Example

```python
import httpx

headers = {'Authorization': f'Bearer {HF_TOKEN}'}
r = httpx.post(
    'https://api-inference.huggingface.co/models/sentence-transformers/all-MiniLM-L6-v2',
    headers=headers,
    json={'inputs': 'What is RAG?'}
)
embedding = r.json()
```

### Related Skills

- [Embedding Generation](../12-data/embedding-generation.md)
- [OpenAI API](openai-api.md)
