---
title: "Asr Hallucination Detection"
category: 01-perception
level: advanced
stability: experimental
description: "Detect hallucinated transcription segments in ASR output by flagging text produced over non-speech audio, repeated loop patterns, and empty-audio text before downstream use."
added: "2026-10"
version: v1
related: [streaming-asr-partial-parsing, audio-transcription, voice-activity-detection]
tags: [asr, hallucination, detection]
---
# Asr Hallucination Detection

## Description
Detect hallucinated transcription segments in ASR output by flagging text produced over non-speech audio, repeated loop patterns, and empty-audio text before downstream use. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- A task requires asr hallucination detection before downstream steps can proceed safely.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for asr hallucination detection. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the asr hallucination detection steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def is_hallucination(segment, voiced):
    return bool(segment["text"]) and not voiced
assert is_hallucination({"text": "thank you."}, False) is True
assert is_hallucination({"text": "hello"}, True) is False
```

## Failure Modes
- Acting outside the declared task boundary.
- Assuming an estimate or preview equals the verified effect.
- Retrying without preserving state or evidence.
- Using stale inputs as if they were current.
- Reporting success without checking the resulting state.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Streaming-ASR deployments in 2026 agent tooling repeatedly report hallucinated text on silence as an operational defect. These are dated public signals, not adoption metrics.

## Related
- streaming-asr-partial-parsing.md
- audio-transcription.md
- voice-activity-detection.md
