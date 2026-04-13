---
title: "Video Description"
category: 08-multimodal
level: advanced
stability: stable
description: "Apply video description in AI agent workflows."
added: "2025-03"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-08-multimodal-video-description.json)

# Video Description

**Category:** `multimodal`  
**Skill Level:** `advanced`  
**Stability:** `stable`
**Added:** 2025-03

### Description

Generate natural language descriptions of video content by analyzing frames, motion, audio, and temporal context. Produces summaries, scene-by-scene narrations, activity recognition outputs, or structured event timelines. Used for video indexing, accessibility, content moderation, and sports/surveillance analytics.

### Example

```python
import base64, cv2
from openai import OpenAI

client = OpenAI()

def sample_frames(video_path, n=8):
    cap = cv2.VideoCapture(video_path)
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frames = []
    for i in range(n):
        cap.set(cv2.CAP_PROP_POS_FRAMES, int(i * total / n))
        ret, frame = cap.read()
        if ret:
            _, buf = cv2.imencode('.jpg', frame)
            frames.append(base64.b64encode(buf).decode())
    cap.release()
    return frames

frames = sample_frames('clip.mp4', n=8)
content = [{'type': 'text', 'text': 'Describe what happens in this video sequence, in order.'}]
for f in frames:
    content.append({'type': 'image_url', 'image_url': {'url': f'data:image/jpeg;base64,{f}'}})

response = client.chat.completions.create(model='gpt-4o', messages=[{'role': 'user', 'content': content}])
print(response.choices[0].message.content)
```

### Frameworks / Models

- GPT-4o (frame sampling + description)
- Google Gemini 1.5 Pro (native video input up to 1 hour)
- Video-LLaVA, VideoChat2 (open-source)
- AWS Rekognition Video
- Google Cloud Video Intelligence API

### Related Skills

- [Video Frame Extraction](video-frame-extraction.md)
- [Image Captioning](image-captioning.md)
- [Video Understanding](../01-perception/video-understanding.md)
