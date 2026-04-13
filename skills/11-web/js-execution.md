---
title: "JavaScript Execution"
category: 11-web
level: advanced
stability: stable
description: "Apply javascript execution in AI agent workflows."
added: "2025-03"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-11-web-js-execution.json)

# JavaScript Execution

**Category:** `web`
**Skill Level:** `advanced`
**Stability:** `stable`
**Added:** 2025-03

### Description

Inject and execute arbitrary JavaScript in the browser context to interact with the DOM, extract data, trigger events, or bypass limitations of standard automation APIs.

### Example

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto('https://example.com')

    # Extract data via JS
    title = page.evaluate("document.title")
    links = page.evaluate("[...document.querySelectorAll('a')].map(a => a.href)")

    # Trigger a hidden event
    page.evaluate("document.querySelector('#hidden-btn').click()")

    # Scroll to bottom
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")

    browser.close()
```

### Related Skills

- [DOM Inspection](dom-inspection.md)
- [Browser Navigation](browser-navigation.md)
- [Web Scraping](web-scraping.md)
