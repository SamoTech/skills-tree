---
name: video-understanding
description: Analyze video over time using bounded frame or segment sampling, temporal metadata, and optional audio transcripts to identify scenes, events, captions, and grounded time ranges.
license: MIT
metadata:
  source: skills/01-perception/video-understanding.md
  version: "v2"
---

# Video Understanding

1. Inspect duration, frame rate, resolution, and audio tracks.
2. Select a bounded sampling strategy appropriate to the question.
3. Preserve timestamps for every frame, segment, transcript span, or detected event.
4. Use scene detection or adaptive sampling when uniform sampling could miss short events.
5. Combine audio transcripts with visual evidence only when both are available.
6. Report uncertainty and distinguish observed frames from inferred continuous events.

## Failure modes

- Sparse sampling misses short events: increase sampling around candidate intervals.
- Audio/video desynchronization: preserve separate clocks and validate offsets.
- Long-video resource exhaustion: process bounded segments and aggregate results hierarchically.

## Evidence

- https://docs.opencv.org/
- https://github.com/openai/whisper
- https://scenedetect.com/

Evidence status: these references support implementation guidance; no performance benchmark is claimed without reproducible benchmark data.
