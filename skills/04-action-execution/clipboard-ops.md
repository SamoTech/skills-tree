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
