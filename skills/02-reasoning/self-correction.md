# Self-Correction

**Category:** `reasoning`  
**Skill Level:** `intermediate`  
**Stability:** `stable`

### Description

Iteratively identify and fix errors in generated outputs — code bugs, factual mistakes, logical inconsistencies.

### Example

```python
for attempt in range(3):
    result = agent.run(task)
    check = agent.verify(result)
    if check['passed']:
        break
    task = f"Fix this error: {check['error']}\n\nPrevious attempt:\n{result}"
```

### Related Skills

- [Self-Reflection](self-reflection.md)
- [Debugging](../05-code/debugging.md)
