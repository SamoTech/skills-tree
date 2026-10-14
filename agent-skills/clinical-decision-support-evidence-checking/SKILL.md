---
name: clinical-decision-support-evidence-checking
description: Check clinical recommendations against cited guideline evidence, grading the strength and recency of each citation.
metadata:
  source: skills/16-domain-specific/clinical-decision-support-evidence-checking.md
  category: 16-domain-specific
  version: "v1"
---
# Clinical Decision Support Evidence Checking

## Description
Check clinical recommendations against cited guideline evidence, grading the strength and recency of each citation. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- A task requires clinical decision support evidence checking before downstream steps can proceed safely.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for clinical decision support evidence checking. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the clinical decision support evidence checking steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def strong_enough(grade, min_grade):
    order = {"C": 1, "B": 2, "A": 3}
    return order[grade] >= order[min_grade]
assert strong_enough("B", "B") is True
assert strong_enough("C", "B") is False
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
Clinical decision-support requests require verifiable guideline citations before recommendations are shown. These are dated public signals, not adoption metrics.

## Related
- medical-literature-search.md
- clinical-trial-protocol-review.md
- drug-interaction.md
