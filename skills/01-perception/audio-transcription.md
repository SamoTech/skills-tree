---
title: "Audio Transcription"
category: 01-perception
level: intermediate
stability: stable
added: "2025-03"
description: "Convert spoken audio into timestamp-aware text while preserving speaker boundaries, language metadata, confidence signals, and recoverable transcription errors."
related: [text-reading, structured-data-reading, json-schema-validation]
version: v2
updated: "2026-09"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-01-perception-audio-transcription.json)

# Audio Transcription

## Description

Convert audio into structured, reviewable transcription data. Preserve timestamps, speaker labels when available, language metadata, and uncertainty instead of presenting low-confidence speech recognition as fact.

## When to Use

Use when an audio recording must be converted into searchable text, meeting notes, captions, evidence for downstream analysis, or a transcript that can be reviewed against the source recording.

## Inputs / Outputs

Input: an audio source plus optional language, diarization, timestamp, and segmentation settings. Output: transcript segments containing text and timing, with speaker and confidence metadata when the transcription system provides them.

## Runnable Example

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Segment:
    start: float
    end: float
    text: str


def normalize_segments(segments: list[dict]) -> list[Segment]:
    """Validate a minimal transcription segment contract."""
    result = []
    for item in segments:
        start = float(item["start"])
        end = float(item["end"])
        text = str(item["text"]).strip()
        if start < 0 or end < start or not text:
            raise ValueError("invalid transcription segment")
        result.append(Segment(start=start, end=end, text=text))
    return result

print(normalize_segments([
    {"start": 0.0, "end": 1.8, "text": "Hello"},
]))
```

## Failure Modes

- Unsupported codec or unreadable media: fail with the source and decoder error; do not emit a fabricated transcript.
- Missing or unreliable timestamps: mark timing as unavailable rather than inventing offsets.
- Low-confidence speech: preserve the uncertainty signal and route ambiguous spans for review.
- Overlapping speakers: keep speaker attribution separate from transcript text when diarization is uncertain.
- Background noise, music, or crosstalk: record the limitation when it materially affects interpretation.

## Output Contract

A valid normalized segment has a non-negative `start`, an `end` greater than or equal to `start`, and non-empty `text`. Optional speaker, language, and confidence fields must retain their source semantics and must not be synthesized as verified facts.

## Design Rules

Separate transcription from summarization. Preserve source order. Keep uncertainty attached to the smallest useful span. Never infer speaker identity from voice characteristics alone. Treat a transcript as an extraction artifact that may require source verification.

## Related Skills

- `text-reading`
- `structured-data-reading`
- `json-schema-validation`

## Changelog

- v2 (2026-09): replaced placeholder guidance with a bounded transcription contract and executable normalization example.
