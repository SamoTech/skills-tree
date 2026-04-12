# Google Workspace API

**Category:** `tool-use`  
**Skill Level:** `intermediate`  
**Stability:** `stable`
**Added:** 2025-03

### Description

Interact with Google Docs, Sheets, Drive, Gmail, and Calendar programmatically via the Google Workspace APIs.

### Example

```python
from googleapiclient.discovery import build

# Read a Google Sheet
service = build('sheets', 'v4', credentials=creds)
result = service.spreadsheets().values().get(
    spreadsheetId=SHEET_ID, range='Sheet1!A1:D10'
).execute()
rows = result.get('values', [])
```

### Related Skills

- [Calendar Event](../04-action-execution/calendar-event.md)
- [Email Sending](../04-action-execution/email-sending.md)
