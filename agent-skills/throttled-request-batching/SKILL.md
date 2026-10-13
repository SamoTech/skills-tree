---
name: throttled-request-batching
description: Batch outbound requests under provider rate limits with measured retry-after compliance, and defer or shed work explicitly instead of retrying blindly.
metadata:
  source: skills/04-action-execution/throttled-request-batching.md
  category: 04-action-execution
  version: "v1"
---

# Throttled Request Batching

## Description
Batch outbound requests under provider rate limits with measured retry-after compliance, and defer or shed work explicitly instead of retrying blindly. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- outbound request volume exceeds a known provider rate limit before downstream steps can proceed safely.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for throttled request batching work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the throttled request batching steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def take(token_bucket, now, cost=1):
    if now > token_bucket["reset_at"]:
        token_bucket["tokens"] = token_bucket["capacity"]
        token_bucket["reset_at"] = now + 60
    if token_bucket["tokens"] < cost:
        return False
    token_bucket["tokens"] -= cost
    return True

bucket = {"tokens": 2, "capacity": 2, "reset_at": 100}
assert take(bucket, 1) is True and take(bucket, 2) is True
assert take(bucket, 3) is False
```

## Failure Modes
- Retrying immediately instead of honoring retry-after.
- Bursting after a long idle and tripping sustained limits.
- Shedding work without recording what was shed.
- Assuming limits are static across endpoints.
- Mixing costs of cheap and expensive calls in one budget.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Rate-limit compliance under agent traffic is a recurring 2026 operations signal in public coverage; this is a dated signal, not an adoption metric.

## Related
- quota-management.md
- http-request.md
- batch-processing.md
