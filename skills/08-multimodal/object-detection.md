---
title: "Object Detection"
category: 08-multimodal
level: intermediate
stability: stable
description: "Apply object detection in AI agent workflows."
added: "2025-03"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-08-multimodal-object-detection.json)

# Object Detection

**Category:** `multimodal`  
**Skill Level:** `intermediate`  
**Stability:** `stable`
**Added:** 2025-03

### Description

Locate and label objects within an image by producing bounding boxes, class labels, and confidence scores. Supports real-time detection, batch processing, and open-vocabulary detection via vision-language models.

### Example

```python
from transformers import pipeline

detector = pipeline('object-detection', model='facebook/detr-resnet-50')
results = detector('https://example.com/street.jpg')
for obj in results:
    print(f"{obj['label']} ({obj['score']:.0%}) at {obj['box']}")
# person (97%) at {'xmin': 40, 'ymin': 70, 'xmax': 180, 'ymax': 400}
```

### Open-Vocabulary with GPT-4o

```python
import base64, httpx
from openai import OpenAI

client = OpenAI()
image_data = base64.b64encode(httpx.get('https://example.com/scene.jpg').content).decode()
response = client.chat.completions.create(
    model='gpt-4o',
    messages=[{'role': 'user', 'content': [
        {'type': 'text', 'text': 'List all objects with approximate locations (top-left, center, etc.).'},
        {'type': 'image_url', 'image_url': {'url': f'data:image/jpeg;base64,{image_data}'}}
    ]}]
)
print(response.choices[0].message.content)
```

### Frameworks / Models

- DETR, YOLO v8/v9, RT-DETR (Hugging Face / Ultralytics)
- Grounding DINO (open-vocabulary)
- GPT-4o (natural language bounding box descriptions)
- Google Cloud Vision Object Localization
- AWS Rekognition Object and Scene Detection

### Related Skills

- [Image Classification](image-classification.md)
- [Image Understanding](../01-perception/image-understanding.md)
- [Visual Question Answering](vqa.md)
