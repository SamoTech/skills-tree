---
title: "File Dialog"
category: 10-computer-use
level: advanced
stability: stable
version: v2
description: "Navigate and operate a file chooser with explicit path, selection, and confirmation boundaries."
added: "2025-03"
related: [desktop-file-organization, window-management]
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-10-computer-use-file-dialog.json)

# File Dialog

**Category:** `computer-use`
**Skill Level:** `advanced`
**Stability:** `stable`
**Added:** 2025-03

### Description

Navigate and operate a file chooser with explicit path, selection, and confirmation boundaries. Destructive outcomes (overwrite, delete) inside the dialog are gated on explicit approval before confirmation.

### Inputs / Outputs

| Direction | Field | Type | Contract |
|---|---|---|---|
| Input | path | object | The explicit target path to select or type into the dialog |
| Input | intent | object | Open vs save, and whether an overwrite confirmation is acceptable |
| Output | selection | object | The dialog state after navigation (selected path, enabled buttons) |
| Output | check | object | Verified dialog outcome or an explicit failure/escalation |

### Procedure
1. Identify the dialog type (native vs application-custom) and its confirmation model.
2. Navigate to the declared path by typing it explicitly rather than trusting autocomplete.
3. Verify the selected path shown by the dialog matches the declared path exactly.
4. On overwrite or replace prompts, stop and require explicit approval before confirming.
5. Verify the dialog outcome (file opened/saved) and report the verified path.

### Example

```python
dialog = {"type": "native-save", "path": "/home/user/reports/q3-summary.pdf"}
typed_path = "/home/user/reports/q3-summary.pdf"
assert typed_path == dialog["path"], "autocomplete must not replace the declared path"
overwrite_prompt = {"shown": True, "existing_file": "q3-summary.pdf"}
if overwrite_prompt["shown"]:
    decision = "escalate-for-approval"  # never auto-confirm overwrite
assert decision == "escalate-for-approval"
print({"dialog": dialog["type"], "path_verified": True, "overwrite": decision})
```

### Related Skills

- [Desktop File Organization](desktop-file-organization.md) - keep the target paths organized
- [Window Management](window-management.md) - bring the dialog into focus
- [Approval Before Destructive Tools](../14-security/approval-before-destructive-tools.md) - gate overwrite confirmations

## Failure Modes

- An autocomplete or recent-files entry silently replaces the declared path.
- An overwrite confirmation is accepted without explicit approval.
- A custom (non-native) dialog is driven with native-dialog assumptions and stalls.
- Keyboard shortcuts differ across OS dialogs and trigger the wrong action.
- The dialog loses focus and typed input lands in the underlying application.

## Changelog
- v2 (2026-11): Structural modernization; added the input/output contract table, a deterministic example, an execution procedure, and corpus-verified related links (replaced the non-corpus input-guardrails/output-guardrails/self-category pointers).
- v1 (2025-03): Initial entry.

## Evidence

- https://agentskills.io/specification

Evidence status: implementation guidance only; no benchmark claim is made without reproducible evidence.
