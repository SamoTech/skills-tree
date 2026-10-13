---
name: cross-timezone-async-communication
description: Write asynchronous updates across timezones with explicit deadlines in named zones, decision deadlines, and no-meeting-required formats.
metadata:
  source: skills/06-communication/cross-timezone-async-communication.md
  category: 06-communication
  version: "v1"
---

# Cross Timezone Async Communication

## Description
Write asynchronous updates across timezones with explicit deadlines in named zones, decision deadlines, and no-meeting-required formats. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- a team spans timezones and decisions must progress while members are offline.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for cross timezone async communication work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the cross timezone async communication steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def deadline_in(tz_offsets, utc_hour):
    return {tz: (utc_hour + off) % 24 for tz, off in tz_offsets.items()}

d = deadline_in({"SF": -8, "BER": 2}, 14)
assert d["SF"] == 6 and d["BER"] == 16
```

## Failure Modes
- Writing deadlines like end of day with no zone.
- Assuming everyone saw the message instantly.
- Blocking progress on one offline approver.
- Scheduling meetings that split some region into night hours.
- No written summary after the async decision.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Distributed async decision-making is a recurring 2026 remote-work topic in public coverage; this is a dated signal, not an adoption metric.

## Related
- stakeholder-status-updates.md
- meeting-decision-recording.md
- email-drafting.md
