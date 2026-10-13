---
name: wake-word-detection
description: Detect a configured wake phrase in an audio stream, gate downstream transcription on the detection, and record confidence rather than treating every match as intentional.
metadata:
  source: skills/01-perception/wake-word-detection.md
  category: 01-perception
  version: "v1"
---

# Wake Word Detection

## Description
Detect a configured wake phrase in an audio stream, gate downstream transcription on the detection, and record confidence rather than treating every match as intentional. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- a voice agent must start listening only after the wake phrase is reliably detected before downstream steps can proceed safely.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for wake word detection work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the wake word detection steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def should_wake(scores, phrase, threshold=0.8):
    score = scores.get(phrase, 0.0)
    if score < threshold:
        return False
    return True

assert should_wake({"hey agent": 0.93}, "hey agent") is True
assert should_wake({"hey agent": 0.42}, "hey agent") is False
```

## Failure Modes
- Triggering on a low-confidence partial match.
- Ignoring false-positive rate when setting the threshold.
- Waking on the phrase embedded in background speech.
- Using a speaker-dependent model without enrollment checks.
- Treating detection as authorization to act.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Voice-first agent products and device assistants remain a recurring 2026 capability request in public agent ecosystems; this is a dated signal, not an adoption metric.

## Related
- voice-activity-detection.md
- audio-transcription.md
- speech-noise-suppression.md
