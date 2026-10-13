---
title: "Free Busy Availability Querying"
category: 07-tool-use
level: advanced
stability: experimental
description: "Query free-busy information with least-privilege scopes, minimal time windows, and aggregate-only reporting so individual calendars stay private."
added: "2026-10"
version: v1
related: [google-workspace-api, tool-argument-construction, api-pagination]
tags: [calendar, scheduling, privacy]
---

# Free Busy Availability Querying

## Description
Query free-busy information with least-privilege scopes, minimal time windows, and aggregate-only reporting so individual calendars stay private. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- a meeting must be scheduled and only aggregate availability is needed, not calendar contents.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for free busy availability querying work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the free busy availability querying steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def aggregate(calendars):
    slots = set(range(24))
    for busy in calendars:
        slots -= set(busy)
    return sorted(slots)

cals = [[1, 2], [2, 3]]
assert aggregate(cals) == [0] + list(range(4, 24))
```

## Failure Modes
- Requesting full calendar read scope.
- Returning who is busy rather than how many.
- Querying windows far larger than the meeting needs.
- Caching availability across days without refresh.
- Ignoring timezones when merging calendars.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Least-privilege availability APIs are a recurring 2026 scheduling-automation topic in public coverage; this is a dated signal, not an adoption metric.

## Related
- google-workspace-api.md
- tool-argument-construction.md
- api-pagination.md
