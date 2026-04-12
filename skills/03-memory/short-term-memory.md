---
Category: Memory
Skill Level: Advanced
Stability: Stable
Tags: [short-term-memory, context-window, sliding-window, summarization-buffer]
---

# Short-Term Memory

### Description
Manages information within a single agent invocation or conversation session. Operates within the LLM context window using sliding window buffers, summarization compression, and token-budget management to maintain coherence without exceeding limits.

### When to Use
- Multi-turn conversations where recent history must inform the next response
- Agentic loops where intermediate tool results must be tracked across steps
- Long conversations exceeding the context window that require intelligent compression

### Example
```python
from langchain.memory import ConversationSummaryBufferMemory
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini")
memory = ConversationSummaryBufferMemory(
    llm=llm, max_token_limit=2000,
    return_messages=True, memory_key="chat_history"
)

def chat(user_input: str) -> str:
    memory.chat_memory.add_user_message(user_input)
    history = memory.load_memory_variables({})["chat_history"]
    r = llm.invoke(history + [{"role": "user", "content": user_input}])
    memory.chat_memory.add_ai_message(r.content)
    return r.content
```

### Advanced Techniques
- **Token-aware truncation**: use `tiktoken` to measure exact token count and truncate oldest messages first
- **Importance scoring**: keep high-importance messages (decisions, errors, tool results) even under compression
- **KV-cache optimization**: structure prompts so the system prefix is always the same to maximize KV-cache hits

### Related Skills
- `episodic-memory`, `working-memory`, `long-term-memory`, `summarization`
