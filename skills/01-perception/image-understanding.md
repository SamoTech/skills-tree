---
title: "Image Understanding"
category: 01-perception
level: intermediate
stability: stable
added: "2025-03"
description: "Apply image understanding in AI agent workflows."
---


![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-01-perception-image-understanding.json)

# Image Understanding

### Description
Extracts semantic meaning, spatial relationships, objects, text, and contextual information from images using multimodal LLMs, specialized vision models, and grounding pipelines. Supports visual question answering (VQA), scene graph generation, object detection with bounding boxes, and cross-modal retrieval.

### When to Use
- Answering natural-language questions about image content in agentic pipelines
- Detecting and localizing objects for downstream computer-use or robotics tasks
- Extracting embedded text (signs, labels, captions) combined with layout context
- Visual grounding: mapping noun phrases to bounding box coordinates

### Example
```python
from openai import OpenAI
import base64, httpx

def vqa(image_url: str, question: str) -> str:
    client = OpenAI()
    # Download and encode if local path
    img_b64 = base64.b64encode(httpx.get(image_url).content).decode()
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{
            "role": "user",
            "content": [
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_b64}", "detail": "high"}},
                {"type": "text", "text": question}
            ]
        }],
        max_tokens=512
    )
    return response.choices[0].message.content

# Advanced: grounding via Grounding DINO
from groundingdino.util.inference import load_model, predict
def ground_objects(image_path: str, caption: str) -> list[dict]:
    model = load_model("groundingdino_swint_ogc.py", "groundingdino_swint_ogc.pth")
    boxes, logits, phrases = predict(model, image_path, caption, box_threshold=0.35, text_threshold=0.25)
    return [{"phrase": p, "box": b.tolist(), "score": float(s)} for p, b, s in zip(phrases, boxes, logits)]
```

### Advanced Techniques
- **Chain-of-thought VQA**: prompt the model to describe the image step-by-step before answering
- **Dense captioning**: use LLaVA-1.6 or InternVL2 for region-level dense captions
- **CLIP embeddings**: retrieve semantically similar images from a vector store using CLIP `ViT-L/14`
- **Structured extraction**: force JSON output via function-calling to extract structured attributes (color, count, position)

### Related Skills
- `ocr`, `video-understanding`, `screen-reading`, `visual-element-detection`, `image-captioning`
