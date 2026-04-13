---
title: "Debugging"
category: 05-code
level: intermediate
stability: stable
description: "Apply debugging in AI agent workflows."
added: "2025-03"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-05-code-debugging.json)

# Debugging

**Category:** `code`  
**Skill Level:** `intermediate`  
**Stability:** `stable`
**Added:** 2025-03

### Description

Identify the root cause of bugs in code by analyzing error messages, stack traces, and code logic — then propose a fix.

### Example

```python
prompt = f"""
This code raises an error:
```python
{buggy_code}
```
Error: {error_message}

Find the bug and provide the fixed code.
"""
```

### Related Skills

- [Code Generation](code-generation.md)
- [Self-Correction](../02-reasoning/self-correction.md)
- [Code Execution (Sandbox)](code-execution-sandbox.md)
