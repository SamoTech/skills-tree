---
title: "Form Submission"
category: 04-action-execution
level: intermediate
stability: stable
description: "Apply form submission in AI agent workflows."
added: "2025-03"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-04-action-execution-form-submission.json)

# Form Submission

**Category:** `action-execution`  
**Skill Level:** `intermediate`  
**Stability:** `stable`
**Added:** 2025-03

### Description

Fill in and submit web forms programmatically — via browser automation or direct HTTP POST requests.

### Example

```python
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto('https://example.com/contact')
    page.fill('#name', 'AI Agent')
    page.fill('#message', 'Hello from the agent.')
    page.click('button[type=submit]')
    browser.close()
```

### Related Skills

- [Browser Navigation](../11-web/browser-navigation.md)
- [Form Filling](../11-web/form-filling.md)
