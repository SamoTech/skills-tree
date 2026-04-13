---
title: "Audio Transcription"
category: 08-multimodal
level: intermediate
stability: stable
description: "Apply audio transcription in AI agent workflows."
added: "2025-03"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-08-multimodal-audio-transcription.json)

# Audio Transcription

**Category:** `multimodal`  
**Skill Level:** `intermediate`  
**Stability:** `stable`
**Added:** 2025-03

### Description

Convert spoken audio (MP3, WAV, M4A, WebM) into accurate text transcripts. Supports speaker diarization, timestamps, multilingual audio, and word-level confidence scores. Used in meeting summarization, voice agents, podcast indexing, and accessibility pipelines.

### Example

```python
from openai import OpenAI

client = OpenAI()
with open('meeting.mp3', 'rb') as audio:
    transcript = client.audio.transcriptions.create(
        model='whisper-1',
        file=audio,
        response_format='verbose_json',
        timestamp_granularities=['word']
    )
print(transcript.text)
for word in transcript.words:
    print(f"[{word.start:.2f}s] {word.word}")
```

### With Speaker Diarization

```python
import whisperx

model = whisperx.load_model('large-v3', device='cuda')
audio = whisperx.load_audio('meeting.wav')
result = model.transcribe(audio, batch_size=16)

# Align and diarize
align_model, metadata = whisperx.load_align_model(language_code='en', device='cuda')
result = whisperx.align(result['segments'], align_model, metadata, audio, device='cuda')
diarize_model = whisperx.DiarizationPipeline(use_auth_token='HF_TOKEN', device='cuda')
diarize_segments = diarize_model(audio)
result = whisperx.assign_word_speakers(diarize_segments, result)
for seg in result['segments']:
    print(f"[{seg['speaker']}] {seg['text']}")
```

### Frameworks / Models

- OpenAI Whisper (whisper-1 API / open-source)
- WhisperX (diarization + alignment)
- AssemblyAI, Deepgram (real-time streaming)
- Google Cloud Speech-to-Text
- AWS Transcribe

### Related Skills

- [Audio Classification](audio-classification.md)
- [Text to Speech](text-to-speech.md)
- [Audio Transcription (Perception)](../01-perception/audio-transcription.md)
