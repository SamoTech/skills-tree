![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-01-perception-calendar-parsing.json)

# Calendar Parsing
Category: perception | Level: basic | Stability: stable | Version: v1

## Description
Parse iCal (.ics) files and calendar API responses into structured event objects.

## Inputs
- `source`: .ics file path, URL, or raw iCal string

## Outputs
- List of events: `{uid, summary, start, end, location, recurrence}`

## Example
```python
from icalendar import Calendar
with open("calendar.ics", "rb") as f:
    cal = Calendar.from_ical(f.read())
for component in cal.walk():
    if component.name == "VEVENT":
        print(component.get("SUMMARY"), component.get("DTSTART").dt)
```

## Frameworks
| Framework | Method |
|---|---|
| Python | `icalendar`, `recurring_ical_events` |
| Google Calendar API | `events.list()` |
| Microsoft Graph | `/me/events` |

## Failure Modes
- Timezone mismatches in recurring events
- VALARM components inflate event list

## Related
- `document-parsing.md` · `email-parsing.md`

## Changelog
- v1 (2026-04): Initial entry
