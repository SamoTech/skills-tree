---
title: "Secret Scanning"
category: 14-security
level: advanced
stability: stable
description: "Apply secret scanning in AI agent workflows."
added: "2025-03"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-14-security-secret-scanning.json)

**Category:** Security
**Skill Level:** `advanced`
**Stability:** stable
**Added:** 2026-04

### Description
Detects secrets, credentials, and sensitive data patterns in code, configs, agent outputs, and tool results before they propagate to storage or external systems. Integrates with pre-commit hooks and CI pipelines.

### Example
```python
import re

SECRET_PATTERNS = {
    "aws_key":      r"AKIA[0-9A-Z]{16}",
    "github_token": r"ghp_[A-Za-z0-9]{36}",
    "private_key":  r"-----BEGIN (RSA |EC )?PRIVATE KEY-----",
    "generic_api":  r"(?i)(api_key|apikey|secret)[\s=:]+[\w\-]{20,}",
}

def scan(text: str) -> list[dict]:
    findings = []
    for name, pattern in SECRET_PATTERNS.items():
        for match in re.finditer(pattern, text):
            findings.append({"type": name, "match": match.group(0)[:20] + "..."})
    return findings

test = "export AWS_KEY=AKIAIOSFODNN7EXAMPLE  # TODO: remove"
print(scan(test))
```

### Related Skills
- [Audit Logging](audit-logging.md)
- [Input Sanitization](input-sanitization.md)
