# Dependency Management

**Category:** `code`  
**Skill Level:** `intermediate`  
**Stability:** `stable`
**Added:** 2025-03

### Description

Install, update, audit, and manage project dependencies across package managers (pip, npm, cargo, etc.).

### Example

```bash
# Python
pip install langchain openai --upgrade
pip freeze > requirements.txt
pip audit  # Security check

# Node
npm install && npm audit fix
```

### Related Skills

- [Dockerfile Generation](dockerfile-generation.md)
- [CI/CD Generation](cicd-generation.md)
- [Security Scanning](security-scanning.md)
