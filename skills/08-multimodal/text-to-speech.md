# Text to Speech

**Category:** `multimodal`  
**Skill Level:** `intermediate`  
**Stability:** `stable`
**Added:** 2025-03

### Description

Convert a text string into natural-sounding spoken audio.

### Example

```python
from openai import OpenAI
client = OpenAI()
response = client.audio.speech.create(
    model='tts-1-hd',
    voice='nova',
    input='Welcome to Skills Tree. Your complete AI skills catalog.'
)
response.stream_to_file('welcome.mp3')
```

### Frameworks / Models

- OpenAI TTS (tts-1, tts-1-hd)
- ElevenLabs
- Google Cloud TTS
- Microsoft Azure TTS

### Related Skills

- [Audio Transcription](../01-perception/audio-transcription.md)
