---
name: clipboard-ops
description: Read or write clipboard content with explicit content handling and privacy boundaries.
metadata:
  source: skills/04-action-execution/clipboard-ops.md
  category: 04-action-execution
---

# Clipboard Operations

## Description

Transfer text or other supported clipboard data between an agent and the active desktop environment. Clipboard contents may contain credentials or personal data and must not be logged or exfiltrated by default.

## When to Use

- Pasting approved text into an application.
- Reading user-provided clipboard content for an explicit task.
- Moving text between desktop applications.

## Inputs / outputs / failure modes

| Input | Output | Failure mode |
|---|---|---|
| Clipboard text | Text value | Clipboard unavailable |
| Write payload | Updated clipboard | Platform error |
| Privacy policy | Redacted handling | Sensitive data leakage |
| Target application | Pasted value | Wrong focus/window |

## Runnable example

```python
import tkinter as tk

root = tk.Tk()
root.withdraw()
root.clipboard_clear()
root.clipboard_append("approved text")
root.update()
print(root.clipboard_get())
root.destroy()
```

## Failure modes

- Printing clipboard contents into logs.
- Copying secrets to an unintended application.
- Assuming the active window is the intended target.
- Leaving sensitive data in the clipboard unnecessarily.

## Related

- keyboard-input.md
- mouse-input.md
- ../14-security/input-guardrails.md

## Evidence

- AI_CONSTITUTION.md
- AGENTS.md
- Repository security and validation workflows
