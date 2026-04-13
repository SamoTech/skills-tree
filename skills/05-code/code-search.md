---
title: "Code Search"
category: 05-code
level: intermediate
stability: stable
description: "Apply code search in AI agent workflows."
added: "2025-03"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-05-code-code-search.json)

# Code Search

**Category:** `code`  
**Skill Level:** `intermediate`  
**Stability:** `stable`
**Added:** 2025-03

### Description

Search through a codebase by keyword, symbol, regex, or semantic meaning to find relevant files, functions, or usages.

### Example

```bash
# ripgrep semantic search
rg 'def train' --type py

# GitHub code search
gh api search/code?q=skill+repo:SamoTech/skills-tree
```

### Related Skills

- [Code Reading](../01-perception/code-reading.md)
- [Refactoring](refactoring.md)
