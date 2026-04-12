**Category:** Security & Safety
**Skill Level:** Intermediate
**Stability:** stable
**Added:** 2025-03

### Description
Cleans and validates all inputs before processing to prevent prompt injection, SQL injection, XSS, path traversal, and shell injection attacks. Applies allowlist validation, encoding, and schema enforcement.

### Example
```python
import re, html, os
from pathlib import Path

def sanitize_prompt_input(user_input: str, max_length: int = 2000) -> str:
    """Block prompt injection attempts."""
    if len(user_input) > max_length:
        raise ValueError(f"Input too long: {len(user_input)} chars (max {max_length})")
    # Strip common injection patterns
    injection_patterns = [
        r"ignore previous instructions",
        r"you are now",
        r"<\|.*?\|>",          # token boundary attacks
        r"\[SYSTEM\]",
    ]
    for pattern in injection_patterns:
        if re.search(pattern, user_input, re.IGNORECASE):
            raise ValueError("Potential prompt injection detected")
    return user_input.strip()

def sanitize_file_path(user_path: str, base_dir: str = "/data") -> Path:
    """Prevent path traversal."""
    resolved = Path(base_dir).joinpath(user_path).resolve()
    if not str(resolved).startswith(str(Path(base_dir).resolve())):
        raise ValueError(f"Path traversal detected: {user_path}")
    return resolved

print(sanitize_prompt_input("What is the weather today?"))
print(sanitize_file_path("reports/q1.csv"))
```

### Related Skills
- [Secret Scanning](secret-scanning.md)
- [Harm Detection](harm-detection.md)
- [Permission Checking](permission-checking.md)
