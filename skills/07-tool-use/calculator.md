# Calculator

**Category:** `tool-use`  
**Skill Level:** `basic`  
**Stability:** `stable`

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
