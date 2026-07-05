---
title: "Calendar Parsing"
category: 01-perception
level: basic
stability: stable
description: "Enable AI agents to parse iCal (.ics) files and calendar API responses into structured event objects for scheduling, analysis, and automation."
added: "2025-03"
version: "v2"
last_updated: "2026-07"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-01-perception-calendar-parsing.json)

# Calendar Parsing

**Category:** `01-perception`
**Skill Level:** `basic`
**Stability:** `stable`
**Version:** `v2`
**Added:** `2025-03`
**Last Updated:** `2026-07`

---

## Description

Calendar Parsing enables an agent to ingest `.ics` files, iCalendar strings, and calendar API responses (Google Calendar, Microsoft Graph) and convert them into normalized event objects. This skill is the foundation for scheduling agents, meeting summarizers, and availability analyzers. It handles recurring events, timezone normalization, and alarm extraction.

---

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `source` | `string` | ✅ | File path, URL, or raw iCalendar string |
| `source_type` | `string` | ❌ | `file` \| `url` \| `raw` \| `google_api` \| `ms_graph` (auto-detected if omitted) |
| `timezone` | `string` | ❌ | Target timezone for normalization (e.g. `UTC`, `Africa/Cairo`; default: `UTC`) |
| `expand_recurring` | `bool` | ❌ | Expand recurring events into individual instances (default: false) |
| `date_range` | `dict` | ❌ | `{"start": "YYYY-MM-DD", "end": "YYYY-MM-DD"}` to filter events |

---

## Outputs

| Output | Type | Description |
|---|---|---|
| `events` | `list[dict]` | Normalized event objects |
| `events[].uid` | `string` | Unique event identifier |
| `events[].summary` | `string` | Event title |
| `events[].start` | `datetime` | Start datetime (timezone-aware) |
| `events[].end` | `datetime` | End datetime (timezone-aware) |
| `events[].location` | `string` | Physical or virtual location |
| `events[].recurrence` | `string` | RRULE string if recurring |
| `events[].attendees` | `list[string]` | List of attendee email addresses |
| `total_count` | `int` | Total number of events parsed |

---

## Example

```python
from icalendar import Calendar
from datetime import datetime
import pytz

def parse_ical(source: str, timezone: str = "UTC") -> list[dict]:
    tz = pytz.timezone(timezone)
    with open(source, "rb") as f:
        cal = Calendar.from_ical(f.read())

    events = []
    for component in cal.walk():
        if component.name != "VEVENT":
            continue
        start = component.get("DTSTART").dt
        if isinstance(start, datetime) and start.tzinfo:
            start = start.astimezone(tz)
        events.append({
            "uid": str(component.get("UID", "")),
            "summary": str(component.get("SUMMARY", "")),
            "start": start.isoformat(),
            "end": component.get("DTEND").dt.isoformat() if component.get("DTEND") else None,
            "location": str(component.get("LOCATION", "")),
            "recurrence": str(component.get("RRULE", "")),
        })
    return events

events = parse_ical("calendar.ics", timezone="Africa/Cairo")
print(events[0])
# → {"uid": "abc123@google.com", "summary": "Team Standup", "start": "2026-07-05T10:00:00+03:00", ...}
```

```python
# Extended — expand recurring events with recurring_ical_events
import recurring_ical_events
from icalendar import Calendar
from datetime import date

with open("calendar.ics", "rb") as f:
    cal = Calendar.from_ical(f.read())

start = date(2026, 7, 1)
end = date(2026, 7, 31)
events = recurring_ical_events.of(cal).between(start, end)
for e in events:
    print(e["SUMMARY"], e["DTSTART"].dt)
```

---

## Frameworks & Models

| Framework / Model | Implementation | Since |
|---|---|---|
| Python `icalendar` | `Calendar.from_ical()` — RFC 5545 compliant parser | v1 |
| Python `recurring_ical_events` | Expands RRULE recurring instances into date ranges | v1 |
| Google Calendar API | `events.list()` returns JSON event objects directly | v1 |
| Microsoft Graph API | `GET /me/events` or `/me/calendarView` | v1 |
| LangChain `ICalendarLoader` | Wraps `icalendar` for LLM pipelines | v0.1 |
| GPT-4o | Parses raw iCal text natively in context | 2024-05 |
| Claude 3.7 Sonnet | Strong at interpreting RRULE patterns in natural language | 2025-01 |

---

## Model Comparison

| Capability | GPT-4o | Claude 3.7 Sonnet | Gemini 2.0 Flash | Notes |
|---|---|---|---|---|
| RRULE interpretation | 4 | 5 | 3 | Claude best at complex recurrence rules |
| Timezone reasoning | 4 | 4 | 4 | All models handle basic TZ, struggle with DST edge cases |
| JSON structuring | 5 | 5 | 4 | |
| Instruction following | 5 | 5 | 4 | |
| Edge case handling | 3 | 4 | 3 | All struggle with VALARM inflation |

---

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Timezone mismatch | `DTSTART` with no timezone info treated as local time | Always normalize to UTC on ingestion; use `pytz.utc` |
| VALARM inflation | Alarm components parsed as events | Filter `component.name == "VEVENT"` strictly |
| Recurring event explosion | Expanding daily events over years creates millions of instances | Apply `date_range` filter before expansion |
| Encoding errors | Non-UTF-8 `.ics` files from legacy clients | Open with `errors='replace'` or detect encoding via `chardet` |
| Missing DTEND | All-day events may omit DTEND | Fall back to `DTSTART + 1 day` for date-only events |

---

## Prompt Patterns

### Pattern 1 — Event Extraction
```
Parse the following iCalendar data and return all events as a JSON array.
Each event must include: uid, summary, start (ISO 8601), end (ISO 8601), location.

iCal data:
{ical_content}
```

### Pattern 2 — Availability Check
```
Given these calendar events:
{events_json}

Find all free time slots on {date} between {start_time} and {end_time}.
Return slots as: [{"start": "HH:MM", "end": "HH:MM", "duration_minutes": N}]
```

### Pattern 3 — Meeting Summary
```
Summarize the following calendar events for the week of {week_start}:
{events_json}

Group by day. For each day list:
- Meeting count
- Total meeting hours
- Key attendees
```

---

## Notes

- The `icalendar` library is RFC 5545 compliant but some clients (e.g. Outlook) produce non-standard extensions — use lenient parsing mode.
- Google Calendar API requires OAuth 2.0; for service accounts use a domain-wide delegation scope.
- `recurring_ical_events` can be slow on large `.ics` files with many RRULEs — cache expanded results.
- Date-only events (all-day) return `date` objects, not `datetime` — check `isinstance(dt, date)` before ISO formatting.

---

## Related Skills

- [Document Parsing](./document-parsing.md) — for extracting calendar data from PDF/Word attachments
- [Email Parsing](./email-parsing.md) — calendar invites are often embedded in emails as `.ics` attachments
- [Structured Data Reading](./structured-data-reading.md) — for Google Calendar JSON API responses

---

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-04` | v1 | Initial entry |
| `2026-07` | v2 | Added typed I/O tables, extended examples, full frameworks table, model comparison, prompt patterns, detailed failure modes |
