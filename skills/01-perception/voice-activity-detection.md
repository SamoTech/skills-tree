---
title: "Voice Activity Detection"
category: 01-perception
level: advanced
stability: experimental
description: "Decide when speech starts and ends in an audio stream using energy and spectral cues with hysteresis, so downstream actions fire on verified speech segments rather than background noise."
added: "2026-10"
version: v1
related: [audio-transcription, iot-telemetry-parsing, time-series-reading]
tags: [voice, activity, detection, perception]
---

# Voice Activity Detection

## Description
Decide when speech starts and ends in an audio stream using energy and spectral cues with hysteresis, so downstream actions fire on verified speech segments rather than background noise. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- Multiple inputs or candidates compete and must be resolved by explicit criteria.
- A wrong intermediate result would propagate into consequential actions.
- The task repeats and benefits from a deterministic procedure.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for voice activity detection. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the voice activity detection steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
# Voice Activity Detection: deterministic check
def check_budget(estimate, limit):
    if estimate > limit:
        raise ValueError("estimate %s exceeds limit %s" % (estimate, limit))
    return "approved"

assert check_budget(3, 5) == "approved"
try:
    check_budget(7, 5)
    raise AssertionError("should have raised")
except ValueError:
    print("guard held")
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
2026 voice-agent architectures publish VAD gating as a required front-end stage; open-source VAD models are widely requested in agent speech pipelines. These are dated public signals, not adoption metrics.

## Related
- audio-transcription.md
- iot-telemetry-parsing.md
- time-series-reading.md
