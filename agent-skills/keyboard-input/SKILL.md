---
name: keyboard-input
description: Send bounded keyboard input to a verified target while controlling focus, protecting sensitive text, and avoiding destructive shortcuts.
metadata:
  source: skills/04-action-execution/keyboard-input.md
  category: 04-action-execution
  version: "v2"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-04-action-execution-keyboard-input.json)

# Keyboard Input

**Category:** `action-execution`
**Skill Level:** `intermediate`
**Stability:** `stable`
**Added:** 2026-09

### Description

Send bounded keyboard input to a verified target while controlling focus and sensitive text. Input is delivered only to a target whose focus is confirmed, length is bounded before typing, and destructive key sequences are never sent without explicit authorization.

### Inputs / Outputs

| Direction | Field | Type | Contract |
|---|---|---|---|
| Input | `target` | verified element locator | The element that receives input; focus checked first |
| Input | `text` | string | The payload; length-bounded before delivery |
| Input | `sensitive` | boolean | When true, the text is masked in all logs and errors |
| Output | `input_result` | `{typed, verified}` | Whether input was delivered and the field content confirmed |
| Output | `failure` | string or `None` | The specific failure when verification does not hold |

### Procedure
1. Resolve the target and confirm it is visible, enabled, and focused before typing; click or focus it explicitly if it is not.
2. Bound the input length before delivery and reject oversized payloads instead of truncating silently.
3. Never send destructive shortcuts (Ctrl+W, Ctrl+Q, Escape in unsaved dialogs) unless the action is explicitly authorized.
4. Treat sensitive text as masked: exclude it from logs, screenshots, and error reports.
5. Verify the result by reading back the field value or the resulting state, not by assuming the keystrokes landed.
6. Prefer element fill APIs that set content atomically over character-by-character typing when timing fidelity is not required.

### Example

```python
def type_bounded(target, text: str, sensitive: bool = False, limit: int = 2000) -> dict:
    if len(text) > limit:
        raise ValueError(f"input too long: {len(text)} > {limit}")
    if not target.is_enabled():
        raise RuntimeError("target is not enabled")
    target.click()
    target.fill(text)
    verified = target.input_value() == text
    return {"typed": True, "verified": verified,
            "failure": None if verified else "field content mismatch",
            "logged": "***" if sensitive else text}

# usage in a browser session: type_bounded(page.get_by_role("textbox", name="Email"), "user@example.com")
```

### Related Skills

- [Mouse Input](mouse-input.md)
- [Clipboard Operations](clipboard-ops.md)
- [Screenshot Capture](screenshot-capture.md)

## Failure Modes

- Typing into the wrong target because focus was assumed instead of checked.
- Destructive shortcuts delivered to an unauthorized surface.
- Sensitive keystrokes captured in logs, traces, or screenshots.
- Unbounded input: oversized payloads submitted without a length check.
- Verifying success by absence of errors instead of by reading back the field state.

## Changelog
- v2 (2026-11): Structural modernization; added the input/output contract table, an explicit procedure, a deterministic bounded-input example, expanded failure modes, and version history.
- v1 (2026-09): Initial entry.

## Evidence

- https://agentskills.io/specification

Evidence status: implementation guidance only; no benchmark claim is made without reproducible evidence.
