# Unit Test Generation

**Category:** `code`  
**Skill Level:** `intermediate`  
**Stability:** `stable`

### Description

Automatically generate unit test cases for functions and classes, covering happy paths, edge cases, and error conditions.

### Example

```python
prompt = f"""Write pytest unit tests for this function:\n{source_code}"""
tests = llm.invoke(prompt)
```

### Related Skills

- [Code Generation](code-generation.md)
- [Debugging](debugging.md)
- [Code Review](code-review.md)
