# Working Memory

**Category:** `memory`  
**Skill Level:** `basic`  
**Stability:** `stable`

### Description

Maintain active context within a single conversation or task session using the model's context window as temporary storage.

### Example

```python
# LangChain conversation buffer
from langchain.memory import ConversationBufferMemory
memory = ConversationBufferMemory()
memory.save_context({'input': 'My name is Ossama'}, {'output': 'Hello Ossama!'})
print(memory.load_memory_variables({}))
```

### Related Skills

- [Episodic Memory](episodic-memory.md)
- [Memory Summarization](memory-summarization.md)
