# Computer Use Agent System

**Category:** systems | **Level:** advanced | **Stability:** experimental | **Version:** v1

## Overview

A full GUI automation agent that perceives live screen state, maps UI elements via accessibility tree or OCR, plans the next action (click, type, scroll, key), executes it, and loops until the goal is achieved — enabling end-to-end task completion in any desktop or browser application without an API.

---

## Skills Used

| Skill | Role in System |
|---|---|
| `skills/10-computer-use/screen-reading.md` | Capture and interpret the current screen |
| `skills/01-perception/ocr.md` | Extract text from non-accessible UI elements |
| `skills/10-computer-use/a11y-tree.md` | Parse accessibility tree for element targeting |
| `skills/10-computer-use/click.md` | Execute mouse click at target coordinate |
| `skills/10-computer-use/type.md` | Send keyboard input to focused element |
| `skills/10-computer-use/scroll.md` | Scroll to reveal off-screen content |
| `skills/02-reasoning/planning.md` | Decompose goal into ordered UI action steps |
| `skills/02-reasoning/self-correction.md` | Detect failed actions and retry differently |

---

## Architecture

```
┌──────────────────────────────────────────────────────┐
│               Computer Use Agent Loop                │
├──────────────────────────────────────────────────────┤
│                                                      │
│  Goal: "Book a flight from Cairo to London"          │
│    │                                                 │
│    ▼                                                 │
│  ┌─────────────────────────────────────────────┐    │
│  │             Perception Layer                │    │
│  │   Screenshot → OCR + a11y tree → JSON state │    │
│  └──────────────────────┬──────────────────────┘    │
│                         │                           │
│                         ▼                           │
│  ┌─────────────────────────────────────────────┐    │
│  │              Planning Layer                 │    │
│  │   Current state + goal → next action        │    │
│  │   {type: click|type|scroll|key, target, val}│    │
│  └──────────────────────┬──────────────────────┘    │
│                         │                           │
│                         ▼                           │
│  ┌─────────────────────────────────────────────┐    │
│  │             Execution Layer                 │    │
│  │   PyAutoGUI / Playwright / xdotool          │    │
│  └──────────────────────┬──────────────────────┘    │
│                         │                           │
│                         ▼                           │
│           Goal reached? ──► Done                    │
│                No ──► Loop (max 50 steps)            │
└──────────────────────────────────────────────────────┘
```

---

## Implementation

```python
import anthropic
import base64
import pyautogui
import json
from PIL import ImageGrab

client = anthropic.Anthropic()

AGENT_SYSTEM = """
You are a computer use agent. You see the current screen as an image.
Your goal is provided. Output the SINGLE next action as JSON:
{
  "action": "click|type|scroll|key|done|fail",
  "x": int (for click/scroll),
  "y": int (for click/scroll),
  "text": str (for type/key),
  "direction": "up|down" (for scroll),
  "reason": "why this action",
  "goal_complete": true/false
}
If the goal is complete, use action=done. If you're stuck after reasoning, use action=fail.
"""

def take_screenshot() -> str:
    """Capture screen and return as base64."""
    img = ImageGrab.grab()
    import io
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return base64.standard_b64encode(buf.getvalue()).decode()

def get_next_action(goal: str, screenshot_b64: str, step: int) -> dict:
    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=512,
        system=AGENT_SYSTEM,
        messages=[{
            "role": "user",
            "content": [
                {"type": "image", "source": {"type": "base64", "media_type": "image/png", "data": screenshot_b64}},
                {"type": "text", "text": f"Goal: {goal}\nStep: {step}/50"}
            ]
        }]
    )
    return json.loads(response.content[0].text)

def execute_action(action: dict):
    match action["action"]:
        case "click":
            pyautogui.click(action["x"], action["y"])
        case "type":
            pyautogui.typewrite(action["text"], interval=0.05)
        case "scroll":
            direction = -3 if action["direction"] == "down" else 3
            pyautogui.scroll(direction, x=action["x"], y=action["y"])
        case "key":
            pyautogui.hotkey(*action["text"].split("+"))

def run_agent(goal: str, max_steps: int = 50) -> str:
    for step in range(1, max_steps + 1):
        screenshot = take_screenshot()
        action = get_next_action(goal, screenshot, step)
        print(f"Step {step}: {action['action']} — {action['reason']}")

        if action["action"] == "done":
            return "SUCCESS"
        if action["action"] == "fail":
            return f"FAILED at step {step}: {action['reason']}"

        execute_action(action)
        import time; time.sleep(0.8)  # wait for UI to settle

    return "TIMEOUT: max steps reached"

# Usage
if __name__ == "__main__":
    result = run_agent("Open Chrome, go to github.com, and star the skills-tree repo")
    print(f"Result: {result}")
```

---

## Failure Modes

| Failure | Cause | Mitigation |
|---|---|---|
| Wrong element clicked | Coordinate drift, dynamic layouts | Use a11y tree IDs over pixel coordinates |
| Infinite loop | UI stuck / modal blocking | Detect repeated identical screenshots → abort |
| Rate limiting | Too many API calls | Add 800ms sleep between steps |
| Coordinate mismatch | HiDPI / retina displays | Scale coordinates by display DPI factor |

---

## Safety Guardrails

```python
BLOCKED_ACTIONS = ["rm -rf", "format", "DELETE FROM", "sudo"]
# Always run in a VM or sandboxed environment
# Never give the agent access to payment forms or admin panels without human approval
# Log every screenshot + action for audit
```

---

## Related

- `blueprints/computer-use-browser.md` — Browser-specific variant using Playwright
- `skills/10-computer-use/screen-reading.md` · `skills/01-perception/ocr.md`
- `skills/02-reasoning/self-correction.md` — Critical for recovery from failed steps

## Changelog

- **v1** (2026-04) — Initial system: screenshot loop, action planning, PyAutoGUI execution
