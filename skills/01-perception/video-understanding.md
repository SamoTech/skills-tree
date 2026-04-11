# Video Understanding

**Category:** `perception`  
**Skill Level:** `advanced`  
**Stability:** `experimental`

### Description

Analyze and describe video content — identifying scenes, objects, events, and temporal patterns.

### Example

```python
# Gemini 2.5 Pro supports direct video input
import google.generativeai as genai
video_file = genai.upload_file('video.mp4')
model = genai.GenerativeModel('gemini-2.5-pro')
response = model.generate_content(['Describe what happens in this video.', video_file])
```

### Frameworks / Models

- Gemini 2.5 Pro (native video)
- GPT-4o (frame-by-frame)
- LLaVA-Video

### Related Skills

- [Audio Transcription](audio-transcription.md)
- [Image Understanding](image-understanding.md)
