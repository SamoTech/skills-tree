# Memory Summarization

**Category:** `memory`  
**Skill Level:** `intermediate`  
**Stability:** `stable`
**Added:** 2025-03

### Description

Compress long conversation history or event logs into concise summaries to stay within context window limits while preserving key information.

### Example

```python
from langchain.memory import ConversationSummaryMemory
memory = ConversationSummaryMemory(llm=llm)
```

### Related Skills

- [Working Memory](working-memory.md)
- [Summarization](../06-communication/summarization.md)
