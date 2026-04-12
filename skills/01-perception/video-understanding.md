---
Category: Perception
Skill Level: Advanced
Stability: Stable
Tags: [video, multimodal, temporal-reasoning, scene-detection, captioning]
---

# Video Understanding

### Description
Extracts temporal semantics from video: scene segmentation, activity recognition, caption generation, highlight detection, and event grounding. Handles long-form video via frame sampling strategies, keyframe extraction, and hierarchical summarization.

### When to Use
- Summarizing lecture videos, sports highlights, surveillance footage, or product demos
- Detecting specific events (e.g., goal in a match, error dialog on screen) across a timeline
- Building video-to-text pipelines for downstream search or RAG applications
- Grounding natural-language queries to temporal segments (video QA)

### Example
```python
import cv2, base64
from openai import OpenAI

def sample_frames(video_path: str, n: int = 16) -> list[str]:
    cap = cv2.VideoCapture(video_path)
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    indices = [int(i * total / n) for i in range(n)]
    frames_b64 = []
    for idx in indices:
        cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
        ok, frame = cap.read()
        if ok:
            _, buf = cv2.imencode(".jpg", frame)
            frames_b64.append(base64.b64encode(buf).decode())
    cap.release()
    return frames_b64

def summarize_video(video_path: str, question: str = "Describe what happens in this video.") -> str:
    client = OpenAI()
    frames = sample_frames(video_path, n=24)
    content = [{"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{f}"}} for f in frames]
    content.append({"type": "text", "text": question})
    r = client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": content}])
    return r.choices[0].message.content
```

### Advanced Techniques
- **Scene detection**: use `scenedetect` (PySceneDetect) to split at cut boundaries before sampling
- **Audio-visual fusion**: combine Whisper transcript timestamps with frame captions for richer event grounding
- **Long-video hierarchical summarization**: summarize chunks independently, then summarize summaries
- **Gemini 1.5 Pro**: supports native video input up to 1 hour — pass video bytes directly via File API

### Related Skills
- `audio-transcription`, `image-understanding`, `screen-reading`, `summarization`
