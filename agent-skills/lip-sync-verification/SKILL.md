---
name: lip-sync-verification
description: Verify generated speech is aligned to mouth movement by comparing onset timings within a tolerance window.
metadata:
  source: skills/08-multimodal/lip-sync-verification.md
  category: 08-multimodal
  version: "v1"
---
# Lip Sync Verification

## Description
Verify generated speech is aligned to mouth movement by comparing onset timings within a tolerance window. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- A task requires lip sync verification before downstream steps can proceed safely.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for lip sync verification. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the lip sync verification steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def aligned(viseme_ms, phoneme_ms, tol_ms):
    return abs(viseme_ms - phoneme_ms) <= tol_ms
assert aligned(100, 110, 20) is True
assert aligned(100, 200, 20) is False
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
Dubbed and generated video workflows in 2026 request objective lip-sync checks before publication. These are dated public signals, not adoption metrics.

## Related
- audio-dubbing-alignment.md
- video-object-tracking.md
- audio-transcription.md
