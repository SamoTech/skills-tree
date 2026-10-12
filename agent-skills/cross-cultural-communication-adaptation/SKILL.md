---
name: cross-cultural-communication-adaptation
description: Adapt message content across cultural norms of directness, formality, and context expectations, without changing the underlying facts or commitments.
metadata:
  source: skills/06-communication/cross-cultural-communication-adaptation.md
  category: 06-communication
  version: "v1"
---

# Cross-Cultural Communication Adaptation

## Description
Adapt message content across cultural norms of directness, formality, and context expectations, without changing the underlying facts or commitments. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- Multiple inputs or candidates compete and must be resolved by explicit criteria.
- A wrong intermediate result would propagate into consequential actions.
- The task repeats and benefits from a deterministic procedure.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for cross-cultural communication adaptation. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Normalize the task into explicit inputs, constraints, and acceptance criteria.
2. Gather the required evidence and check completeness before proceeding.
3. Apply the cross-cultural communication adaptation procedure using the declared criteria only.
4. Record the outcome, rejected alternatives, and the reason for each rejection.
5. Verify the result against the acceptance criteria with an independent check.
6. Report the result with evidence, and escalate explicitly when a criterion cannot be met.

## Runnable Example
```python
# Cross-Cultural Communication Adaptation: deterministic check
def validate(record, required):
    missing = [k for k in required if k not in record]
    return (True, []) if not missing else (False, missing)

ok, missing = validate({"id": "x", "source": "y"}, ["id", "source"])
assert ok and not missing
print("validated")
```

## Failure Modes
- Proceeding with cross-cultural communication adaptation without the required evidence or inputs.
- Treating an unverified result as verified.
- Silently swallowing errors instead of failing closed with reasons.
- Optimizing the stated metric while violating the stated constraint.
- Losing the audit trail of decisions and rejected alternatives.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Global agent deployment in 2026 requires cross-cultural communication adaptation; localization threads request norm-aware phrasing. These are dated public signals, not adoption metrics.

## Related
- multilingual-output.md
- audience-analysis.md
- translation.md
