---
title: "Browser Navigation"
category: 11-web
level: intermediate
stability: stable
added: "2025-03"
description: "Apply browser navigation in AI agent workflows."
dependencies:
  - package: playwright
    min_version: "1.40.0"
    tested_version: "1.58.0"
    confidence: verified
code_blocks:
  - id: "example-navigation"
    type: executable
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-11-web-browser-navigation.json)

# Browser Navigation

**Category:** `web`  
**Skill Level:** `intermediate`  
**Stability:** `stable`
**Added:** 2025-03

### Description

Control a real browser to navigate URLs, interact with pages, and handle dynamic JavaScript-rendered content.

### Example

```python
# pip install playwright && playwright install chromium
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    page.goto("https://example.com")
    print(page.title())

    # Click a link
    page.click("a[href='/about']")
    page.wait_for_load_state("networkidle")

    # Go back
    page.go_back()

    # Get full page HTML
    html = page.content()
    browser.close()
```

### Related Skills
- `web-login`, `form-filling`, `dom-inspection`, `url-screenshot`, `web-scraping`
