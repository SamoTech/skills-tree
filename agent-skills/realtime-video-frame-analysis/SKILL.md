---
name: realtime-video-frame-analysis
description: Analyze selected frames from a live video stream within latency budgets, with dropped-frame accounting and explicit staleness marking.
metadata:
  source: skills/08-multimodal/realtime-video-frame-analysis.md
  category: 08-multimodal
  version: "v1"
---

# Realtime Video Frame Analysis

## Description
Analyze selected frames from a live video stream within latency budgets, with dropped-frame accounting and explicit staleness marking. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- The task has explicit constraints such as time, budget, or safety that must gate the outcome.
- A silent failure mode exists that must be surfaced rather than swallowed.
- Verification evidence is required before the result is trusted.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for realtime video frame analysis. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Normalize the task into explicit inputs, constraints, and acceptance criteria.
2. Gather the required evidence and check completeness before proceeding.
3. Apply the realtime video frame analysis procedure using the declared criteria only.
4. Record the outcome, rejected alternatives, and the reason for each rejection.
5. Verify the result against the acceptance criteria with an independent check.
6. Report the result with evidence, and escalate explicitly when a criterion cannot be met.

## Runnable Example
```python
# Realtime Video Frame Analysis: deterministic check
def validate(record, required):
    missing = [k for k in required if k not in record]
    return (True, []) if not missing else (False, missing)

ok, missing = validate({"id": "x", "source": "y"}, ["id", "source"])
assert ok and not missing
print("validated")
```

## Failure Modes
- Proceeding with realtime video frame analysis without the required evidence or inputs.
- Treating an unverified result as verified.
- Silently swallowing errors instead of failing closed with reasons.
- Optimizing the stated metric while violating the stated constraint.
- Losing the audit trail of decisions and rejected alternatives.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Realtime multimodal agents are a 2026 trend; latency-bounded analysis is a published requirement. These are dated public signals, not adoption metrics.

## Related
- video-frame-extraction.md
- object-detection.md
- video-understanding.md
