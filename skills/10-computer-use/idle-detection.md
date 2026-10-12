---
title: "Idle Detection"
category: 10-computer-use
level: basic
stability: experimental
description: "Detect user idle periods from timestamped activity events against an explicit threshold so background work can schedule itself into measured quiet windows."
added: "2026-10"
version: v1
related: ["mouse-move", "keyboard-shortcut"]
---

# Idle Detection

Category: Computer Use | Level: basic | Stability: experimental | Version: v1

## Description

“The user looks away” is not an observation until it is defined: idle is a gap between timestamped activity events that meets a declared threshold. This skill computes idle periods from an activity log — each gap at or above the threshold is a quiet window, including the trailing gap up to now. The threshold is a policy number, recorded with the results, not an intuition.

## When to Use

Use when background work — indexing, syncing, heavy computation — should run in measured quiet windows on a shared machine, or when session security needs an observable inactivity signal.

Do not use to infer user intent or presence for surveillance purposes; this contract measures gaps, not people.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `events` | `list[number]` | Yes | Timestamps of user activity, sorted ascending |
| `threshold` | `number` | Yes | Idle duration in seconds that defines a quiet window |
| `now` | `number` | Yes | Current time bounding the trailing gap |

## Procedure

1. Require sorted activity timestamps; unsorted input is rejected before gaps are computed.
2. Compute each gap between consecutive events; a gap at or above the threshold is an idle period.
3. Include the trailing gap from the last event to now when it meets the threshold.
4. Return periods as (start, end) pairs so downstream work can schedule against real windows.
5. Record the threshold alongside the results; a bare window list is uninterpretable later.
6. Re-validate the threshold after usage changes; the right quiet window is a moving target.

## Outputs

| Output | Type | Description |
|---|---|---|
| `periods` | `list[(start, end)]` | Idle windows at or above the threshold |
| `total_idle` | `number` | Summed idle time across all windows |
| `longest` | `number` | Duration of the longest quiet window |

## Runnable Example

```python
def idle_periods(events, threshold, now):
    """Sorted activity timestamps -> idle gaps at or above threshold."""
    periods = []
    previous = None
    for t in events:
        if previous is not None and t - previous >= threshold:
            periods.append((previous, t))
        previous = t
    if previous is not None and now - previous >= threshold:
        periods.append((previous, now))
    return periods

events = [1.0, 2.0, 8.0, 9.0]
periods = idle_periods(events, threshold=3.0, now=15.0)
print(periods, "longest:", max(b - a for a, b in periods))
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| False idle | Clock skew between event sources | Use one monotonic time source for events and now |
| Threshold guessing | Quiet window tuned by intuition | Measure actual gap distribution and set policy from it |
| Trailing gap omitted | Current quiet window never reported | Always evaluate the last event against now |
| Micro-gap noise | Every small pause counted as idle | Only gaps at or above the threshold qualify |
| Activity starvation | No events logged, idle undefined | Report insufficient evidence rather than inventing windows |

## Security and Authority Boundary

Activity timestamps are behavioral data about a person. Idle detection for scheduling must respect declared consent scopes, and its logs inherit the retention rules of the activity source.

## Evidence

This skill is grounded in dated public implementation references:

1. MDN documentation for the Idle Detection API (https://developer.mozilla.org/en-US/docs/Web/API/Idle_Detection_API).
2. Python’s bisect module documentation for ordered event handling (https://docs.python.org/3/library/bisect.html).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Mouse Move](mouse-move.md) — a primary activity signal whose timestamps feed this gap analysis.
- [Keyboard Shortcut](keyboard-shortcut.md) — input events that reset the idle clock alongside mouse activity.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
