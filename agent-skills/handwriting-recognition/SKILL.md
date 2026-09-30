---
name: handwriting-recognition
description: Transcribe handwritten text from images while preserving uncertainty, illegible regions, layout observations, and source-image provenance. Use domain context only as a disambiguating hint.
license: MIT
metadata:
  source: skills/01-perception/handwriting-recognition.md
  version: "v2"
---

# Handwriting Recognition

1. Preserve the original image and record image/page provenance.
2. Identify language, writing direction, and document layout when possible.
3. Transcribe legible content without silently correcting spelling.
4. Mark illegible or ambiguous characters explicitly.
5. Preserve lists, tables, annotations, and crossed-out content as structural observations.
6. Use domain context only to disambiguate plausible readings, never to invent text.

## Failure modes

- Cursive or low-resolution writing: mark uncertain spans and request a better source when material.
- Mixed scripts: segment by language/script before transcription.
- Sensitive handwriting: minimize retention and avoid exposing unrelated personal data.

## Evidence

- https://docs.anthropic.com/en/docs/build-with-claude/vision
- https://tesseract-ocr.github.io/
