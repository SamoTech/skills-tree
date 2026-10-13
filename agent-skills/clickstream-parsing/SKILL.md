---
name: clickstream-parsing
description: Parse clickstream and event-stream logs into ordered user sessions with timestamps and event types, and flag malformed or out-of-order events instead of dropping them silently.
metadata:
  source: skills/01-perception/clickstream-parsing.md
  category: 01-perception
  version: "v1"
---

# Clickstream Parsing

## Description
Parse clickstream and event-stream logs into ordered user sessions with timestamps and event types, and flag malformed or out-of-order events instead of dropping them silently. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- behavioral analytics depend on well-formed sessions reconstructed from raw event logs before downstream steps can proceed safely.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for clickstream parsing work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the clickstream parsing steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def to_sessions(events, gap_s=1800):
    sessions, cur, last = [], [], None
    flagged = []
    for ts, user, kind in sorted(events):
        if cur and (user != cur[0][1] or ts - last > gap_s):
            sessions.append(cur); cur = []
        if last is not None and ts < last:
            flagged.append((ts, user))
        cur.append((ts, user, kind)); last = ts
    if cur: sessions.append(cur)
    return sessions, flagged

ev = [(10, "u1", "view"), (20, "u1", "click"), (9999, "u1", "view")]
sess, flagged = to_sessions(ev)
assert len(sess) == 2 and flagged == []
```

## Failure Modes
- Merging distinct users into one session.
- Silently dropping out-of-order events.
- Assuming the log is chronologically sorted.
- Deriving identity across sessions without consent.
- Treating session count as a user count.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Agent-assisted analytics and product telemetry remain recurring 2026 requests in public data-tool coverage; this is a dated signal, not an adoption metric.

## Related
- log-parsing.md
- time-series-reading.md
- iot-telemetry-parsing.md
