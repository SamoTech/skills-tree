---
name: action-concurrency-limiting
description: Bound how many actions of each type run simultaneously using explicit limits and queuing, so parallelism does not exhaust quotas, rate limits, or downstream capacity.
metadata:
  source: skills/04-action-execution/action-concurrency-limiting.md
  category: 04-action-execution
  version: "v1"
---
# Action Concurrency Limiting

## Description
Bound how many actions of each type run simultaneously using explicit limits and queuing, so parallelism does not exhaust quotas, rate limits, or downstream capacity. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- The task has explicit constraints such as time, budget, or safety that must gate the outcome.
- A silent failure mode exists that must be surfaced rather than swallowed.
- Verification evidence is required before the result is trusted.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for action concurrency limiting. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the action concurrency limiting steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
# Action Concurrency Limiting: deterministic check
attempts = []
def flaky(n):
    attempts.append(n)
    return n >= 3

tries, max_tries, done = 0, 5, False
while tries < max_tries:
    tries += 1
    if flaky(tries):
        done = True
        break
assert done and tries == 3
print("succeeded after", tries, "attempts")
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
Safety under concurrent load is a named 2026 production concern for agent teams; published guidance recommends explicit concurrency budgets. These are dated public signals, not adoption metrics.

## Related
- batch-processing.md
- process-management.md
- rate-limiting.md
