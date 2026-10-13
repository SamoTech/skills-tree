---
title: "Crash Loop Detection"
category: 05-code
level: advanced
stability: experimental
description: "Detect repeated crash signatures across process restarts and stop the loop by flagging instead of restarting forever."
added: "2026-10"
version: v1
related: [stack-trace-analysis, error-handling-design, debugging]
tags: [reliability, crashes, operations]
---

# Crash Loop Detection

## Description
Detect repeated crash signatures across process restarts and stop the loop by flagging instead of restarting forever. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- a service or agent restarts repeatedly and the loop must be stopped before it hides the failure.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for crash loop detection work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the crash loop detection steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def classify(restarts, window, max_restarts):
    if len(restarts) < max_restarts:
        return "healthy"
    signatures = {r["sig"] for r in restarts[-window:]}
    if len(signatures) == 1:
        return "crash-loop"
    return "unstable"

rs = [{"sig": "X"} for _ in range(5)]
assert classify(rs, 5, 3) == "crash-loop"
assert classify(rs[:2], 5, 3) == "healthy"
```

## Failure Modes
- Restarting without a cap and a backoff.
- Treating each crash as independent without signatures.
- Resetting the counter on any successful start.
- Alerting on the restart, never on the root cause.
- Silently absorbing the crash loop in monitoring.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Crash-loop handling for agent runtimes is a recurring 2026 reliability topic in public coverage; this is a dated signal, not an adoption metric.

## Related
- stack-trace-analysis.md
- error-handling-design.md
- debugging.md
