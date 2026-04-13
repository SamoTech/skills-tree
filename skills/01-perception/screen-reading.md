---
title: "Screen Reading"
category: 01-perception
level: intermediate
stability: stable
description: "Apply screen reading in AI agent workflows."
added: "2025-03"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-01-perception-screen-reading.json)

# Screen Reading

**Category:** `perception`  
**Skill Level:** `intermediate`  
**Stability:** `stable`  
**Added:** 2025-03  
**Last Updated:** 2026-04

---

## Description

Capture, analyze, and extract structured information from screenshots or live screen grabs. Identifies UI elements (buttons, inputs, menus, dialogs), reads text via vision, detects application state, and returns a machine-readable description of what is currently visible on screen. Foundation skill for computer-use agents.

---

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `screenshot` | `bytes` / `url` | ✅ | PNG or JPEG screenshot |
| `task` | `string` | ❌ | Task context hint, e.g. `"find the submit button"` |

---

## Outputs

| Output | Type | Description |
|---|---|---|
| `application` | `string` | Detected app name or type |
| `current_view` | `string` | Page or dialog name |
| `interactive_elements` | `list` | `[{type, label, position_hint}]` |
| `errors_or_alerts` | `list` | Visible error messages or modal dialogs |
| `suggested_next_action` | `string` | What a user would likely do next |

---

## Example

```python
import anthropic
import base64
from pathlib import Path

client = anthropic.Anthropic()

def read_screen(screenshot_path: str) -> str:
    """Analyze a screenshot and return a structured UI state description."""
    image_data = base64.standard_b64encode(
        Path(screenshot_path).read_bytes()
    ).decode("utf-8")

    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1024,
        messages=[{
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/png",
                        "data": image_data
                    }
                },
                {
                    "type": "text",
                    "text": (
                        "Analyze this screenshot and return JSON with:\n"
                        "- application: detected app name or type\n"
                        "- current_view: page or dialog name\n"
                        "- visible_text: list of all readable text blocks\n"
                        "- interactive_elements: [{type, label, position_hint}]\n"
                        "- errors_or_alerts: any error messages or modal dialogs\n"
                        "- suggested_next_action: what a user would likely do next\n"
                        "Return ONLY valid JSON."
                    )
                }
            ]
        }]
    )
    return response.content[0].text

state = read_screen("screenshot.png")
print(state)
```

---

## Frameworks & Models

| Framework / Model | Implementation | Since |
|---|---|---|
| Claude claude-opus-4-5 | Native vision via `image` content block | 2024-06 |
| GPT-4o | Vision via `image_url` | 2024-05 |
| LangChain | `ChatAnthropic` + image message | v0.2 |
| Anthropic Computer Use | Built-in screenshot + action loop | 2024-10 |

---

## Notes

- Use PNG for lossless screenshots; avoid JPEG compression artifacts
- For real-time agents, capture at reduced resolution (1280×720) to reduce token usage
- Combine with [URL/DOM Inspection](url-dom-inspection.md) for more reliable element targeting on web pages

---

## Related Skills

- [OCR](ocr.md) — text-only extraction from screen
- [Image Understanding](image-understanding.md) — general image analysis
- [URL/DOM Inspection](url-dom-inspection.md) — structured web page reading

---

## Changelog

| Date | Change |
|---|---|
| `2026-04` | Expanded from stub: full description, I/O table, screenshot analysis example |
| `2025-03` | Initial stub entry |
