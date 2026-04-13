---
title: "Audio Classification"
category: 08-multimodal
level: advanced
stability: stable
description: "Apply audio classification in AI agent workflows."
added: "2025-03"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-08-multimodal-audio-classification.json)

# Audio Classification

**Category:** `multimodal`  
**Skill Level:** `advanced`  
**Stability:** `stable`
**Added:** 2025-03

### Description

Assign category labels to audio clips — environmental sounds, music genres, speech events, anomaly detection, or speaker emotion. Uses spectrogram-based neural networks or audio foundation models to classify raw waveforms or extracted features.

### Example

```python
from transformers import pipeline

classifier = pipeline('audio-classification', model='MIT/ast-finetuned-audioset-10-10-0.4593')
results = classifier('alarm.wav')
for r in results[:3]:
    print(f"{r['label']}: {r['score']:.2%}")
# Fire alarm: 94.3%
# Smoke detector: 88.1%
# Alarm clock: 12.7%
```

### Music Genre Classification

```python
from transformers import pipeline

genre_classifier = pipeline('audio-classification', model='mtg-upf/discogs-maest-30s-pw-129e')
result = genre_classifier('track.mp3')
print(result[0])  # {'label': 'Electronic---Techno', 'score': 0.87}
```

### Frameworks / Models

- Audio Spectrogram Transformer (AST) — environmental sounds
- Wav2Vec2, HuBERT — speech classification
- CLAP — zero-shot audio classification
- Google AudioSet pretrained models
- AssemblyAI Audio Intelligence API

### Related Skills

- [Audio Transcription](audio-transcription.md)
- [Text to Speech](text-to-speech.md)
