---
title: "Calendar Event"
category: 04-action-execution
level: intermediate
stability: stable
description: "Create a calendar event representation with explicit time zone, duration, participants, and confirmation boundaries."
added: "2026-09"
related: [form-submission, assertion, email-sending]
---

# Calendar Event

## Description

Construct or submit a calendar event while preserving time zone, duration, attendees, and summary. External calendar writes should remain explicit actions with duplicate-prevention controls.

## When to Use

- Preparing an iCalendar event for import.
- Creating an event through a calendar API.
- Translating an approved scheduling request into structured data.

## Inputs / outputs / failure modes

| Input | Output | Failure mode |
|---|---|---|
| Start/end time | Calendar event | Ambiguous time zone |
| Summary/location | Event fields | Missing data |
| Attendees | Participant list | Invalid address |
| Stable event ID | Idempotent identity | Duplicate event |

## Runnable example

```python
from datetime import datetime, timezone

start = datetime(2026, 9, 30, 15, 0, tzinfo=timezone.utc)
end = datetime(2026, 9, 30, 16, 0, tzinfo=timezone.utc)
event = {"summary": "Project review", "start": start.isoformat(), "end": end.isoformat()}
print(event)
```

## Failure modes

- Omitting a time zone and silently shifting the meeting.
- Creating duplicates without a stable identifier.
- Sending invitations when only a draft was requested.
- Trusting ambiguous attendee data.

## Related

- form-submission.md
- assertion.md
- email-sending.md

## Evidence

- AI_CONSTITUTION.md
- AGENTS.md
- Repository security and validation workflows
