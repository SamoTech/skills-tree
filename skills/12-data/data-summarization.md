---
title: "Data Summarization"
category: 12-data
level: intermediate
stability: stable
description: "Apply data summarization in AI agent workflows."
added: "2025-03"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-12-data-data-summarization.json)

# Data Summarization

**Category:** `data`  
**Skill Level:** `intermediate`  
**Stability:** `stable`
**Added:** 2025-03

### Description

Produce a natural language summary of a dataset's contents, distributions, trends, and notable patterns.

### Example

```python
prompt = f"""Here is a dataset:\n{df.to_markdown()}\n
Summarize the key trends, outliers, and insights in 3 bullet points."""
response = llm.invoke(prompt)
```

### Frameworks

- Any LLM with data-to-text prompting
- LangChain `PandasDataFrameAgent`
- OpenAI Code Interpreter

### Related Skills

- [Statistical Analysis](statistical-analysis.md)
- [Data Visualization](data-visualization.md)
