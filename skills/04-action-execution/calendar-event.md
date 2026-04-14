---
title: "Calendar Event Creation"
category: 04-action-execution
level: intermediate
stability: stable
description: "Apply calendar event creation in AI agent workflows."
added: "2025-03"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-04-action-execution-calendar-event.json)

# Calendar Event Creation

**Category:** `action-execution`  
**Skill Level:** `intermediate`  
**Stability:** `stable`
**Added:** 2025-03

### Description

Create, update, or delete calendar events via calendar APIs (Google Calendar, Outlook, CalDAV).

### Example

```python type:illustrative
# pip install google-api-python-client google-auth
# Note: `googleapiclient` is the import name for PyPI package `google-api-python-client`
from googleapiclient.discovery import build

service = build('calendar', 'v3', credentials=creds)
event = {
    'summary': 'Agent Review Meeting',
    'start': {'dateTime': '2026-04-15T10:00:00+02:00'},
    'end':   {'dateTime': '2026-04-15T11:00:00+02:00'},
}
service.events().insert(calendarId='primary', body=event).execute()
```

### Related Skills

- [Email Sending](email-sending.md)
- [Notification Sending](notification-sending.md)
