# Security Scanning

**Category:** `code`  
**Skill Level:** `advanced`  
**Stability:** `stable`

### Description

Scan code, dependencies, and configurations for security vulnerabilities, exposed secrets, and known CVEs.

### Example

```bash
# Python
bandit -r src/ -ll
safety check

# Node
npm audit --audit-level=high

# Secrets
trufflehog filesystem ./
```

### Related Skills

- [Secret Scanning](../14-security/secret-scanning.md)
- [Dependency Management](dependency-management.md)
- [Linting & Formatting](linting-formatting.md)
