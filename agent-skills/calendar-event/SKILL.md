---
name: calendar-event
description: Create a calendar event representation with explicit time zone, duration, participants, and confirmation boundaries.
license: MIT
metadata:
  source: skills/04-action-execution/calendar-event.md
  version: "v2"
---

# Calendar Event

1. Resolve start, end, and time zone explicitly.
2. Validate summary, location, and attendee fields.
3. Assign a stable event identifier where duplicate prevention matters.
4. Keep external calendar writes behind the required approval boundary.

## Failure modes

- Ambiguous time zone.
- Duplicate event creation.
- Sending invitations when only a draft was requested.

## Evidence

- skills/04-action-execution/calendar-event.md
- AI_CONSTITUTION.md
- AGENTS.md

Evidence status: repository-backed implementation guidance; no benchmark claim.
