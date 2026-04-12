# Code Translation

**Category:** `code`  
**Skill Level:** `intermediate`  
**Stability:** `stable`
**Added:** 2025-03

### Description

Translate code from one programming language to another while preserving logic and idioms.

### Example

```python
prompt = '''
Translate this Python function to TypeScript:

def greet(name: str) -> str:
    return f"Hello, {name}!"
'''
ts_code = llm.invoke(prompt)
```

### Related Skills

- [Code Generation](code-generation.md)
- [Code Explanation](code-explanation.md)
