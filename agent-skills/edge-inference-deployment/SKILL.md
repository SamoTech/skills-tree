---
name: edge-inference-deployment
description: Deploy models at the edge with hardware-aware quantization, model version pinning, and local rollback.
metadata:
  source: skills/17-infrastructure/edge-inference-deployment.md
  category: 17-infrastructure
  version: "v1"
---
# Edge Inference Deployment

## Description
Deploy models at the edge with hardware-aware quantization, model version pinning, and local rollback. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- A task requires edge inference deployment before downstream steps can proceed safely.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for edge inference deployment. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the edge inference deployment steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def pinned(requested, deployed):
    return requested == deployed
assert pinned("v1.0.0", "v1.0.0") is True
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
Edge inference deployment is requested for latency and privacy constrained agent use cases in 2026. These are dated public signals, not adoption metrics.

## Related
- inference-endpoint-autoscaling.md
- container-image-slimming.md
- deployment-rollback.md
