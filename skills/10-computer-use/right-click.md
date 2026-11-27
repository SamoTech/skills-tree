---
title: "Right Click"
category: 10-computer-use
level: advanced
stability: stable
version: v2
description: "Perform a context click on a verified UI target and inspect the resulting context menu."
added: "2025-03"
related: [mouse-click, double-click]
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-10-computer-use-right-click.json)

# Right Click

**Category:** `computer-use`
**Skill Level:** `advanced`
**Stability:** `stable`
**Added:** 2025-03

### Description

Perform a context click on a verified UI target and inspect the resulting context menu. The action is contract-first: verify the target and the menu it should produce, read the menu items before selecting, and treat menu-driven actions as separate gated steps.

### Inputs / Outputs

| Direction | Field | Type | Contract |
|---|---|---|---|
| Input | target | object | Verified UI target that owns a context menu |
| Input | intended_item | object | The menu item to select, with destructive items flagged |
| Output | menu | object | The observed context menu items actually rendered |
| Output | check | object | Verified menu outcome or explicit escalation for destructive items |

### Procedure
1. Verify the target and its context-menu semantics before the click.
2. Perform the context click and capture the menu that actually renders.
3. Read the menu items and match the intended item against the observed text (localization-aware).
4. Require explicit approval before selecting destructive menu items (delete, replace, send).
5. Verify the postcondition of the selected action; close stray menus on failure.

### Example

```python
click = {"capability": "right-click", "target": {"strategy": "semantic", "identifier": "doc-row-7"}}
menu = {"items": ["Open", "Rename", "Copy path", "Delete"]}
intended = {"item": "Delete", "destructive": True}
assert intended["item"] in menu["items"], "intended menu item not rendered"
if intended["destructive"]:
    selection = "escalate-for-approval"  # never auto-select destructive items
assert selection == "escalate-for-approval"
print({"menu_verified": True, "intended": intended["item"], "selection": selection})
```

### Related Skills

- [Mouse Click](mouse-click.md) - primary-button click path
- [Double Click](double-click.md) - the other multi-state click
- [Approval Before Destructive Tools](../14-security/approval-before-destructive-tools.md) - gate destructive menu items

## Failure Modes

- The context menu renders off-screen or clipped and menu items cannot be read reliably.
- A custom menu needs a hover delay first; an immediate click closes it or opens the wrong one.
- The target suppresses or replaces the context menu (browser default menu appears instead).
- Menu item text is localized or dynamic and no longer matches the intended label.
- Focus loss or a stray click dismisses the menu between observation and selection.

## Changelog
- v2 (2026-11): Structural modernization; added the input/output contract table, a deterministic example, an execution procedure, and corpus-verified related links (replaced the non-corpus input-guardrails/output-guardrails/self-category pointers).
- v1 (2025-03): Initial entry.

## Evidence

- https://agentskills.io/specification

Evidence status: implementation guidance only; no benchmark claim is made without reproducible evidence.
