---
name: audio-dubbing-alignment
description: Align dubbed audio to source speech with per-utterance timing tolerance, voice-match checks, and acceptance gates so dubbing stays in sync.
metadata:
  source: skills/08-multimodal/audio-dubbing-alignment.md
  category: 08-multimodal
  version: "v1"
---

# Audio Dubbing Alignment

## Description
Align dubbed audio to source speech with per-utterance timing tolerance, voice-match checks, and acceptance gates so dubbing stays in sync. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- translated audio must be aligned to on-screen speech timing.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for audio dubbing alignment work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the audio dubbing alignment steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def align_check(segments, tolerance):
    bad = [s["i"] for s in segments if abs(s["delta"]) > tolerance]
    return bad or "accepted"

segs = [{"i": 1, "delta": 0.1}, {"i": 2, "delta": 1.5}]
assert align_check(segs, 0.4) == [2]
```

## Failure Modes
- Free-running dub audio that drifts over the runtime.
- Clipping speech to fit the tolerance.
- Accepting without listening to transitions.
- No per-language tolerance tuning.
- Ignoring lip-sync cues on visible speakers.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Dubbing workflows are a recurring 2026 localization request as generation tooling matures in public coverage; this is a dated signal, not an adoption metric.

## Related
- subtitle-generation.md
- text-to-speech.md
- audio-transcription.md
