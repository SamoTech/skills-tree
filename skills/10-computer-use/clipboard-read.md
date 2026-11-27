---
title: "Clipboard Read"
category: 10-computer-use
level: advanced
stability: stable
version: v2
description: "Read clipboard contents from an authorized computer-use session and preserve their type and provenance."
added: "2025-03"
related: [clipboard-write, clipboard-automation-hygiene]
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-10-computer-use-clipboard-read.json)

# Clipboard Read

**Category:** `computer-use`
**Skill Level:** `advanced`
**Stability:** `stable`
**Added:** 2025-03

### Description

Read clipboard contents from an authorized computer-use session and preserve their type and provenance. Clipboard data is untrusted input: capture its format and source session, and validate it before any downstream use.

### Inputs / Outputs

| Direction | Field | Type | Contract |
|---|---|---|---|
| Input | session | object | The authorized computer-use session to read from |
| Input | expected | object | The expected content type (text, image, file list) and bounds |
| Output | content | object | The clipboard payload with its actual format recorded |
| Output | check | object | Format and bounds verification result |

### Procedure
1. Confirm the target session is the authorized one and the read is permitted.
2. Read the clipboard and record the actual content type alongside the expected type.
3. Validate the payload against the declared bounds (size, type, encoding).
4. Treat the content as untrusted data; sanitize before injecting into prompts or commands.
5. Report the payload with its format and provenance, or an explicit mismatch failure.

### Example

```python
clip = {"session": "workstation-7", "format": "text/plain", "data": "INV-2026-0118", "bytes": 13}
expected = {"format": "text/plain", "max_bytes": 1024}
assert clip["session"] == "workstation-7", "read from unauthorized session"
assert clip["format"] == expected["format"], "clipboard format mismatch"
assert clip["bytes"] <= expected["max_bytes"], "payload exceeds declared bounds"
print({"read": True, "format": clip["format"], "sanitized_before_use": True})
```

### Related Skills

- [Clipboard Write](clipboard-write.md) - the matching write path
- [Clipboard Automation Hygiene](clipboard-automation-hygiene.md) - avoid cross-session leakage
- [Input Sanitization](../14-security/input-sanitization.md) - treat clipboard content as untrusted

## Failure Modes

- Reading from a session other than the authorized one (cross-session clipboard leakage).
- The actual content type differs from the expected type and is used unchecked.
- Sensitive clipboard content is echoed into logs or prompts.
- Format coercion (rich text to plain text) silently drops or alters payload.
- The read races a concurrent write and returns partial content.

## Changelog
- v2 (2026-11): Structural modernization; added the input/output contract table, a deterministic example, an execution procedure, and corpus-verified related links (replaced the non-corpus input-guardrails/output-guardrails/self-category pointers).
- v1 (2025-03): Initial entry.

## Evidence

- https://agentskills.io/specification

Evidence status: implementation guidance only; no benchmark claim is made without reproducible evidence.
