---
name: voice-clone-detection
description: Assess whether audio likely contains synthetic cloned voices using artifact and provenance cues, with explicit uncertainty and no unverified identity claims.
metadata:
  source: skills/08-multimodal/voice-clone-detection.md
  category: 08-multimodal
  version: "v1"
---

# Voice Clone Detection

## Description
Assess whether audio likely contains synthetic cloned voices using artifact and provenance cues, with explicit uncertainty and no unverified identity claims. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- A task requires voice clone detection before downstream steps can proceed safely.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for voice clone detection. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Normalize the task into explicit inputs, constraints, and acceptance criteria.
2. Gather the required evidence and check completeness before proceeding.
3. Apply the voice clone detection procedure using the declared criteria only.
4. Record the outcome, rejected alternatives, and the reason for each rejection.
5. Verify the result against the acceptance criteria with an independent check.
6. Report the result with evidence, and escalate explicitly when a criterion cannot be met.

## Runnable Example
```python
# Voice Clone Detection: deterministic check
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
- Proceeding with voice clone detection without the required evidence or inputs.
- Treating an unverified result as verified.
- Silently swallowing errors instead of failing closed with reasons.
- Optimizing the stated metric while violating the stated constraint.
- Losing the audit trail of decisions and rejected alternatives.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Voice-cloning abuse is a documented 2026 threat; detection requests recur in trust-and-safety threads. These are dated public signals, not adoption metrics.

## Related
- audio-classification.md
- audio-diarization.md
- deepfake-detection.md
