---
title: "Cookie / Session Management"
category: 11-web
level: advanced
stability: stable
description: "Apply cookie / session management in AI agent workflows."
added: "2025-03"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-11-web-cookie-management.json)

# Cookie / Session Management

**Category:** `web`
**Skill Level:** `advanced`
**Stability:** `stable`
**Added:** 2025-03

### Description

Read, set, and delete browser cookies and session storage to maintain authenticated state, bypass consent banners, or inject session tokens for headless automation.

### Example

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    context = browser.new_context()

    # Load saved session state (cookies + localStorage)
    context = browser.new_context(storage_state='session.json')
    page = context.new_page()
    page.goto('https://github.com')  # already logged in

    # Manually set a cookie
    context.add_cookies([{
        'name': 'consent', 'value': '1',
        'domain': '.example.com', 'path': '/'
    }])
    browser.close()
```

### Related Skills

- [Web Login](web-login.md)
- [Browser Navigation](browser-navigation.md)
- [JavaScript Execution](js-execution.md)
