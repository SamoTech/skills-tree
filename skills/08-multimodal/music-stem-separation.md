---
title: "Music Stem Separation"
category: 08-multimodal
level: basic
stability: experimental
description: "Separate a music track into stems for vocals, drums, bass, and other instruments with quality checks and artifact detection, preserving source attribution."
added: "2026-10"
version: v1
related: [audio-mixing, audio-diarization, audio-transcription]
tags: [music, stem, separation, multimodal]
---

# Music Stem Separation

## Description
Separate a music track into stems for vocals, drums, bass, and other instruments with quality checks and artifact detection, preserving source attribution. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- The task has explicit constraints such as time, budget, or safety that must gate the outcome.
- A silent failure mode exists that must be surfaced rather than swallowed.
- Verification evidence is required before the result is trusted.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for music stem separation. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the music stem separation steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
# Music Stem Separation: deterministic check
candidates = [{"id": "a", "score": 0.8, "cost": 2}, {"id": "b", "score": 0.95, "cost": 9}]
eligible = [c for c in candidates if c["score"] >= 0.8]
selected = min(eligible, key=lambda c: c["cost"])
assert selected["id"] == "a"
print("selected:", selected["id"])
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
Stem separation appears in 2026 creator tooling requests; provenance and quality checks are named concerns. These are dated public signals, not adoption metrics.

## Related
- audio-mixing.md
- audio-diarization.md
- audio-transcription.md
