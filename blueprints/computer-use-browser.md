# Blueprint: Computer Use — Browser Automation

**Type:** `blueprint`  
**Pattern:** Vision + Action Loop  
**Complexity:** High  
**Status:** Experimental  
**Version:** v1

---

## Overview

An agent that controls a real browser using vision (screenshot → understand) and action (click, type, scroll) to complete web-based tasks without requiring API access. Combines screen reading, DOM inspection, and structured action execution.

---

## Architecture

```
  Task (natural language)
         │
         ▼
  ┌─────────────┐
  │   PERCEIVE  │  Screenshot → VLM description
  │             │  DOM inspection (optional)
  └──────┬──────┘
         │ observation
         ▼
  ┌─────────────┐
  │   REASON    │  "I can see a login form.
  │             │   I need to enter credentials.
  │             │   Next action: click username field."
  └──────┬──────┘
         │ action
         ▼
  ┌─────────────┐
  │   ACT       │  Playwright / Selenium / Pyautogui
  │             │  click(x,y) / type(text) / scroll()
  └──────┬──────┘
         │ new state
         └──────────────▶ back to PERCEIVE
                          (until task complete)
```

---

## Skills Used

| Skill | Role |
|---|---|
| [Screen Reading](../skills/01-perception/screen-reading.md) | Parse UI state from screenshot |
| [URL/DOM Inspection](../skills/01-perception/url-dom-inspection.md) | Structured element access |
| [Image Understanding](../skills/01-perception/image-understanding.md) | Interpret visual UI elements |
| [Planning](../skills/02-reasoning/planning.md) | Multi-step task execution |
| [Risk Assessment](../skills/02-reasoning/risk-assessment.md) | Prevent destructive actions |

---

## Implementation (Playwright + Claude Vision)

```python
from playwright.sync_api import sync_playwright
from anthropic import Anthropic
import base64, io
from PIL import Image

client = Anthropic()

def browser_agent(task: str, max_steps: int = 20):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1280, "height": 720})
        page.goto("about:blank")

        messages = [{"role": "user", "content": [
            {"type": "text", "text": f"Task: {task}\nStart navigating to accomplish this task."}
        ]}]

        for step in range(max_steps):
            # 1. Screenshot → base64
            screenshot = page.screenshot()
            img_b64 = base64.b64encode(screenshot).decode()

            # 2. Ask LLM what to do next
            messages.append({"role": "user", "content": [
                {"type": "image", "source": {"type": "base64",
                 "media_type": "image/png", "data": img_b64}},
                {"type": "text", "text":
                 "What do you see? What is the next action? "
                 "Respond with JSON: {\"action\": \"click|type|navigate|scroll|done\", "
                 "\"target\": \"CSS selector or URL\", \"value\": \"text if typing\"}"}
            ]})

            resp = client.messages.create(
                model="claude-opus-4-5", max_tokens=512, messages=messages
            )
            action = parse_json(resp.content[0].text)
            messages.append({"role": "assistant", "content": resp.content[0].text})

            # 3. Execute action
            if action["action"] == "done":
                return page.url, page.content()
            elif action["action"] == "click":
                page.click(action["target"])
            elif action["action"] == "type":
                page.fill(action["target"], action["value"])
            elif action["action"] == "navigate":
                page.goto(action["target"])
            elif action["action"] == "scroll":
                page.mouse.wheel(0, int(action.get("value", 500)))

            page.wait_for_timeout(500)  # let page settle

        browser.close()
        return None, "Max steps reached"
```

---

## Action Space

| Action | When | Risk Level |
|---|---|---|
| `navigate(url)` | Go to a URL | Low |
| `click(selector)` | Click element | Medium |
| `type(selector, text)` | Fill input | Medium |
| `scroll(pixels)` | Scroll page | Low |
| `select(selector, option)` | Dropdown | Medium |
| `submit()` | Submit form | **High — confirm first** |
| `download(url)` | Download file | Medium |

---

## Guardrails

- **URL allow-list** — only navigate to pre-approved domains
- **No form submission** without explicit user confirmation in the task
- **Screenshot diff** — if 3 consecutive screenshots are identical, agent is stuck → abort
- **Loop detection** — if visiting the same URL > 3 times, try different strategy
- **Max steps hard limit** — configurable, default 20

---

## Provider Comparison

| Approach | Accuracy | Latency | Cost |
|---|---|---|---|
| Screenshot + VLM | High | ~2s/step | $$$ |
| DOM-only + LLM | Medium | ~0.5s/step | $ |
| Hybrid (DOM + screenshot) | Highest | ~2.5s/step | $$$$ |
| Playwright codegen + LLM | Medium | ~1s/step | $$ |

---

## Related

- [Blueprint: Multi-Agent Workflow](multi-agent-workflow.md)
- [Skill: Screen Reading](../skills/01-perception/screen-reading.md)
- [System: Research Agent](../systems/research-agent.md)
