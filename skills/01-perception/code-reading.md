# Code Reading

**Category:** `perception`  
**Skill Level:** `intermediate`  
**Stability:** `stable`
**Added:** 2025-03

### Description

Read, parse, and understand source code files across programming languages — identifying functions, classes, imports, and logic flow.

### Example

```python
import ast
tree = ast.parse(open('script.py').read())
for node in ast.walk(tree):
    if isinstance(node, ast.FunctionDef):
        print(node.name)
```

### Related Skills

- [Code Explanation](../05-code/code-explanation.md)
- [Code Review](../05-code/code-review.md)
- [Code Search](../05-code/code-search.md)
