# Form Submission

**Category:** `action-execution`  
**Skill Level:** `intermediate`  
**Stability:** `stable`

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
