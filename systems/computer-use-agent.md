---
title: Computer Use Agent
category: systems
version: v1
stability: experimental
skills: [screen-reading, ocr, click, type, scroll, file-system-reading, planning]
---

# Computer Use Agent

> Full GUI automation agent that perceives desktop/browser state via screenshots, plans action sequences, and executes click/type/scroll/key commands to complete multi-step tasks.

## Skills Used

| Skill | Role |
|---|---|
| `skills/01-perception/screen-reading.md` | Parse screenshot → structured UI state |
| `skills/01-perception/ocr.md` | Read text from non-native UI elements |
| `skills/10-computer-use/click.md` | Precise element targeting |
| `skills/10-computer-use/type.md` | Keyboard input with focus management |
| `skills/10-computer-use/scroll.md` | Navigate long pages / lists |
| `skills/02-reasoning/planning.md` | Multi-step task decomposition |
| `skills/02-reasoning/self-correction.md` | Detect failures, re-plan |

## Architecture

```
  Task: "Book a flight EGY→LHR on May 15 under $600"
        │
        ▼
┌─────────────────────┐
│    Task Planner     │  breaks task into ordered sub-goals
└─────────┬───────────┘
          │
    ┌─────▼──────────────────────────────┐
    │         Action Loop               │
    │                                   │
    │  Screenshot → Perceive UI state   │
    │       ↓                           │
    │  Plan next action (tool call)     │
    │       ↓                           │
    │  Execute: click / type / scroll   │
    │       ↓                           │
    │  Verify: expected state reached?  │
    │     yes → next step               │
    │     no  → self-correct / retry    │
    └─────────────────────────────────--┘
          │
          ▼
     Task complete / escalate to human
```

## Implementation

```python
import anthropic
import base64
from pathlib import Path

client = anthropic.Anthropic()

def screenshot_to_base64(path: str) -> str:
    return base64.b64encode(Path(path).read_bytes()).decode()

def run_computer_use_step(task: str, screenshot_path: str, history: list) -> dict:
    screenshot_b64 = screenshot_to_base64(screenshot_path)

    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1024,
        tools=[{
            "type": "computer_20250124",
            "name": "computer",
            "display_width_px": 1920,
            "display_height_px": 1080,
        }],
        system=f"You are completing this task: {task}\nUse the computer tool to interact with the screen.",
        messages=history + [{
            "role": "user",
            "content": [{
                "type": "image",
                "source": {"type": "base64", "media_type": "image/png", "data": screenshot_b64}
            }, {
                "type": "text",
                "text": "What is the current state of the screen? What action should I take next to complete the task?"
            }]
        }]
    )

    for block in response.content:
        if block.type == "tool_use" and block.name == "computer":
            return {"action": block.input["action"], "params": block.input, "done": False}
    return {"action": "none", "done": True, "summary": response.content[0].text}

def run_task(task: str, executor):
    history = []
    for step in range(30):  # max 30 steps
        shot = executor.screenshot()
        result = run_computer_use_step(task, shot, history)
        if result["done"]:
            return result["summary"]
        executor.execute(result["action"], result["params"])
        history.append({"role": "assistant", "content": str(result)})
```

## Failure Modes

| Failure | Cause | Fix |
|---|---|---|
| Infinite click loop | UI state not changing after action | Add state-hash comparison; break on repeat |
| Wrong element targeted | Overlapping / off-screen elements | Use accessibility tree as backup selector |
| CAPTCHA blocks | Bot detection | Pause + alert human; do not auto-solve |
| Action diverges from task | Ambiguous sub-goal | Break task into explicit checkpoints with verification |

## Related

- `blueprints/computer-use-browser.md`
- `skills/10-computer-use/`
- `skills/01-perception/screen-reading.md`

## Changelog

- `v1` (2026-04) — Initial agent with screenshot-driven action loop and self-correction
