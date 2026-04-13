---
title: "Image Classification"
category: 08-multimodal
level: basic
stability: stable
description: "Apply image classification in AI agent workflows."
added: "2025-03"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-08-multimodal-image-classification.json)

# Image Classification

**Category:** `multimodal`  
**Skill Level:** `basic`  
**Stability:** `stable`
**Added:** 2025-03

### Description

Assign one or more category labels to an image using a vision model or classifier. Supports zero-shot classification via CLIP-style models and few-shot classification via fine-tuned CNNs or ViTs.

### Example

```python
from transformers import pipeline

classifier = pipeline('image-classification', model='google/vit-base-patch16-224')
results = classifier('https://example.com/cat.jpg')
# [{'label': 'tabby cat', 'score': 0.94}, ...]
for r in results[:3]:
    print(f"{r['label']}: {r['score']:.2%}")
```

### Zero-Shot with CLIP

```python
from transformers import CLIPProcessor, CLIPModel
import requests
from PIL import Image

model = CLIPModel.from_pretrained('openai/clip-vit-base-patch32')
processor = CLIPProcessor.from_pretrained('openai/clip-vit-base-patch32')

image = Image.open(requests.get('https://example.com/dog.jpg', stream=True).raw)
labels = ['a dog', 'a cat', 'a car', 'a building']
inputs = processor(text=labels, images=image, return_tensors='pt', padding=True)
logits = model(**inputs).logits_per_image.softmax(dim=1)
print(dict(zip(labels, logits[0].tolist())))
```

### Frameworks / Models

- Google ViT, EfficientNet (Hugging Face)
- OpenAI CLIP (zero-shot)
- GPT-4o vision (multi-label natural language output)
- Google Cloud Vision API
- AWS Rekognition

### Related Skills

- [Image Understanding](../01-perception/image-understanding.md)
- [Image Captioning](image-captioning.md)
- [Object Detection](object-detection.md)
