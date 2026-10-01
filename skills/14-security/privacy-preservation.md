---
title: "Privacy Preservation"
category: 14-security
level: advanced
stability: stable
description: "Minimize, detect, and redact sensitive personal data before agent inputs, outputs, logs, storage, or external transmission."
added: "2025-03"
updated: "2026-10"
version: v2
---

# Privacy Preservation

## Description

Privacy preservation reduces unnecessary collection and propagation of personal or sensitive information through an agent system. Apply data minimization first, then detect and transform sensitive values at explicit trust boundaries.

Pattern matching is useful for known formats but is incomplete. Production systems should combine deterministic detection with domain-specific validation, access controls, retention rules, and appropriate privacy governance.

## Inputs / Outputs

| Input | Type | Required | Description |
|---|---|---:|---|
| `text` | string | yes | Content to inspect |
| `patterns` | mapping | yes | Named detection patterns |
| `replacement` | string | no | Redaction marker |
| `context` | dict | no | Minimal policy context |

| Output | Type | Description |
|---|---|---:|---|
| `redacted` | string | Sanitized content |
| `types` | list[str] | Detected data classes |
| `count` | int | Number of replacements |

## Runnable Example

```python
import re

PATTERNS = {
    "email": re.compile(r"\b[\w.+-]+@[\w-]+(?:\.[\w-]+)+\b"),
    "phone": re.compile(r"\b\+?[0-9][0-9 .()-]{7,}[0-9]\b"),
}

def redact(text: str) -> tuple[str, list[str]]:
    found = []
    for kind, pattern in PATTERNS.items():
        if pattern.search(text):
            found.append(kind)
            text = pattern.sub(f"[REDACTED:{kind}]", text)
    return text, found

print(redact("Contact example@example.com or +20 100 000 0000"))
```

The example uses deliberately generic test data. It is not a complete PII detector.

## Failure Modes

| Failure | Cause | Mitigation |
|---|---|---|
| Missed PII | Format is not covered by a regex | Add domain-aware detectors and test representative samples |
| Over-redaction | Pattern is too broad | Use validation and context before replacing |
| Sensitive logs | Original input is copied before redaction | Redact before logging and before external transmission |
| Re-identification | Several harmless fields combine into identity | Apply data minimization and access controls |
| Unicode bypass | Normalization differences | Normalize consistently before detection |
| Retention leak | Redacted output retained indefinitely | Apply explicit retention and deletion policy |

## Design Rules

- Collect only what the task requires.
- Redact before crossing a trust boundary.
- Never assume a regex provides complete privacy protection.
- Keep detection results free of the sensitive values they describe.
- Define retention, access, and deletion policies.
- Test international formats where relevant.

## References

- NIST Privacy Framework: https://www.nist.gov/privacy-framework
- OWASP Secrets Management Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html

Evidence status: references support privacy and secret-handling practices; no legal compliance determination is implied.

## Related Skills

- [Secret Scanning](secret-scanning.md)
- [Input Sanitization](input-sanitization.md)
- [Audit Logging](audit-logging.md)
