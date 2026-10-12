---
title: "Calibrated Forecast Reasoning"
category: 02-reasoning
level: intermediate
stability: experimental
description: "Produce forecasts with explicit probability ranges and calibration checks against resolved outcomes instead of single-point predictions."
added: "2026-10"
version: v1
related: [probabilistic-reasoning, uncertainty-quantification, numerical-estimation]
tags: [calibrated, forecast, reasoning, reasoning]
---
# Calibrated Forecast Reasoning

## Description
Produce forecasts with explicit probability ranges and calibration checks against resolved outcomes instead of single-point predictions. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- A task requires calibrated forecast reasoning before downstream steps can proceed safely.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for calibrated forecast reasoning. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the calibrated forecast reasoning steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
# Calibrated Forecast Reasoning: deterministic check
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
Forecast evaluation is a recurring 2026 agent-benchmark theme; calibration scoring is published as a required evaluation dimension. These are dated public signals, not adoption metrics.

## Related
- probabilistic-reasoning.md
- uncertainty-quantification.md
- numerical-estimation.md
