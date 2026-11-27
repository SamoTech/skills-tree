---
title: "Screen Ocr"
category: 10-computer-use
level: advanced
stability: stable
version: v2
description: "Extract visible text from a verified screen region using OCR while preserving location and uncertainty."
added: "2025-03"
related: [screenshot-capture, visual-element-detection]
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-10-computer-use-screen-ocr.json)

# Screen Ocr

**Category:** `computer-use`
**Skill Level:** `advanced`
**Stability:** `stable`
**Added:** 2025-03

### Description

Extract visible text from a verified screen region using OCR while preserving location and uncertainty. OCR output is approximate untrusted data: every reading carries its source region and a confidence level, and sensitive content must be handled before results leave the session.

### Inputs / Outputs

| Direction | Field | Type | Contract |
|---|---|---|---|
| Input | region | object | The verified screen region (or full screen) to read, with its geometry |
| Input | expectation | object | The text expected to appear, when known, for verification |
| Output | readings | object | Extracted text spans with per-span region coordinates |
| Output | check | object | Confidence and expectation comparison, or an explicit low-confidence failure |

### Procedure
1. Capture a fresh image of the verified region (a stale screenshot invalidates coordinates).
2. Run OCR and record each text span with its bounding region.
3. Compare readings against the expectation when one is declared; flag glyph confusions (0/O, 1/l/I).
4. Screen for sensitive content (credentials, PII) before results are logged or transmitted.
5. Report spans with coordinates and confidence; mark low-confidence spans explicitly rather than guessing.

### Example

```python
capture = {"region": {"x": 40, "y": 120, "w": 600, "h": 80}, "fresh": True}
assert capture["fresh"], "OCR on a stale frame gives stale coordinates"
readings = [
    {"text": "Order total: 1042.50 USD", "conf": 0.97, "box": {"x": 48, "y": 140}},
    {"text": "Status: PENDING", "conf": 0.62, "box": {"x": 48, "y": 170}},
]
expectation = "Order total:"
assert readings[0]["text"].startswith(expectation), "reading does not match expectation"
low_conf = [r for r in readings if r["conf"] < 0.8]
status = "usable" if not low_conf else "low-confidence-spans-present"
print({"spans": len(readings), "low_confidence": len(low_conf), "status": status})
```

### Related Skills

- [Screenshot Capture](screenshot-capture.md) - the fresh frame this skill reads
- [Visual Element Detection](visual-element-detection.md) - locate UI elements instead of text
- [Input Sanitization](../14-security/input-sanitization.md) - OCR output is untrusted input

## Failure Modes

- Low contrast, anti-aliasing, or subpixel rendering produces plausible but wrong text.
- Glyph confusions (0/O, 1/l/I, 5/S) silently corrupt numbers and identifiers.
- The region is clipped or the window scrolled, so coordinates no longer match the UI.
- Sensitive content (credentials, PII) is extracted and echoed into logs or prompts.
- Low-confidence readings are presented as certain text without their confidence level.

## Changelog
- v2 (2026-11): Structural modernization; added the input/output contract table, a deterministic example, an execution procedure, and corpus-verified related links (replaced the non-corpus input-guardrails/output-guardrails/self-category pointers).
- v1 (2025-03): Initial entry.

## Evidence

- https://agentskills.io/specification

Evidence status: implementation guidance only; no benchmark claim is made without reproducible evidence.
