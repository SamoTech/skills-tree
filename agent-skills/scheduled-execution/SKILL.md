---
name: scheduled-execution
description: Run work at explicit times or intervals — cron-style schedules, ISO 8601 recurrences, and named time zones — with missed-run handling stated instead of improvised.
metadata:
  source: skills/04-action-execution/scheduled-execution.md
  category: 04-action-execution
  version: "v1"
---

# Scheduled Execution

Category: Action Execution | Level: basic | Stability: experimental | Version: v1

## Description

A request to run something every night hides a stack of decisions: which time zone, what happens to a run missed during downtime, and whether overlapping runs are allowed. This skill turns schedule intent into an explicit schedule — recurrence expression, time zone, catch-up policy, concurrency rule — and makes missed-run behavior a stated choice rather than an accident.

## When to Use

Use for recurring agent or system work — periodic syncs, reports, maintenance, retention sweeps — that must happen at known times without a human pressing go.

Do not deploy a schedule without deciding missed-run behavior; a scheduler that silently skips or silently piles up is one incident away from discovery.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `task` | `callable` | Yes | The work to run |
| `recurrence` | `string` | Yes | Cron expression or ISO 8601 recurrence |
| `timezone` | `string` | Yes | The zone the schedule is anchored to |
| `policy` | `map` | No | Missed-run and overlap handling |

## Procedure

1. Express the recurrence in an explicit, reviewable form — a cron expression or ISO 8601 rule — not as an opaque delay constant.
2. Anchor the schedule to a named time zone; unanchored times drift with daylight-saving shifts and server moves.
3. Decide the missed-run policy — run once on catch-up, skip, or run every missed slot — and state it next to the schedule.
4. Decide the overlap policy: cancel the previous run, allow concurrent runs, or skip if the previous run is still going.
5. Record each run with its scheduled time, actual start, and outcome so schedule health is observable.
6. Test at the boundaries — month ends, daylight-saving transitions, leap days — because that is where schedule defects live.

## Outputs

| Output | Type | Description |
|---|---|---|
| `schedule` | `map` | Recurrence, zone, and policies for the task |
| `runs` | `list` | Per-run record with scheduled and actual times |
| `health` | `map` | Missed, skipped, and overlapping run counts |

## Runnable Example

```python
from datetime import datetime, timedelta

def next_run(hour, now):
    scheduled = now.replace(hour=hour, minute=0, second=0, microsecond=0)
    if scheduled <= now:
        scheduled += timedelta(days=1)
    return scheduled.isoformat()

def catch_up_missed(last_run, now, hour, policy):
    missed = []
    cursor = last_run
    while (cursor := cursor + timedelta(days=1)) <= now:
        if cursor.hour == hour:
            missed.append(cursor.isoformat())
    return missed if policy == "run-each" else missed[:1]

now = datetime(2026, 10, 12, 6, 0)
print(next_run(4, now))
print(catch_up_missed(datetime(2026, 10, 10, 4, 0), now, 4, "run-once"))
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Floating times | No zone means the meaning changes with the server | Anchor to a named time zone |
| Silent skips | Missed runs during downtime are never addressed | State the missed-run policy |
| Overlap pile-ups | Long runs spawn concurrent copies | Decide the overlap policy explicitly |
| DST surprises | Off-by-one hours around transitions | Test daylight-saving boundaries |
| Invisible health | Nobody knows how often runs were missed | Record per-run scheduled and actual times |

## Security and Authority Boundary

Scheduled work runs unattended with whatever credentials the scheduler holds. Scope those credentials to the task, prefer short-lived credentials, avoid schedules that trigger privileged actions without limits, and alert on schedule changes — a moved job is a common persistence trick.

## Evidence

This skill is grounded in dated public implementation references:

1. Wikipedia's overview of cron, the canonical scheduling syntax (https://en.wikipedia.org/wiki/Cron).
2. Wikipedia's overview of ISO 8601 interval notation (https://en.wikipedia.org/wiki/ISO_8601).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Wait Sleep](wait-sleep.md) — the in-process delay primitive distinct from durable scheduling.
- [Calendar Event](calendar-event.md) — the human-facing scheduling counterpart.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
