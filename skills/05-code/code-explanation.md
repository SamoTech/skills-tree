# Code Explanation

**Category:** `code`  
**Skill Level:** `basic`  
**Stability:** `stable`
**Added:** 2025-03

### Description

Explain what a piece of code does in plain language — line by line, function by function, or at a high level.

### Example

```python
code = '''
def fib(n):
    return n if n <= 1 else fib(n-1) + fib(n-2)
'''
prompt = f'Explain what this Python function does:\n{code}'
explanation = llm.invoke(prompt)
```

### Related Skills

- [Code Review](code-review.md)
- [Documentation Generation](documentation-generation.md)
- [Debugging](debugging.md)
