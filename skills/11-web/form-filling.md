# Form Filling

**Category:** `web`
**Skill Level:** `intermediate`
**Stability:** `stable`
**Added:** 2025-03

### Description

Locate HTML form fields, fill them with provided values, and submit the form — handling text inputs, dropdowns, checkboxes, radio buttons, and file uploads.

### Example

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto('https://example.com/contact')

    page.fill('#name', 'Ossama Hashim')
    page.fill('#email', 'ossama@example.com')
    page.select_option('#topic', 'support')
    page.check('#agree-terms')
    page.click('button[type="submit"]')
    page.wait_for_url('**/thank-you')
    browser.close()
```

### Related Skills

- [Browser Navigation](browser-navigation.md)
- [Web Login](web-login.md)
- [DOM Inspection](dom-inspection.md)
