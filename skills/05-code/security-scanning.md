---
title: "Security Scanning"
category: 05-code
level: advanced
stability: stable
description: "Apply security scanning in AI agent workflows."
added: "2025-03"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-05-code-security-scanning.json)

# Security Scanning

**Category:** `code`  
**Skill Level:** `advanced`  
**Stability:** `stable`
**Added:** 2025-03

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
