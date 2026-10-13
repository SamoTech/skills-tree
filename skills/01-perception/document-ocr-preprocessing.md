---
title: "Document OCR Preprocessing"
category: 01-perception
level: advanced
stability: experimental
description: "Prepare scanned or photographed documents for OCR through deskewing, binarization, and layout cleanup, and verify that preprocessing measurably improved recognition before accepting it."
added: "2026-10"
version: v1
related: [ocr, document-parsing, image-super-resolution]
tags: [ocr, preprocessing, documents]
---

# Document OCR Preprocessing

## Description
Prepare scanned or photographed documents for OCR through deskewing, binarization, and layout cleanup, and verify that preprocessing measurably improved recognition before accepting it. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- raw page images are too degraded for reliable OCR and cleanup must be validated before downstream steps can proceed safely.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for document ocr preprocessing work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the document ocr preprocessing steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def choose_threshold(gray):
    # Otsu-style simple split on a two-level histogram
    counts = {0: gray.count(0), 255: gray.count(255)}
    return 128 if counts[0] and counts[255] else 256

def binarize(gray, t):
    return [0 if v < t else 255 for v in gray]

assert choose_threshold([0, 0, 255, 255]) == 128
assert binarize([10, 200], 128) == [0, 255]
assert binarize([10, 200], 256) == [0, 0]  # degenerate case stays blank, never invented ink
```

## Failure Modes
- Applying destructive binarization without measuring OCR impact.
- Deskewing with the wrong rotation direction.
- Inventing strokes in blank regions.
- Assuming one preprocessing chain fits every document type.
- Skipping validation pages before full runs.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Document ingestion pipelines remain a recurring enterprise agent request signal in public 2026 coverage; this is a dated signal, not an adoption metric.

## Related
- ocr.md
- document-parsing.md
- image-super-resolution.md
