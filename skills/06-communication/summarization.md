# Summarization

**Category:** `communication`  
**Skill Level:** `basic`  
**Stability:** `stable`
**Added:** 2025-03

### Description

Condense long content (articles, documents, conversations) into concise key points while preserving the core meaning.

### Example

```python
prompt = f"""Summarize the following in 3 bullet points:\n{long_text}"""
summary = llm.invoke(prompt)
```

### Related Skills

- [Memory Summarization](../03-memory/memory-summarization.md)
- [Report Writing](report-writing.md)
- [Data Summarization](../12-data/data-summarization.md)
