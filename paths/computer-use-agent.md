# Path: Computer Use Agent

**Difficulty:** ⭐⭐⭐ Advanced  
**Skills:** 5  
**Est. Time:** ~4 hours  
**Goal:** Build an agent that controls a desktop UI — parsing the screen, planning actions, clicking, typing, and verifying outcomes.

---

## Overview

Computer Use agents operate GUI applications without an API. They see the screen as pixels or an accessibility tree, plan a sequence of actions, and execute them via OS-level input simulation. This is the foundation of automated testing, RPA, and general computer-use assistants.

---

## Prerequisites

- Python 3.11+
- `pip install pillow pyautogui anthropic`
- A desktop environment (Windows, macOS, or Linux with a display)
- Claude claude-sonnet-4-5 API key (Anthropic's computer-use model)

---

## The Path

### Step 1 — Screen Parsing
`skills/10-computer-use/screen-parsing.md`

**Why first:** The agent's eyes. You learn how to capture screenshots, locate UI elements by coordinate and accessibility tree, and build a structured scene representation. Everything else depends on reliable screen understanding.

**Key takeaways:**
- Use accessibility tree (AT) parsing when available — more reliable than pixel coordinates
- Fall back to vision model + bounding box detection when AT is unavailable
- Cache the scene representation — re-capture only when an action has been taken

---

### Step 2 — Action Planning
`skills/09-agentic-patterns/action-planning.md`

**Why second:** Given a goal and a scene, the agent must plan a sequence of low-level actions (click, type, scroll, wait). This skill teaches goal decomposition into atomic UI actions with preconditions and expected post-states.

**Key takeaways:**
- Represent the plan as `[{action, target, value, expected_state}]`
- Validate preconditions before executing each action
- Keep plans short (≤10 steps) — re-plan after each verification checkpoint

---

### Step 3 — Action Execution
`skills/04-action-execution/ui-interaction.md`

**Why third:** Translate plan steps into actual OS-level inputs. This skill covers mouse click, keyboard type, scroll, drag, hotkeys, and clipboard operations across platforms.

**Key takeaways:**
- Add 150ms delay between actions — UIs need time to respond
- Use `pyautogui.locateOnScreen()` for image-based element targeting as fallback
- Always release modifiers (Ctrl, Alt, Shift) in a `finally` block

---

### Step 4 — State Verification
`skills/10-computer-use/state-verification.md`

**Why fourth:** After each action, the agent must verify the UI reached the expected state before proceeding. Without verification, errors compound silently. This skill teaches screenshot diff, element presence checks, and error recovery.

**Key takeaways:**
- Take a screenshot after every action, compare to expected state description
- On mismatch: retry once, then re-plan from current state
- Timeout after 3s waiting for UI to settle before taking verification screenshot

---

### Step 5 — Error Recovery
`skills/09-agentic-patterns/error-recovery.md`

**Why last:** Computer use agents fail often — popups appear, elements move, network dialogs interrupt. This skill teaches interruption detection, safe abort procedures, and graceful recovery strategies.

**Key takeaways:**
- Maintain an "undo stack" — record reversible actions for rollback
- On unexpected popup: screenshot → classify → dismiss or handle → resume
- Set a max-retry budget (3 retries per step, 10 total) to prevent infinite loops

---

## Code Scaffold

```python
# computer_use_agent.py — minimal computer use loop
import time
import pyautogui
import anthropic
from PIL import ImageGrab
import base64
import io

client = anthropic.Anthropic()

def screenshot_b64() -> str:
    """Capture screen and encode as base64 PNG."""
    img = ImageGrab.grab()
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode()

def ask_claude(goal: str, screen_b64: str, history: list) -> dict:
    """Ask Claude what action to take next."""
    messages = history + [{
        "role": "user",
        "content": [
            {"type": "image", "source": {"type": "base64", "media_type": "image/png", "data": screen_b64}},
            {"type": "text", "text": f"Goal: {goal}\nWhat is the next single action to take? Reply as JSON: {{\"action\": \"click|type|scroll|done\", \"x\": 0, \"y\": 0, \"text\": \"\", \"reason\": \"\"}}"}
        ]
    }]
    resp = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=256,
        messages=messages
    )
    import json, re
    raw = resp.content[0].text
    match = re.search(r'\{.*\}', raw, re.DOTALL)
    return json.loads(match.group()) if match else {"action": "done"}

def execute_action(action: dict) -> None:
    """Execute a single UI action — skills/04-action-execution/ui-interaction.md"""
    pyautogui.FAILSAFE = True
    kind = action.get("action", "done")
    if kind == "click":
        pyautogui.click(action["x"], action["y"])
    elif kind == "type":
        pyautogui.typewrite(action.get("text", ""), interval=0.05)
    elif kind == "scroll":
        pyautogui.scroll(action.get("amount", 3), x=action["x"], y=action["y"])
    time.sleep(0.15)  # let UI settle

def run_agent(goal: str, max_steps: int = 20) -> None:
    """Main agent loop."""
    history = []
    for step in range(max_steps):
        screen = screenshot_b64()
        action = ask_claude(goal, screen, history)
        print(f"[step {step+1}] {action}")
        if action.get("action") == "done":
            print("[agent] Goal complete.")
            break
        # Verify preconditions here (skills/10-computer-use/state-verification.md)
        execute_action(action)
        history.append({"role": "assistant", "content": str(action)})
    else:
        print("[agent] Max steps reached — re-plan or abort.")

if __name__ == "__main__":
    run_agent("Open Notepad, type 'Hello from the agent', and save the file as test.txt")
```

---

## Completion Checklist

- [ ] Agent successfully opens an application from the desktop
- [ ] Agent types into a text field correctly
- [ ] Verification step catches a wrong state at least once during testing
- [ ] Error recovery dismisses an unexpected dialog without crashing
- [ ] Full task (open → interact → save) completes in ≤20 steps

---

## Next Steps

- Add **accessibility tree parsing** for more reliable element targeting
- Integrate with **web browser** for cross-app workflows
- See the full system: `systems/computer-use-system.md`
