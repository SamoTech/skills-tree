![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-06-communication-question-answering.json)

# Question Answering

**Category:** `communication`  
**Skill Level:** `basic`  
**Stability:** `stable`
**Added:** 2025-03

### Description

Answer questions accurately and concisely based on provided context, retrieved knowledge, or world knowledge.

### Example

```python
context = load_document('skills-tree/README.md')
question = 'How many skill categories does the skills-tree have?'
prompt = f'Context:\n{context}\n\nQuestion: {question}'
answer = llm.invoke(prompt)
```

### Related Skills

- [Summarization](summarization.md)
- [RAG](../03-memory/rag.md)
