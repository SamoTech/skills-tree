# Code Review

**Category:** `code`  
**Skill Level:** `intermediate`  
**Stability:** `stable`
**Added:** 2025-03

### Description

Review code for bugs, security issues, style violations, performance problems, and best practice adherence.

### Example

```python
prompt = f"""Review this code diff and identify: bugs, security risks, performance issues, and style problems.\n```diff\n{diff}\n```"""
review = llm.invoke(prompt)
```

### Frameworks

- GitHub Copilot Code Review
- CodeRabbit
- Any LLM via prompting

### Related Skills

- [Security Vulnerability Scanning](security-scanning.md)
- [Refactoring](refactoring.md)
- [Unit Test Generation](unit-test-generation.md)
