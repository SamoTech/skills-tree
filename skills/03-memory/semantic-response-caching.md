---
title: "Semantic Response Caching"
category: 03-memory
level: intermediate
stability: experimental
description: "Cache expensive responses keyed by semantic equivalence of requests, with TTL, invalidation, and a bypass for side-effecting requests, so identical work is not repeated."
added: "2026-10"
version: v1
related: [cache-management, memory-ttl, prompt-caching]
tags: [semantic, response, caching, memory]
---

# Semantic Response Caching

## Description
Cache expensive responses keyed by semantic equivalence of requests, with TTL, invalidation, and a bypass for side-effecting requests, so identical work is not repeated. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- A task requires semantic response caching before downstream steps can proceed safely.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for semantic response caching. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the semantic response caching steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
# Semantic Response Caching: deterministic check
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
LLM cost control is a dominant 2026 concern after public runaway-bill incidents; response caching is a standard published mitigation. These are dated public signals, not adoption metrics.

## Related
- cache-management.md
- memory-ttl.md
- prompt-caching.md
