---
name: action-execution-screenshot-capture
description: Capture a verified application or screen region while minimizing sensitive content exposure.
metadata:
  source: skills/04-action-execution/screenshot-capture.md
  category: 04-action-execution
---

# Screenshot Capture

## Description

Capture a verified application or screen region while minimizing sensitive content exposure.

## When to Use

- Execute an explicitly approved action.
- Use when the target and scope can be verified.
- Verify the resulting state when the action is consequential.

## Inputs / outputs / failure modes

| Input | Output | Failure mode |
|---|---|---|
| Target and action | Execution result | Invalid target |
| Scope/authorization | Allowed action | Unauthorized action |
| Timeout/bounds | Controlled execution | Resource exhaustion |
| Postcondition | Verified state | Silent failure |

## Runnable Example

```python
from pathlib import Path
def capture(page, path):
    page.screenshot(path=path)
    if not Path(path).is_file(): raise RuntimeError("capture failed")
    return path
```

## Failure modes

Capturing private data; uncontrolled storage; unverified artifact; excessive capture scope.

## Related

- `screen-reading.md`
- `mouse-input.md`
- `clipboard-ops.md`

## Evidence

- AI_CONSTITUTION.md
- AGENTS.md
- Repository security and validation workflows
