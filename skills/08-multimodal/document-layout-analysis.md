---
title: "Document Layout Analysis"
category: 08-multimodal
level: advanced
stability: stable
description: "Apply document layout analysis in AI agent workflows."
added: "2025-03"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-08-multimodal-document-layout-analysis.json)

# Document Layout Analysis

**Category:** `multimodal`  
**Skill Level:** `advanced`  
**Stability:** `stable`
**Added:** 2025-03

### Description

Understand the visual and structural layout of a document page — detecting regions such as text blocks, headings, tables, figures, captions, headers, and footers. Enables ordered reading, structure-aware extraction, and multimodal document understanding beyond raw OCR.

### Example

```python
from transformers import AutoProcessor, AutoModelForObjectDetection
from PIL import Image
import torch

processor = AutoProcessor.from_pretrained('microsoft/layoutlmv3-base')
model = AutoModelForObjectDetection.from_pretrained('microsoft/layoutlmv3-base')

image = Image.open('invoice.png').convert('RGB')
inputs = processor(images=image, return_tensors='pt')
outputs = model(**inputs)

# Post-process bounding boxes
target_sizes = torch.tensor([image.size[::-1]])
results = processor.post_process_object_detection(outputs, threshold=0.5, target_sizes=target_sizes)[0]
for label, box in zip(results['labels'], results['boxes']):
    print(f"{model.config.id2label[label.item()]}: {box.tolist()}")
```

### With DocTR

```python
from doctr.io import DocumentFile
from doctr.models import ocr_predictor

model = ocr_predictor(pretrained=True)
doc = DocumentFile.from_pdf('report.pdf')
result = model(doc)
for page in result.pages:
    for block in page.blocks:
        for line in block.lines:
            print(' '.join(w.value for w in line.words))
```

### Frameworks / Models

- LayoutLMv3 (Microsoft) — layout + text + vision
- DocTR (Mindee) — end-to-end document OCR with layout
- Detectron2 + PubLayNet — academic document layout
- Azure Document Intelligence (Form Recognizer)
- Google Document AI

### Related Skills

- [Document Parsing](../01-perception/document-parsing.md)
- [OCR](../01-perception/ocr.md)
- [Table Extraction](../01-perception/table-extraction.md)
- [PDF Parsing](../01-perception/pdf-parsing.md)
