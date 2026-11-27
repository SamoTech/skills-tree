---
title: "Keyboard Type"
category: 10-computer-use
level: advanced
stability: stable
version: v2
description: "Enter supplied text into a verified focused UI field while preserving intended content and handling sensitive data safely."
added: "2025-03"
related: [keyboard-shortcut, clipboard-automation-hygiene]
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-10-computer-use-keyboard-type.json)

# Keyboard Type

**Category:** `computer-use`
**Skill Level:** `advanced`
**Stability:** `stable`
**Added:** 2025-03

### Description

Enter supplied text into a verified focused UI field while preserving intended content and handling sensitive data safely. The entry is contract-first: verify the focused field before typing, keep the keystroke rate within what the field accepts, and verify the field content afterwards rather than trusting the typing acknowledgement.

### Inputs / Outputs

| Direction | Field | Type | Contract |
|---|---|---|---|
| Input | text | object | The exact text to enter, with sensitive segments flagged |
| Input | field | object | The verified focused field identity and its input constraints |
| Output | result | object | Typing acknowledgement with the field target used |
| Output | check | object | Verified field content (read-back) or explicit failure |

### Procedure
1. Verify the intended field has focus and is empty or in the declared state before typing.
2. Type the text at a rate the field accepts; prefer clipboard paste for large or exact-match content.
3. Route sensitive segments so they are not echoed to logs or command lines.
4. Read back the field content and compare against the declared text.
5. Stop and report mismatches (autocorrect, IME rewrite, truncation) rather than re-typing blind.

### Example

```python
entry = {"text": "invoice-2026-0118", "sensitive_segments": [], "via": "clipboard-paste"}
field = {"id": "invoice-number", "focused": True, "max_len": 32}
assert field["focused"], "type only into a verified focused field"
assert len(entry["text"]) <= field["max_len"], "text exceeds field capacity"
read_back = "invoice-2026-0118"
assert read_back == entry["text"], "field content differs from declared text (autocorrect/IME?)"
print({"typed": True, "field": field["id"], "read_back_verified": True})
```

### Related Skills

- [Keyboard Shortcut](keyboard-shortcut.md) - chords instead of text
- [Clipboard Automation Hygiene](clipboard-automation-hygiene.md) - clear sensitive content after paste
- [Input Sanitization](../14-security/input-sanitization.md) - treat typed content as untrusted downstream

## Failure Modes

- Focus moves mid-typing (dialog, notification) and the remainder lands in another field.
- IME, autocorrect, or input masks rewrite the entered text silently.
- The keystroke rate exceeds what the field or remote session accepts and characters drop.
- Sensitive text is echoed into logs, command lines, or screen recordings.
- The field's placeholder or pre-filled value is mistaken for the entered content.

## Changelog
- v2 (2026-11): Structural modernization; added the input/output contract table, a deterministic example, an execution procedure, and corpus-verified related links (replaced the non-corpus input-guardrails/output-guardrails/self-category pointers).
- v1 (2025-03): Initial entry.

## Evidence

- https://agentskills.io/specification

Evidence status: implementation guidance only; no benchmark claim is made without reproducible evidence.
