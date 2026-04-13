---
title: "Notion API"
category: 07-tool-use
level: intermediate
stability: stable
description: "Apply notion api in AI agent workflows."
added: "2025-03"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-07-tool-use-notion-api.json)

# Notion API

**Category:** `tool-use`  
**Skill Level:** `intermediate`  
**Stability:** `stable`
**Added:** 2025-03

### Description

Read from and write to Notion databases, pages, and blocks via the Notion API.

### Example

```python
import httpx

headers = {'Authorization': f'Bearer {NOTION_KEY}', 'Notion-Version': '2022-06-28'}
r = httpx.post(
    'https://api.notion.com/v1/pages',
    headers=headers,
    json={
        'parent': {'database_id': DB_ID},
        'properties': {
            'Name': {'title': [{'text': {'content': 'New Skill: Tree of Thought'}}]}
        }
    }
)
```

### Related Skills

- [Google Workspace API](google-workspace-api.md)
- [Structured Output](../06-communication/structured-output.md)
