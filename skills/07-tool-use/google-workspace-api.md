---
title: "Google Workspace API"
category: 07-tool-use
level: intermediate
stability: stable
description: "Apply google workspace api in AI agent workflows."
added: "2025-03"
dependencies:
  - package: google-api-python-client
    min_version: "2.100.0"
    tested_version: "2.130.0"
    confidence: verified
  - package: google-auth
    min_version: "2.23.0"
    tested_version: "2.29.0"
    confidence: verified
code_blocks:
  - id: "example-sheets"
    type: illustrative
    note: "Requires OAuth2 credentials setup — illustrative only"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-07-tool-use-google-workspace-api.json)

# Google Workspace API

**Category:** `tool-use`  
**Skill Level:** `intermediate`  
**Stability:** `stable`
**Added:** 2025-03

### Description

Interact with Google Docs, Sheets, Drive, Gmail, and Calendar programmatically via the Google Workspace APIs.

### Example

```python type:illustrative
# pip install google-api-python-client google-auth
# Note: `googleapiclient` is the import name for PyPI package `google-api-python-client`
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
