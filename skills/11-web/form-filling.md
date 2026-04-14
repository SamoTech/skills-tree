---
title: "Form Filling"
category: 11-web
level: intermediate
stability: stable
added: "2025-03"
description: "Apply form filling in AI agent workflows."
dependencies:
  - package: playwright
    min_version: "1.40.0"
    tested_version: "1.58.0"
    confidence: verified
code_blocks:
  - id: "example-form"
    type: executable
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-11-web-form-filling.json)

# Form Filling

**Category:** `web`  
**Skill Level:** `intermediate`  
**Stability:** `stable`
**Added:** 2025-03

### Description

Fill HTML forms — text inputs, dropdowns, checkboxes, file uploads — and submit them programmatically.

### Example

```python
# pip install playwright && playwright install chromium
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://example.com/contact")

    # Text inputs
    page.fill("#name", "Agent Smith")
    page.fill("#email", "agent@example.com")
    page.fill("#message", "Hello from an AI agent.")

    # Dropdown
    page.select_option("select#category", "support")

    # Checkbox
    page.check("input[name='agree']")

    # Submit
    page.click("button[type='submit']")
    page.wait_for_selector(".success-message")
    browser.close()
```

### Related Skills
- `browser-navigation`, `web-login`, `dom-inspection`, `form-submission`
