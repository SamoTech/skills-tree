---
name: multispectral-image-reading
description: Read multispectral imagery band stacks into aligned arrays with band metadata and per-band statistics for analysis.
metadata:
  source: skills/01-perception/multispectral-image-reading.md
  category: 01-perception
  version: "v1"
---

# Multispectral Image Reading

## Description
Read multispectral imagery band stacks into aligned arrays with band metadata and per-band statistics for analysis. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- A task requires multispectral image reading before downstream steps can proceed safely.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for multispectral image reading. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the multispectral image reading steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def band_count(stack):
    return len(stack)
assert band_count([[], [], []]) == 3
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
Earth-observation and agronomy agent requests increasingly require multispectral band handling beyond RGB. These are dated public signals, not adoption metrics.

## Related
- image-understanding.md
- image-classification.md
- sensor-reading.md
