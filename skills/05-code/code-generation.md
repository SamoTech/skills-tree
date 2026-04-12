# Code Generation

**Category:** `code`  
**Skill Level:** `basic`  
**Stability:** `stable`
**Added:** 2025-03

### Description

Generate working code in any programming language from a natural language description.

### Example

```python
prompt = "Write a Python function that takes a list of dicts and returns them sorted by 'date' key descending."
code = llm.invoke(prompt)
# def sort_by_date(items):
#     return sorted(items, key=lambda x: x['date'], reverse=True)
```

### Frameworks / Models

- GPT-4o, Claude 3.7, Gemini 2.5 Pro
- GitHub Copilot
- DeepSeek Coder, Qwen Coder
- Codestral (Mistral)

### Related Skills

- [Code Explanation](code-explanation.md)
- [Debugging](debugging.md)
- [Unit Test Generation](unit-test-generation.md)
