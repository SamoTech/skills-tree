# Refactoring

**Category:** `code`  
**Skill Level:** `intermediate`  
**Stability:** `stable`

### Description

Restructure existing code to improve readability, maintainability, and performance without changing its external behavior.

### Example

```python
# Before
def p(x):
    r = []
    for i in x:
        if i > 0:
            r.append(i * 2)
    return r

# After (refactored)
def double_positives(numbers: list[int]) -> list[int]:
    return [n * 2 for n in numbers if n > 0]
```

### Related Skills

- [Code Review](code-review.md)
- [Linting & Formatting](linting-formatting.md)
