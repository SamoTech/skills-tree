---
name: audio-transcription
description: Transcribe speech into text with timestamps and optional speaker attribution. Use for meetings, interviews, captions, recordings, and other speech-to-text workflows.
license: MIT
metadata:
  source: skills/01-perception/audio-transcription.md
  version: "v2"
---

# Audio Transcription

1. Establish the audio format, language expectations, and required output granularity.
2. Transcribe with a documented speech-recognition implementation.
3. Enable word timestamps only when downstream processing needs them.
4. Add diarization as a separate stage when speaker attribution is required.
5. For long recordings, process bounded segments and preserve offsets.
6. Mark low-confidence or ambiguous spans rather than inventing words or speakers.

## Failure modes

- Repetition or timestamp instability: adjust decoding/windowing and inspect the affected segment.
- Speaker overlap: do not assign a speaker with unsupported certainty.
- Domain terminology errors: use documented vocabulary prompting or post-processing and verify critical terms.

## Evidence

- https://github.com/openai/whisper
- https://github.com/openai/whisper/blob/main/whisper/transcribe.py
- https://github.com/pyannote/pyannote-audio

Evidence status: these references support implementation guidance; no performance benchmark is claimed without reproducible benchmark data.
