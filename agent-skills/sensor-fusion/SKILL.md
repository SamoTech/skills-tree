---
name: sensor-fusion
description: Combine multiple heterogeneous sensor readings with timestamps, uncertainty, and disagreement handling into one state estimate instead of trusting a single noisy source.
metadata:
  source: skills/01-perception/sensor-fusion.md
  category: 01-perception
  version: "v1"
---
# Sensor Fusion

## Description
Combine multiple heterogeneous sensor readings with timestamps, uncertainty, and disagreement handling into one state estimate instead of trusting a single noisy source. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- The task has explicit constraints such as time, budget, or safety that must gate the outcome.
- A silent failure mode exists that must be surfaced rather than swallowed.
- Verification evidence is required before the result is trusted.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for sensor fusion. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Normalize the task into explicit inputs, constraints, and acceptance criteria.
2. Gather the required evidence and check completeness before proceeding.
3. Apply the sensor fusion procedure using the declared criteria only.
4. Record the outcome, rejected alternatives, and the reason for each rejection.
5. Verify the result against the acceptance criteria with an independent check.
6. Report the result with evidence, and escalate explicitly when a criterion cannot be met.

## Runnable Example
```python
# Sensor Fusion: deterministic check
def validate(record, required):
    missing = [k for k in required if k not in record]
    return (True, []) if not missing else (False, missing)

ok, missing = validate({"id": "x", "source": "y"}, ["id", "source"])
assert ok and not missing
print("validated")
```

## Failure Modes
- Proceeding with sensor fusion without the required evidence or inputs.
- Treating an unverified result as verified.
- Silently swallowing errors instead of failing closed with reasons.
- Optimizing the stated metric while violating the stated constraint.
- Losing the audit trail of decisions and rejected alternatives.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Embodied-agent and robotics work in 2026 relies on multi-sensor state estimation; public agent frameworks request unified perception interfaces. These are dated public signals, not adoption metrics.

## Related
- sensor-reading.md
- depth-estimation.md
- metadata-extraction.md
