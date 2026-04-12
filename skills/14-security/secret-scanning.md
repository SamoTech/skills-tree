**Category:** Security & Safety
**Skill Level:** Intermediate
**Stability:** stable
**Added:** 2025-03

### Description
Detects hardcoded secrets — API keys, passwords, private keys, tokens — in source code, configuration files, and agent outputs using pattern matching (regex) and entropy analysis. Integrates with pre-commit hooks or CI pipelines.

### Example
```python
import re

SECRET_PATTERNS = [
    ("AWS Access Key",      r"AKIA[0-9A-Z]{16}"),
    ("GitHub Token",        r"ghp_[A-Za-z0-9]{36}"),
    ("OpenAI Key",          r"sk-[A-Za-z0-9]{48}"),
    ("Generic Password",    r"(?i)password\s*=\s*['\"][^'\"]{8,}['\"]"),
    ("Private Key Header",  r"-----BEGIN (RSA |EC )?PRIVATE KEY-----"),
]

def scan_for_secrets(text: str) -> list[dict]:
    findings = []
    for name, pattern in SECRET_PATTERNS:
        for match in re.finditer(pattern, text):
            findings.append({
                "type": name,
                "match": match.group()[:20] + "...",
                "position": match.start(),
            })
    return findings

sample_code = """
api_key = 'sk-abcdefghijklmnopqrstuvwxyz1234567890abcdefghijkl'
AWS_KEY = 'AKIAIOSFODNN7EXAMPLE'
"""

for finding in scan_for_secrets(sample_code):
    print(f"[{finding['type']}] at pos {finding['position']}: {finding['match']}")
```

### Related Skills
- [Input Sanitization](input-sanitization.md)
- [Audit Logging](audit-logging.md)
- [Permission Checking](permission-checking.md)
