---
title: "DOM Inspection"
category: 11-web
level: intermediate
stability: stable
description: "Apply dom inspection in AI agent workflows."
added: "2025-03"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-11-web-dom-inspection.json)

# DOM Inspection

**Category:** `web`
**Skill Level:** `intermediate`
**Stability:** `stable`
**Added:** 2025-03

### Description

Query and traverse the live Document Object Model (DOM) of a loaded web page to extract element attributes, text, structure, or relationships between nodes.

### Example

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto('https://news.ycombinator.com')

    # Query all story titles
    titles = page.query_selector_all('.titleline > a')
    for t in titles:
        print(t.text_content(), t.get_attribute('href'))

    # Get element attributes
    logo = page.query_selector('#hnmain td img')
    print(logo.get_attribute('src'))
    browser.close()
```

### Related Skills

- [JavaScript Execution](js-execution.md)
- [Web Scraping](web-scraping.md)
- [Browser Navigation](browser-navigation.md)
