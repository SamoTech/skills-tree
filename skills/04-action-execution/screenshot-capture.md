---
title: "Screenshot Capture (App Region)"
category: 04-action-execution
level: basic
stability: stable
version: v1
description: "Capture a verified application or screen region while minimizing sensitive content exposure."
added: "2026-09"
related: [screen-reading, mouse-input, clipboard-ops]
---

# Screenshot Capture (App Region)

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

## Failure Modes

Capturing private data; uncontrolled storage; unverified artifact; excessive capture scope.

## Related

- `screen-reading.md`
- `mouse-input.md`
- `clipboard-ops.md`

## Evidence

- AI_CONSTITUTION.md
- AGENTS.md
- Repository security and validation workflows

## Changelog

| Version | Date | Change |
|---|---|---|
| `v1` | `2026-11` | Title disambiguated per DECISION-2026-11-26-TITLE-UNIQUENESS; capability contract unchanged. |
