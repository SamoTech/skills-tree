---
title: "Notification Sending"
category: 04-action-execution
level: intermediate
stability: stable
version: v2
description: "Deliver an approved notification through a configured channel with a validated destination, bounded content, and duplicate-delivery protection."
added: "2026-09"
related: [email-sending, assertion, tool-guardrails]
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-04-action-execution-notification-sending.json)

# Notification Sending

**Category:** `action-execution`
**Skill Level:** `intermediate`
**Stability:** `stable`
**Added:** 2026-09

### Description

Deliver an approved notification through a configured channel with a validated destination and content. The destination is matched against an allowlist, the content is bounded and checked for secrets before sending, and delivery is confirmed from the channel response with duplicate protection.

### Inputs / Outputs

| Direction | Field | Type | Contract |
|---|---|---|---|
| Input | `destination` | verified channel address | A recipient on the approved allowlist for the channel |
| Input | `message` | string | Bounded content; scanned for secrets before sending |
| Input | `urgency` | `info\|warning\|critical` | Controls delivery path; only `critical` may page a human |
| Output | `send_result` | `{sent, delivery_id}` | Channel-confirmed outcome with a traceable delivery id |
| Output | `errors` | list of string | Validation failures, before anything is delivered |

### Procedure
1. Validate the destination against the channel's approved allowlist; reject unknown or ambiguous recipients.
2. Bound the message length and scan it for secrets, credentials, and personal data before sending.
3. Classify urgency explicitly; reserve human-paging paths for genuinely critical events.
4. Attach a stable idempotency key so an ambiguous delivery cannot be duplicated by a retry.
5. Send once and confirm from the channel response; treat a timeout as ambiguous and query the delivery id before resending.
6. Record the delivery id with the triggering event so the notification can be audited later.

### Example

```python
import re

SECRET_PATTERN = re.compile(r"(?i)(api[_-]?key|token|password|secret)\s*[:=]\s*\S+")

def build_notification(destination: str, message: str, urgency: str,
                       allowlist: set[str], max_len: int = 2000) -> dict:
    errors = []
    if destination not in allowlist:
        errors.append(f"destination not on allowlist: {destination}")
    if urgency not in {"info", "warning", "critical"}:
        errors.append(f"invalid urgency: {urgency}")
    if len(message) > max_len:
        errors.append("message exceeds length bound")
    if SECRET_PATTERN.search(message):
        errors.append("message contains a potential secret; redact before sending")
    return {"errors": errors, "sendable": not errors,
            "content": message if not errors else None}

check = build_notification(
    "ops@example.com",
    "Nightly backup finished in 12m; 0 failures.",
    "info",
    allowlist={"ops@example.com", "oncall@example.com"},
)
print(check)
```

### Related Skills

- [Email Sending](email-sending.md)
- [Assertion](assertion.md)
- [Tool Guardrails](../07-tool-use/tool-guardrails.md)

## Failure Modes

- Ambiguous destination: a recipient that matches multiple channels or addresses; validate against the allowlist first.
- Sensitive content leakage through the notification body or its metadata.
- Duplicate delivery on retry without an idempotency key.
- Uncontrolled urgency: paging humans for informational events erodes trust in the channel.
- Assuming delivery from a completed request instead of the channel-confirmed response.

## Changelog
- v2 (2026-11): Structural modernization; added the input/output contract table, an explicit procedure, a deterministic validation example with secret scanning, expanded failure modes, and version history.
- v1 (2026-09): Initial entry.

## Evidence

- https://agentskills.io/specification

Evidence status: implementation guidance only; no benchmark claim is made without reproducible evidence.
