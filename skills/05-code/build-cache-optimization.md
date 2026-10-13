---
title: "Build Cache Optimization"
category: 05-code
level: advanced
stability: experimental
description: "Reduce continuous integration time by restoring, keying, and pruning build caches correctly across runs."
added: "2026-10"
version: v1
related: [ci-failure-triage, cicd-generation, performance-profiling]
tags: [ci, caching, builds]
---

# Build Cache Optimization

## Description
Reduce continuous integration time by restoring, keying, and pruning build caches correctly across runs. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- build times grow because caches are missed or bloated and the cache policy must be fixed deliberately.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for build cache optimization work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the build cache optimization steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def cache_key(lock, job):
    digest = sum(ord(c) for c in lock + job) % (10 ** 8)
    return f"{job}-{digest:08d}"

def should_restore(entries, key, limit):
    if key in entries and entries[key]["size"] <= limit:
        return True
    return False

entries = {cache_key("l", "test"): {"size": 400}}
assert should_restore(entries, cache_key("l", "test"), 500) is True
assert should_restore(entries, cache_key("l", "test"), 100) is False
```

## Failure Modes
- Keying caches on the branch name so main never hits.
- Restoring caches that exceed the storage budget.
- Caching outputs that depend on wall-clock time.
- Never pruning stale entries until eviction is forced.
- Measuring save time but not restore hit rate.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
CI cost and duration reduction is a recurring 2026 engineering request as agent pipelines multiply; this is a dated signal, not an adoption metric.

## Related
- ci-failure-triage.md
- cicd-generation.md
- performance-profiling.md
