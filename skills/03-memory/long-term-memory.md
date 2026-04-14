---
title: "Long-Term Memory"
category: 03-memory
level: intermediate
stability: stable
added: "2025-03"
description: "Apply long term memory in AI agent workflows."
---


![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-03-memory-long-term-memory.json)

# Long-Term Memory

### Description
Persists agent knowledge, learned preferences, and distilled insights across sessions and deployments. Long-term memory is durable (survives restarts), structured (organized for efficient retrieval), and self-maintaining (entries are updated, merged, or expired over time). Implemented via databases, file systems, or managed memory services like Mem0 or Zep.

### When to Use
- Remembering user preferences, goals, and constraints across many sessions
- Accumulating domain expertise from tool outcomes over time (learning agents)
- Persisting agent-generated knowledge distillations (summaries, rules, heuristics)
- Cross-agent knowledge sharing in multi-agent systems

### Example
```python type:illustrative
# pip install mem0ai
# Note: `mem0` is the import name for PyPI package `mem0ai`
from mem0 import Memory

m = Memory()

# Store preference from interaction
m.add("User prefers concise bullet-point summaries over long paragraphs.",
      user_id="user_42", metadata={"category": "communication_style"})

# Before responding, retrieve relevant long-term memories
relevant = m.search("How should I format my response?", user_id="user_42", limit=5)
for mem in relevant:
    print(f"[{mem['score']:.2f}] {mem['memory']}")

# Update when preferences change
m.update(mem_id=relevant[0]["id"], data="User now prefers detailed explanations with examples.")
```

### Advanced Techniques
- **Memory distillation**: run nightly summarization jobs that compress episodic memories into semantic facts
- **Contradiction resolution**: before upserting, check semantic similarity to existing memories; merge or flag conflicts
- **Tiered storage**: hot memories in Redis, warm in PostgreSQL + pgvector, cold in S3 + re-embed on access
- **Memory audit trails**: store the source (which interaction, which tool output) for every memory entry

### Related Skills
- `episodic-memory`, `semantic-memory`, `working-memory`, `memory-augmented`, `rag`
