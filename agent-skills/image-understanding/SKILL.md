---
name: image-understanding
description: Transcribe, interpret, and ground visual content while preserving source coordinates, uncertainty, and provenance. Use for VQA, object localization, scene understanding, and structured visual extraction.
metadata:
  source: skills/01-perception/image-understanding.md
  category: 01-perception
  version: "v3"
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

### Inputs / Outputs

| Direction | Field | Type | Contract |
|---|---|---|---|
| Input | `image` | URL, file path, or base64 bytes | Image to analyze; JPEG/PNG/WebP within the runtime size limit |
| Input | `question` | string | Natural-language question or extraction instruction |
| Input | `detail` | `"low"` or `"high"` | Vision-detail hint; `high` preserves small text and fine coordinates |
| Output | `answer` | string | Direct answer or structured extraction result |
| Output | `grounding` | list of `{label, box, score}` | Optional bounding boxes in source-image coordinates |
| Output | `uncertainty` | string | Stated model uncertainty and unresolved regions; never dropped silently |

### Procedure
1. Confirm the requester is authorized to analyze the image and record its provenance.
2. Validate that the image decodes and note its dimensions; reject or bound oversized inputs.
3. Choose the model path: a multimodal LLM for open questions, a grounding model when coordinates are required.
4. Issue the request with `detail: "high"` when small text or precise localization matters.
5. Post-process grounding boxes back into source coordinates and verify at least one box per claimed object.
6. Return the answer with explicit uncertainty, provenance, and any regions the model could not resolve.

### Example
```python
# pip install openai httpx
from openai import OpenAI
import base64, httpx

def vqa(image_url: str, question: str) -> str:
    client = OpenAI()
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
```

### Advanced Example - Grounding DINO

```python type:illustrative
# pip install groundingdino-py
# Note: `groundingdino` is the import name for PyPI package `groundingdino-py`
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
- [OCR](ocr.md)
- [Video Understanding](video-understanding.md)
- [Screen Reading](screen-reading.md)
- [Visual Element Detection](../10-computer-use/visual-element-detection.md)
- [Chart Reading](chart-reading.md)

## Failure Modes

- Untrusted or malformed input: validate that the image decodes, bound resource usage, and preserve parser or model uncertainty.
- Ambiguous visual evidence: distinguish observed pixels from inferred interpretation and retain source references for every claim.
- Hallucinated grounding: verify each returned box with a second pass or a deterministic detector before acting on its coordinates.
- Sensitive or unauthorized source: require authorization, minimize retained data, and do not expose unrelated content.
- Model or provider outage: fall back to a smaller vision model or defer the task rather than returning fabricated results.

## Changelog
- v3 (2026-11): Structural modernization; added the input/output contract table, procedure, and skill-specific failure modes, and normalized related links to in-corpus targets.
- v1 (2025-03): Initial entry.

## Evidence

- https://agentskills.io/specification
- https://github.com/openai/openai-python

Evidence status: implementation guidance is grounded in the cited standards or primary implementation references; no benchmark claim is made without reproducible benchmark evidence.
