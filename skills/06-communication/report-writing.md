# Report Writing

**Category:** `communication`  
**Skill Level:** `intermediate`  
**Stability:** `stable`

### Description

Compose structured, well-organized reports with executive summaries, findings, analysis, and recommendations.

### Example

```python
prompt = '''
Write a technical report on the following findings:
- 223 skill files were missing from the repository
- All files have been added in 9 batched commits
- Repository now contains 292+ documented skills

Include: summary, impact, actions taken, next steps.
'''
report = llm.invoke(prompt)
```

### Related Skills

- [Summarization](summarization.md)
- [Argument Construction](argument-construction.md)
