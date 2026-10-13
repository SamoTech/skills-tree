---
title: "Audio Event Detection"
category: 08-multimodal
level: advanced
stability: experimental
description: "Detect discrete audio events with onset windows, confidence thresholds, and per-event timestamps so long recordings yield structured event lists."
added: "2026-10"
version: v1
related: [audio-classification, audio-transcription, audio-diarization]
tags: [audio, events, detection]
---

# Audio Event Detection

## Description
Detect discrete audio events with onset windows, confidence thresholds, and per-event timestamps so long recordings yield structured event lists. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- a long recording must be reduced to a list of discrete events with timestamps.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for audio event detection work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the audio event detection steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def events(windows, threshold):
    out = []
    for w in windows:
        if w["score"] >= threshold:
            out.append({"t": w["t"], "kind": w["kind"]})
    return out

ws = [{"t": 1.2, "kind": "door", "score": 0.9}, {"t": 3.0, "kind": "speech", "score": 0.3}]
assert events(ws, 0.5) == [{"t": 1.2, "kind": "door"}]
```

## Failure Modes
- Merging overlapping events into one.
- No threshold so noise becomes events.
- Reporting event kinds the model was never validated on.
- Missing timestamps so events cannot be audited.
- Ignoring channel information on stereo input.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Audio event detection is a recurring 2026 multimodal request as agents gain meeting and monitoring duties in public coverage; this is a dated signal, not an adoption metric.

## Related
- audio-classification.md
- audio-transcription.md
- audio-diarization.md
