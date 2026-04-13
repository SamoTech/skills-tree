---
title: "Linting & Formatting"
category: 05-code
level: basic
stability: stable
description: "Apply linting & formatting in AI agent workflows."
added: "2025-03"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-05-code-linting-formatting.json)

# Linting & Formatting

**Category:** `code`  
**Skill Level:** `basic`  
**Stability:** `stable`
**Added:** 2025-03

### Description

Run linters and code formatters to enforce style, catch errors, and maintain consistent code quality.

### Example

```bash
# Python
ruff check . --fix
black .
mypy src/

# JavaScript/TypeScript
npx eslint . --fix
npx prettier --write .
```

### Related Skills

- [Code Review](code-review.md)
- [CI/CD Generation](cicd-generation.md)
