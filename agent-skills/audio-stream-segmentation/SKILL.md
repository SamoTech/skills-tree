---
name: audio-stream-segmentation
description: Segment continuous audio streams into bounded utterance or event chunks using voice-activity boundaries and clock alignment, flagging overlapping speakers and dropped frames instead of merging them.
metadata:
  source: skills/01-perception/audio-stream-segmentation.md
  category: 01-perception
  version: "v1"
---

# Audio Stream Segmentation

## Description
Segment continuous audio streams into bounded utterance or event chunks using voice-activity boundaries and clock alignment, flagging overlapping speakers and dropped frames instead of merging them. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A long audio stream must be split into verifiable segments before transcription or diarization.
- The outcome would change if inputs were stale, ambiguous, or incomplete.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | audio stream segmentation task context, candidate data, and explicit acceptance criteria. |
| Outputs | A structured record with the decision, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the audio stream segmentation steps in a bounded, checkpointed way.
4. Compare the actual outcome against the acceptance criteria and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Outputs
| Area | Contract |
|---|---|
| Primary | A segment list with start and end offsets, VAD evidence, and anomaly flags. |
| Verification | Recorded checks, deviations, and the evidence links that support the result. |
| Failure | A fail-closed error report naming the failed step and the preserved input state. |

## Runnable Example
```python
def segments(vad, frame_ms=20):
    out = []
    start = None
    for i, v in enumerate(vad):
        if v and start is None:
            start = i * frame_ms
        elif not v and start is not None:
            out.append((start, i * frame_ms))
            start = None
    return out
assert segments([0, 1, 1, 0, 0, 1, 0]) == [(20, 60), (100, 120)]
```

## Failure Modes
- Acting outside the declared task boundary.
- Merging two speakers whose activity overlaps into one segment.
- Ignoring dropped frames and reporting offsets that do not match the clock.
- Retrying without preserving state or evidence.
- Reporting success without checking the resulting state.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- Streaming-audio segmentation is a recurring 2026 voice-agent preprocessing request. ([public signal](https://github.com/SamoTech/skills-tree/issues/87))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [asr hallucination detection](../01-perception/asr-hallucination-detection.md)
- [audio transcription](../01-perception/audio-transcription.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
