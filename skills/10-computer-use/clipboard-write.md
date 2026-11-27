---
title: "Clipboard Write"
category: 10-computer-use
level: advanced
stability: stable
version: v2
description: "Write explicitly supplied content to the clipboard for a subsequent authorized computer-use step."
added: "2025-03"
related: [clipboard-read, clipboard-automation-hygiene]
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-10-computer-use-clipboard-write.json)

# Clipboard Write

**Category:** `computer-use`
**Skill Level:** `advanced`
**Stability:** `stable`
**Added:** 2025-03

### Description

Write explicitly supplied content to the clipboard for a subsequent authorized computer-use step. The write is contract-first: confirm the session, write the exact declared content and format, and verify the round-trip before the consuming step runs.

### Inputs / Outputs

| Direction | Field | Type | Contract |
|---|---|---|---|
| Input | content | object | The exact payload to write, with its format and size declared |
| Input | session | object | The authorized computer-use session to write to |
| Output | ack | object | Write acknowledgement with the format actually written |
| Output | check | object | Round-trip verification result (read-back equals written content) |

### Procedure
1. Confirm the target session is the authorized one and the write is permitted.
2. Write the exact declared content in the declared format; no silent transformations.
3. Read back and compare against the declared payload to verify the round trip.
4. Plan the cleanup: sensitive content must be cleared from the clipboard after the consuming step.
5. Report the verified write, or an explicit failure (permission denied, format unsupported).

### Example

```python
payload = {"format": "text/plain", "data": "release-notes-v2 draft text", "bytes": 24}
write_ack = {"session": "workstation-7", "format_written": payload["format"]}
read_back = {"format": "text/plain", "data": "release-notes-v2 draft text", "bytes": 24}
assert write_ack["session"] == "workstation-7", "write to unauthorized session"
assert read_back == payload, "clipboard round-trip mismatch"
print({"written": True, "round_trip_verified": True, "cleanup_planned": True})
```

### Related Skills

- [Clipboard Read](clipboard-read.md) - verify the round trip
- [Clipboard Automation Hygiene](clipboard-automation-hygiene.md) - clear sensitive content afterwards
- [Tool Guardrails](../07-tool-use/tool-guardrails.md) - keep the write within declared bounds

## Failure Modes

- The session or application denies clipboard write permission.
- Content is truncated or re-encoded so the read-back differs from the declared payload.
- The consuming step pastes before the write lands (race) and reads stale content.
- Sensitive content is left on the clipboard after the step completes.
- The write targets a remote session whose clipboard is disabled or redirected.

## Changelog
- v2 (2026-11): Structural modernization; added the input/output contract table, a deterministic example, an execution procedure, and corpus-verified related links (replaced the non-corpus input-guardrails/output-guardrails/self-category pointers).
- v1 (2025-03): Initial entry.

## Evidence

- https://agentskills.io/specification

Evidence status: implementation guidance only; no benchmark claim is made without reproducible evidence.
