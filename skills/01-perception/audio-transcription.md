---
title: "Audio Transcription"
category: 01-perception
level: intermediate
stability: stable
added: "2025-03"
description: "Convert spoken audio into timestamp-aware text while preserving speaker boundaries, language metadata, confidence signals, and recoverable transcription errors."
dependencies:
  - package: openai-whisper
    min_version: "20231117"
    tested_version: "20231117"
    confidence: verified
  - package: torch
    min_version: "2.1.0"
    tested_version: "2.3.0"
    confidence: verified
code_blocks:
  - id: "example-diarization"
    type: illustrative
    note: "pyannote.audio requires HuggingFace token and model download — illustrative only"
version: v2
updated: "2026-09"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-01-perception-audio-transcription.json)

# Audio Transcription

## Description

Convert spoken audio into timestamp-aware text while preserving speaker boundaries, language metadata, confidence signals, and recoverable transcription errors.

## When to Use

Use for voice notes, meetings, calls, interviews, or media pipelines where audio must become searchable or actionable text.

## Inputs / Outputs

| Field | Type | Description |
|---|---|---|
| input | structured | Source content plus any format-specific metadata. |
| options | object | Limits, locale, schema, or provider-specific parsing options. |
| output | structured | Normalized records with provenance and explicit uncertainty. |

## Runnable Example

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Segment:
    start: float
    end: float
    text: str
    speaker: str | None = None

def normalize_segments(raw: list[dict]) -> list[Segment]:
    result = []
    for item in raw:
        start = float(item["start"])
        end = float(item["end"])
        text = str(item["text"]).strip()
        if end < start:
            raise ValueError("segment end precedes start")
        if text:
            result.append(Segment(start, end, text, item.get("speaker")))
    return result

segments = normalize_segments([
    {"start": 0.0, "end": 2.4, "text": "Hello", "speaker": "A"},
    {"start": 2.5, "end": 4.0, "text": "Welcome", "speaker": "B"},
])
print(segments)
```

## Failure Modes

| Failure | Cause | Mitigation |
|---|---|---|
| Noisy audio | malformed or adversarial input | Validate structure before semantic processing. |
| overlapping speakers | unexpected source variation | Preserve raw context and emit a warning. |
| wrong language detection | incomplete source | Mark uncertainty instead of inventing values. |
| Resource exhaustion | unbounded input | Enforce size, time, and result limits. |

## Output Contract

Ordered transcription segments with timestamps and optional speaker labels; retain provider confidence separately.

## Design Rules

1. Preserve source provenance and ordering whenever it is available.
2. Validate structure before interpreting semantics.
3. Never silently convert uncertainty into a confident assertion.
4. Bound input size, execution time, and result cardinality.
5. Keep provider-specific parsing behind a stable internal representation.

## Related Skills

- [Text Reading](text-reading.md) — plain text extraction and normalization
- [Structured Data Reading](structured-data-reading.md) — schema-aware data ingestion
- [JSON Schema Validation](json-schema-validation.md) — validate normalized structures

## Changelog

| Version | Date | Change |
|---|---|---|
| v1 | 2025-03 | Initial skill entry |
| v2 | 2026-09 | Replaced placeholder guidance with executable implementation, I/O contract, failure modes, and bounded parsing rules |
