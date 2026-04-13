---
title: "Clipboard Operations"
category: 04-action-execution
level: basic
stability: stable
description: "Apply clipboard operations in AI agent workflows."
added: "2025-03"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-04-action-execution-clipboard-ops.json)

# Clipboard Operations

**Category:** `action-execution`  
**Skill Level:** `basic`  
**Stability:** `stable`
**Added:** 2025-03

### Description

Read from or write to the system clipboard programmatically.

### Example

```python
import pyperclip

# Write
pyperclip.copy('Hello from the agent!')

# Read
text = pyperclip.paste()
print(text)
```

### Related Skills

- [Keyboard Input](keyboard-input.md)
- [Screenshot Capture](screenshot-capture.md)
