---
title: "Cron Expression Authoring"
category: 07-tool-use
level: advanced
stability: experimental
description: "Author and verify cron expressions by expanding them into concrete fire times so schedules are reviewed against actual dates."
added: "2026-10"
version: v1
related: [tool-behavior-contract-testing, offline-tool-fallback, tool-argument-construction]
tags: [scheduling, cron, automation]
---

# Cron Expression Authoring

## Description
Author and verify cron expressions by expanding them into concrete fire times so schedules are reviewed against actual dates. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- a recurring schedule must be configured and its real fire times reviewed before it goes live.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for cron expression authoring work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the cron expression authoring steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def next_hours(expr_hours, start):
    fires = []
    h = start
    while len(fires) < 3:
        if h % 24 in expr_hours:
            fires.append(h)
        h += 1
    return fires

assert next_hours({0, 12}, 10) == [12, 24, 36]
```

## Failure Modes
- Shipping an unverified cron string.
- Forgetting the timezone the scheduler runs in.
- Day-of-month and day-of-week confusion on the 31st.
- No expansion shown in review.
- No alert when the schedule silently stops firing.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Schedule verification is a recurring 2026 automation topic as agents take over cron-like work in public discussion; this is a dated signal, not an adoption metric.

## Related
- tool-behavior-contract-testing.md
- offline-tool-fallback.md
- tool-argument-construction.md
