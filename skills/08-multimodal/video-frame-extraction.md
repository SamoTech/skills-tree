---
title: "Video Frame Extraction"
category: 08-multimodal
level: intermediate
stability: stable
description: "Apply video frame extraction in AI agent workflows."
added: "2025-03"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-08-multimodal-video-frame-extraction.json)

# Video Frame Extraction

**Category:** `multimodal`  
**Skill Level:** `intermediate`  
**Stability:** `stable`
**Added:** 2025-03

### Description

Extract representative frames from a video for downstream vision tasks — uniform sampling, keyframe detection, scene-change detection, or motion-triggered extraction. Produces a sequence of images with timestamps for captioning, VQA, object detection, or indexing pipelines.

### Example

```python
import cv2, os

def extract_frames(video_path, output_dir, fps=1):
    """Extract 1 frame per second."""
    os.makedirs(output_dir, exist_ok=True)
    cap = cv2.VideoCapture(video_path)
    video_fps = cap.get(cv2.CAP_PROP_FPS)
    frame_interval = int(video_fps / fps)
    count, saved = 0, 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        if count % frame_interval == 0:
            ts = count / video_fps
            path = os.path.join(output_dir, f'frame_{saved:04d}_{ts:.2f}s.jpg')
            cv2.imwrite(path, frame)
            saved += 1
        count += 1
    cap.release()
    return saved

print(f"Extracted {extract_frames('video.mp4', 'frames/', fps=1)} frames")
```

### Keyframe / Scene-Change Detection

```python
import cv2
import numpy as np

def detect_scene_changes(video_path, threshold=30):
    cap = cv2.VideoCapture(video_path)
    prev, keyframes = None, []
    idx = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if prev is not None:
            diff = np.mean(np.abs(gray.astype(float) - prev.astype(float)))
            if diff > threshold:
                keyframes.append((idx, frame))
        prev = gray
        idx += 1
    cap.release()
    return keyframes
```

### Frameworks / Models

- OpenCV (`cv2`) — universal, CPU-based
- PyAV — FFmpeg Python bindings, faster for large files
- ffmpeg-python — shell-level frame extraction
- PySceneDetect — automated scene-change detection

### Related Skills

- [Video Description](video-description.md)
- [Image Understanding](../01-perception/image-understanding.md)
- [Video Understanding](../01-perception/video-understanding.md)
