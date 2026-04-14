---
title: "Web Login"
category: 11-web
level: intermediate
stability: stable
added: "2025-03"
description: "Apply web login in AI agent workflows."
dependencies:
  - package: playwright
    min_version: "1.40.0"
    tested_version: "1.58.0"
    confidence: verified
code_blocks:
  - id: "example-login"
    type: executable
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-11-web-web-login.json)

# Web Login

**Category:** `web`  
**Skill Level:** `intermediate`  
**Stability:** `stable`
**Added:** 2025-03

### Description

Automate login flows: fill credentials, submit forms, handle redirects, and persist session cookies for subsequent requests.

### Example

```python
# pip install playwright && playwright install chromium
from playwright.sync_api import sync_playwright
import json

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    page.goto("https://app.example.com/login")
    page.fill("input[name='email']", "user@example.com")
    page.fill("input[name='password']", "s3cr3t")
    page.click("button[type='submit']")
    page.wait_for_url("**/dashboard")

    # Save session cookies for reuse
    cookies = page.context.cookies()
    with open("session.json", "w") as f:
        json.dump(cookies, f)

    browser.close()
```

### Related Skills
- `browser-navigation`, `cookie-management`, `form-filling`, `web-scraping`
