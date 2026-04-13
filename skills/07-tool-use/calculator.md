---
title: "Calculator"
category: 07-tool-use
level: basic
stability: stable
description: "Apply calculator in AI agent workflows."
added: "2025-03"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-07-tool-use-calculator.json)

# Calculator

**Category:** `tool-use`  
**Skill Level:** `basic`  
**Stability:** `stable`
**Added:** 2025-03

### Description

Perform precise arithmetic, symbolic math, and unit conversions — bypassing LLM floating-point errors by calling a real calculator or math engine.

### Example

```python
# Using Python as calculator tool
def calculate(expression: str) -> float:
    import ast
    return eval(ast.parse(expression, mode='eval').body)

# Or use Wolfram Alpha API for symbolic math
result = calculate('(2 ** 32) / 1024')
```

### Related Skills

- [Wolfram API](wolfram-api.md)
- [Mathematical Reasoning](../02-reasoning/mathematical-reasoning.md)
