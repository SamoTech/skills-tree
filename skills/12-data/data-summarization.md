# Data Summarization

**Category:** `data`  
**Skill Level:** `intermediate`  
**Stability:** `stable`

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
