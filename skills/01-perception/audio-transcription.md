---
title: "Audio Transcription"
category: 01-perception
level: intermediate
stability: stable
added: "2025-03"
description: "Apply audio transcription in AI agent workflows."
---


![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-01-perception-audio-transcription.json)

# Audio Transcription

### Description
Converts spoken audio into structured text with word-level timestamps, speaker diarization, language identification, and confidence scoring. Handles noise, overlapping speech, domain-specific vocabulary, and long-form recordings via chunking strategies.

### When to Use
- Transcribing meetings, interviews, podcasts, call recordings, or lecture audio
- Building downstream pipelines that require timestamped captions or subtitles
- Speaker-attributed summarization or action-item extraction from multi-participant audio
- Real-time transcription via streaming WebSocket APIs

### Example
```python type:illustrative
# pip install openai-whisper torch pyannote.audio
# Note: `pyannote` is the import name for PyPI package `pyannote.audio`
import whisper, torch
from pyannote.audio import Pipeline

def transcribe_with_diarization(audio_path: str) -> list[dict]:
    # Step 1: transcribe with word timestamps
    model = whisper.load_model("large-v3", device="cuda" if torch.cuda.is_available() else "cpu")
    result = model.transcribe(audio_path, word_timestamps=True, language=None)  # auto-detect lang

    # Step 2: diarize
    diar = Pipeline.from_pretrained("pyannote/speaker-diarization-3.1")
    diar_result = diar(audio_path)

    # Step 3: merge word timestamps with speaker turns
    segments = []
    for turn, _, speaker in diar_result.itertracks(yield_label=True):
        words = [
            w for seg in result["segments"]
            for w in seg.get("words", [])
            if turn.start <= w["start"] < turn.end
        ]
        if words:
            segments.append({"speaker": speaker, "start": turn.start,
                              "end": turn.end, "text": " ".join(w["word"] for w in words)})
    return segments
```

### Advanced Techniques
- **Long audio chunking**: split at silence boundaries (`pydub.silence.split_on_silence`) before feeding to Whisper to avoid context window truncation
- **Custom vocabulary**: inject domain terms via `initial_prompt` parameter in Whisper or use PromptingWhisper
- **Streaming**: use `faster-whisper` with `stream=True` for low-latency real-time pipelines
- **Post-correction**: run a language model pass to fix homophones and domain-specific names

### Related Skills
- `video-understanding`, `summarization`, `text-reading`, `image-understanding`
