---
title: "Keyboard Shortcut"
category: 10-computer-use
level: advanced
stability: stable
version: v2
description: "Execute a specified keyboard shortcut against the verified active application and UI context."
added: "2025-03"
related: [keyboard-type, hotkey-conflict-resolution]
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-10-computer-use-keyboard-shortcut.json)

# Keyboard Shortcut

**Category:** `computer-use`
**Skill Level:** `advanced`
**Stability:** `stable`
**Added:** 2025-03

### Description

Execute a specified keyboard shortcut against the verified active application and UI context. The action is contract-first: verify focus and shortcut scope before sending the chord, and verify the observable effect afterwards rather than trusting the keystroke acknowledgement.

### Inputs / Outputs

| Direction | Field | Type | Contract |
|---|---|---|---|
| Input | shortcut | object | The modifier-plus-key combination in platform-neutral form |
| Input | scope | object | The application and UI context the shortcut applies to |
| Output | result | object | Chord delivery acknowledgement with the focus target used |
| Output | check | object | Verified observable effect of the shortcut or explicit failure |

### Procedure
1. Verify the intended application owns keyboard focus before sending the chord.
2. Check the shortcut is not intercepted by another layer (OS global hotkey, IDE keymap, browser extension).
3. Send the chord with correct modifier order and the active keyboard layout in mind.
4. Re-observe the UI and verify the shortcut's expected effect (dialog opened, pane switched).
5. Stop and report when the effect differs (intercepted, layout mismatch, wrong scope).

### Example

```python
shortcut = {"modifiers": ["ctrl"], "key": "s", "layout": "qwerty"}
focus = {"application": "editor", "focused": True}
assert focus["focused"], "send chord only with verified focus"
interceptors = {"os_global": False, "ide_keymap": False, "extension": False}
assert not any(interceptors.values()), "shortcut would be intercepted"
delivered = {"chord": "ctrl+s", "to": focus["application"]}
effect = {"expected": "save-dialog-or-autosave", "verified": False}
print({"delivered": delivered, "postcondition_verification_required": effect["expected"]})
```

### Related Skills

- [Keyboard Type](keyboard-type.md) - text entry instead of chords
- [Hotkey Conflict Resolution](hotkey-conflict-resolution.md) - resolve intercepted shortcuts
- [Window Management](window-management.md) - ensure the right window has focus

## Failure Modes

- Another application or OS layer intercepts the chord and the target app never sees it.
- A different keyboard layout maps the key to a different character or position.
- A modifier key is stuck from a prior action, turning the chord into an unintended combo.
- The shortcut is scoped to a focused element that does not currently have focus.
- The application's custom keymap overrides the default shortcut binding.

## Changelog
- v2 (2026-11): Structural modernization; added the input/output contract table, a deterministic example, an execution procedure, and corpus-verified related links (replaced the non-corpus input-guardrails/output-guardrails/self-category pointers).
- v1 (2025-03): Initial entry.

## Evidence

- https://agentskills.io/specification

Evidence status: implementation guidance only; no benchmark claim is made without reproducible evidence.
