---
title: "Voice Command Audio Segmentation"
category: 08-multimodal
level: advanced
stability: experimental
description: "Segment a voice-command audio stream into command boundaries so each spoken command is parsed as one utterance."
added: "2026-10"
version: v1
related: [audio-stream-segmentation, voice-activity-detection]
tags: [voice, audio, segmentation, commands]
---
# Voice Command Audio Segmentation

## Description
Segment a voice-command audio stream into command boundaries so each spoken command is parsed as one utterance. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A voice-driven agent receives a continuous audio stream and must split it into commands before intent parsing.
- The outcome would change if a step failed silently or the verification evidence were missing.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | the declared input set, policy thresholds, and explicit acceptance criteria. |
| Outputs | A structured record with the decision, rejected alternatives, and the verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Detect command boundaries from the silence and wake-word markers in the stream, and reject segments that carry no wake word or that overlap the previous segment.
4. Compare the actual outcome against the acceptance criteria and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Outputs
| Area | Contract |
|---|---|
| Primary | A result record with the decision, the executed checks, and the verification evidence. |
| Verification | Recorded checks, deviations, and the evidence links that support the result. |
| Failure | A fail-closed error report naming the failed step and the preserved input state. |

## Runnable Example
```python
def segment(stream, silence_ms, min_len):
    segments, start = [], 0
    for i, frame in enumerate(stream):
        if frame == "silence" and i - start >= min_len:
            segments.append((start, i))
            start = i + 1
    if len(stream) - start >= min_len:
        segments.append((start, len(stream)))
    return segments

stream = ["wake", "speech", "silence", "wake", "speech", "speech", "silence"]
segs = segment(stream, "silence", 2)
assert len(segs) == 2 and segs[0] == (0, 2) and segs[1] == (3, 6)
```

## Failure Modes
- Silence thresholds are tuned so trailing speech is cut into a partial command.
- Segments without a wake word are parsed as commands anyway.
- Overlapping segments are emitted and one utterance is parsed twice.
- Wake-word partials are treated as full command boundaries.
- Segmentation runs before noise suppression so coughs split commands.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- The OpenAI Codex CLI 0.163 release adds voice control to a coding agent, making command-boundary segmentation a live multimodal input need (trendintech.com, dated October 2026) ([public signal](https://trendintech.com/openai-codex-cli-0-163-voice-control-2026/))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Audio Stream Segmentation](../08-multimodal/audio-stream-segmentation.md)
- [Voice Activity Detection](../01-perception/voice-activity-detection.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
