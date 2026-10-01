---
title: "Secret Scanning"
category: 14-security
level: advanced
stability: stable
description: "Detect credentials and secret-like material before it reaches source control, logs, prompts, artifacts, or external systems, with validation and remediation controls."
added: "2025-03"
updated: "2026-10"
version: v2
---

# Secret Scanning

## Description

Secret scanning detects API keys, access tokens, private keys, passwords, and other credential material before it propagates through an agent system. Pattern matching is useful for fast detection, but production controls should combine provider-aware detectors, validation, push protection, and incident response.

Never store a real secret in a skill example or test fixture.

## Inputs / Outputs

| Input | Type | Required | Description |
|---|---|---:|---|
| `text` | string | yes | Content to scan |
| `patterns` | mapping | no | Custom patterns in addition to provider detectors |
| `context` | dict | no | File/source metadata used for policy |

| Output | Type | Description |
|---|---|---|
| `findings` | list | Secret type and location metadata without exposing the secret |
| `blocked` | bool | Whether policy requires stopping the operation |
| `remediation` | list[str] | Actions such as revoke, rotate, or remove |

## Runnable Example

```python
import re

PATTERNS = {
    "private_key": re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    "github_like_token": re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{20,}\b"),
    "generic_assignment": re.compile(r"(?i)\b(api[_-]?key|secret|password)\s*[:=]\s*['\"][^'\"]{12,}"),
}

def scan(text: str) -> list[dict[str, str]]:
    findings = []
    for kind, pattern in PATTERNS.items():
        for match in pattern.finditer(text):
            findings.append({"type": kind, "offset": str(match.start())})
    return findings

print(scan("api_key='THIS_IS_A_FAKE_TEST_VALUE_ONLY'"))
```

The patterns are illustrative and intentionally incomplete. Provider-specific scanners should be preferred where available.

## Failure Modes

| Failure | Cause | Mitigation |
|---|---|---|
| False negative | New or provider-specific token format | Keep detectors updated and use provider validation |
| False positive | Random high-entropy text matches | Use contextual validation and allowlisted test fixtures |
| Secret exposure in findings | Scanner stores the matched value | Store type/location/hash, not the credential |
| Already leaked secret | Detection occurs after publication | Revoke/rotate immediately and remove from affected history |
| Bypass abuse | Developer bypasses push protection | Require documented reason and review for exceptions |
| Secret in generated artifacts | CI only scans source files | Scan generated files and release artifacts too |

## Design Rules

- Scan before commit and again in CI.
- Prefer provider-aware detectors and push protection.
- Never print the matched secret in logs.
- Treat detection as an incident trigger, not proof that the credential is harmless.
- Rotate/revoke exposed credentials before cleanup work.
- Keep test fixtures obviously synthetic.

## References

- GitHub Secret Security documentation: https://docs.github.com/en/code-security/reference/secret-security
- GitHub push protection: https://docs.github.com/en/code-security/how-tos/secure-your-secrets/prevent-future-leaks/enable-push-protection
- OWASP Secrets Management Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html

Evidence status: current GitHub documentation confirms secret scanning and push-protection behavior; no claim is made that regex-only scanning is complete.

## Related Skills

- [Privacy Preservation](privacy-preservation.md)
- [Audit Logging](audit-logging.md)
- [Input Sanitization](input-sanitization.md)
