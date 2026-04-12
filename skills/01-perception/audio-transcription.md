# Audio Transcription

**Category:** `perception`  
**Skill Level:** `intermediate`  
**Stability:** `stable`
**Added:** 2025-03

### Description

Convert spoken audio into text using automatic speech recognition (ASR) models.

### Example

```python
from openai import OpenAI
client = OpenAI()
with open('audio.mp3', 'rb') as f:
    result = client.audio.transcriptions.create(model='whisper-1', file=f)
print(result.text)
```

### Frameworks / Models

- OpenAI Whisper (local + API)
- Google Speech-to-Text
- AWS Transcribe
- AssemblyAI

### Related Skills

- [Text to Speech](../08-multimodal/text-to-speech.md)
- [Video Understanding](video-understanding.md)
