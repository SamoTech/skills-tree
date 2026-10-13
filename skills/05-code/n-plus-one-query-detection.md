---
title: "N Plus One Query Detection"
category: 05-code
level: advanced
stability: experimental
description: "Detect query loops that issue one request per item, and rewrite them into batched access with a measured request-count check."
added: "2026-10"
version: v1
related: [performance-profiling, sql-query-generation, observability-instrumentation]
tags: [performance, queries, detection]
---

# N Plus One Query Detection

## Description
Detect query loops that issue one request per item, and rewrite them into batched access with a measured request-count check. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- a page or endpoint is slow and the cause may be one query per item in a loop.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for n plus one query detection work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the n plus one query detection steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def detect(requests, items):
    fetches = [r for r in requests if r["kind"] == "fetch"]
    return len(fetches) > len(items) * 2

reqs = [{"kind": "fetch"} for _ in range(40)] + [{"kind": "render"}]
assert detect(reqs, 10) is True
assert detect(reqs[:5], 10) is False
```

## Failure Modes
- Counting queries only on the happy path.
- Batching without checking the result order.
- Assuming the loop is the cause without a counter.
- Fixing one loop while five clones remain.
- No regression counter that fails CI next time.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
N-plus-one access patterns remain a top performance finding in 2026 API reviews in public coverage; this is a dated signal, not an adoption metric.

## Related
- performance-profiling.md
- sql-query-generation.md
- observability-instrumentation.md
