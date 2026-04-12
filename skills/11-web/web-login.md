# Login / Authentication

**Category:** `web`
**Skill Level:** `intermediate`
**Stability:** `stable`

### Description

Authenticate to websites using username/password forms, OAuth flows, or session tokens. Supports storing and reusing session state to avoid repeated logins.

### Example

```python
from playwright.sync_api import sync_playwright
import json

with sync_playwright() as p:
    browser = p.chromium.launch()
    context = browser.new_context()
    page = context.new_page()

    page.goto('https://github.com/login')
    page.fill('#login_field', 'my-username')
    page.fill('#password', 'my-password')
    page.click('[type="submit"]')
    page.wait_for_url('https://github.com/')

    # Save session for reuse
    context.storage_state(path='session.json')
    browser.close()
```

### Related Skills

- [Form Filling](form-filling.md)
- [Cookie / Session Management](cookie-management.md)
- [Browser Navigation](browser-navigation.md)
