---
title: "Audio Transcription"
category: 01-perception
level: intermediate
stability: stable
version: v3
added: "2025-03"
description: "Convert speech audio into timestamped text while preserving timing, language metadata, and source traceability for captions, search, summarization, and extraction."

related: [text-reading, video-understanding, summarization]
---

# Audio Transcription

## Description

Convert an audio file into structured transcript segments. A useful pipeline preserves timestamps and enough source metadata to trace generated text back to the recording. Transcription is extraction, not independent fact verification.

## Inputs / Outputs

| Item | Type | Required | Notes |
|---|---|---:|---|
| Audio path | str | yes | Local audio readable by the process |
| Model | str | yes | Installed Whisper model identifier |
| Language | str or None | no | Omit for model language detection |
| Output segments | list[dict] | yes | Start, end, and text per segment |
| Output language | str or None | no | Detected language when available |

## Runnable Example

```python
import json
from pathlib import Path
import whisper

def transcribe(path: str, model_name: str = "base") -> dict:
    model = whisper.load_model(model_name)
    result = model.transcribe(path, fp16=False)
    return {
        "source": str(Path(path)),
        "language": result.get("language"),
        "segments": [
            {"start": round(s["start"], 3), "end": round(s["end"], 3), "text": s["text"].strip()}
            for s in result.get("segments", [])
        ],
    }

transcript = transcribe("meeting.wav")
Path("meeting.transcript.json").write_text(json.dumps(transcript, indent=2), encoding="utf-8")
print(f"segments={len(transcript['segments'])}")
```

## Engineering Rules

- Bound maximum file size and duration before processing.
- Preserve the source identifier and transcription model in application metadata.
- For long recordings, chunk without losing absolute timestamps.
- Speaker diarization is a separate component; do not imply speaker identity from plain transcription.
- Treat transcript text as extracted data until independently verified.

## Failure Modes

| Failure | Cause | Mitigation |
|---|---|---|
| Wrong language | Automatic detection uncertainty | Supply language when known and retain detected value |
| Hallucinated text | Ambiguous or poor audio | Preserve timestamps and verify critical segments |
| Truncated recording | Operational limits | Process bounded chunks with absolute time offsets |
| Resource exhaustion | Large model or media | Select model size explicitly and enforce limits |

## Evidence

- Whisper implementation: https://github.com/openai/whisper
- Whisper transcription implementation: https://github.com/openai/whisper/blob/main/whisper/transcribe.py

Evidence status: implementation guidance is grounded in the cited primary implementation. No accuracy or benchmark claim is made.

## Related

- text-reading
- video-understanding
- summarization

## Changelog

| Version | Date | Change |
|---|---|---|
| v1 | 2025-03 | Initial entry |
| v2 | 2026-04 | Structured transcription guidance |
| v3 | 2026-10 | Added runnable batch pipeline and explicit failure boundaries |
