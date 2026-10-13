---
name: audio-highlight-extraction
description: Extract highlight segments from long audio using energy, speaker-turn, and semantic markers with minimum segment checks and replay verification.
metadata:
  source: skills/08-multimodal/audio-highlight-extraction.md
  category: 08-multimodal
  version: "v1"
---

# Audio Highlight Extraction

## Description
Extract highlight segments from long audio using energy, speaker-turn, and semantic markers with minimum segment checks and replay verification. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- a long recording must be reduced to short highlight segments for review.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for audio highlight extraction work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the audio highlight extraction steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def highlights(segments, min_len):
    return [s["id"] for s in segments if s["score"] >= 0.7 and s["len"] >= min_len]

segs = [{"id": 1, "score": 0.9, "len": 30}, {"id": 2, "score": 0.9, "len": 2}, {"id": 3, "score": 0.1, "len": 30}]
assert highlights(segs, 5) == [1]
```

## Failure Modes
- Highlights that cut mid-sentence.
- Volume-only scoring that picks noise bursts.
- No minimum segment length.
- Skipping replay of chosen highlights before delivery.
- No context padding so meaning is lost.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Long-audio summarization into highlights is a recurring 2026 content workflow request in public coverage; this is a dated signal, not an adoption metric.

## Related
- video-highlight-detection.md
- audio-mixing.md
- audio-transcription.md
