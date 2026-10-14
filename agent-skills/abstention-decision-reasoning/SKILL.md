---
name: abstention-decision-reasoning
description: Decide when to abstain rather than answer by scoring evidence sufficiency, coverage, and confidence against explicit thresholds.
metadata:
  source: skills/02-reasoning/abstention-decision-reasoning.md
  category: 02-reasoning
  version: "v1"
---
# Abstention Decision Reasoning

## Description
Decide when to abstain rather than answer by scoring evidence sufficiency, coverage, and confidence against explicit thresholds. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- A task requires abstention decision reasoning before downstream steps can proceed safely.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for abstention decision reasoning. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the abstention decision reasoning steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def should_abstain(evidence, threshold):
    return evidence < threshold
assert should_abstain(0.2, 0.5) is True
assert should_abstention := (should_abstain(0.9, 0.5) is False)
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
Production agent guides in 2026 recommend calibrated abstention over forced answers under uncertainty. These are dated public signals, not adoption metrics.

## Related
- uncertainty-quantification.md
- self-correction.md
- calibrated-forecast-reasoning.md
