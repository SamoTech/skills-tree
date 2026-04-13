![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-14-security-privacy-preservation.json)

**Category:** Security & Safety
**Skill Level:** Advanced
**Stability:** stable
**Added:** 2025-03

### Description
Detects and redacts Personally Identifiable Information (PII) — names, emails, phone numbers, SSNs, credit card numbers — from inputs and outputs before storage or transmission. Supports both regex-based and LLM-based detection.

### Example
```python
import re

PII_PATTERNS = {
    "email":        r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
    "phone_us":     r"\b(\+1[-.]?)?(\(?\d{3}\)?[-.]?)\d{3}[-.]?\d{4}\b",
    "ssn":          r"\b\d{3}-\d{2}-\d{4}\b",
    "credit_card":  r"\b(?:\d{4}[-\s]?){3}\d{4}\b",
    "ip_address":   r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
}

def redact_pii(text: str, replacement: str = "[REDACTED]") -> tuple[str, list[str]]:
    redacted = text
    found_types = []
    for pii_type, pattern in PII_PATTERNS.items():
        if re.search(pattern, redacted):
            found_types.append(pii_type)
            redacted = re.sub(pattern, replacement, redacted)
    return redacted, found_types

original = "Contact John at john.doe@email.com or 555-123-4567 (SSN: 123-45-6789)"
cleaned, types = redact_pii(original)
print(cleaned)
# Contact John at [REDACTED] or [REDACTED] (SSN: [REDACTED])
print(f"Redacted: {types}")
```

### Related Skills
- [Harm Detection](harm-detection.md)
- [Audit Logging](audit-logging.md)
- [Input Sanitization](input-sanitization.md)
