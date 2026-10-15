---
name: batch-inference-job-orchestration
description: Orchestrate large offline inference jobs with chunking, checkpointing, idempotent resumes, and result manifests.
metadata:
  source: skills/17-infrastructure/batch-inference-job-orchestration.md
  category: 17-infrastructure
  version: "v1"
---

# Batch Inference Job Orchestration

## Description
Orchestrate large offline inference jobs with chunking, checkpointing, idempotent resumes, and result manifests. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- A task requires batch inference job orchestration before downstream steps can proceed safely.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for batch inference job orchestration. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the batch inference job orchestration steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def manifest(chunks_done, total):
    return {"done": chunks_done, "total": total, "complete": chunks_done == total}
m = manifest(10, 10)
assert m["complete"] is True
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
Batch inference over large corpora is a recurring 2026 platform request for cost efficiency. These are dated public signals, not adoption metrics.

## Related
- background-job-submission.md
- batch-processing.md
- inference-endpoint-autoscaling.md
