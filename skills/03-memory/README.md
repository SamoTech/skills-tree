![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-03-memory-README.json)

# 🧠 Memory Skills

Memory skills enable agents to **store, retrieve, and reason over information** across turns, sessions, and tasks.

## Memory Types

```
Memory
├── In-Context (Working Memory)
│   ├── Conversation history
│   ├── Scratchpad / chain of thought
│   └── Tool call results
├── External Memory
│   ├── Vector stores (semantic search)
│   ├── Key-value stores (exact lookup)
│   ├── Relational databases
│   └── Document stores
└── Parametric Memory
    └── Knowledge baked into model weights
```

## Skills in This Category

| Skill | Level | Description |
|---|---|---|
| [Working Memory](working-memory.md) | Basic | Maintain context within a conversation |
| [Short-Term Memory](short-term-memory.md) | Intermediate | Manage information within a single session using sliding windows and summarization |
| [Long-Term Memory](long-term-memory.md) | Intermediate | Persist knowledge, preferences, and insights across sessions and deployments |
| [Episodic Memory](episodic-memory.md) | Intermediate | Remember past interactions and events |
| [Semantic Memory](semantic-memory.md) | Intermediate | Store and retrieve factual knowledge |
| [Procedural Memory](procedural-memory.md) | Advanced | Learn and recall how to do tasks |
| [Procedural](procedural.md) | Intermediate | Store, retrieve, and execute step-by-step procedures and recurring workflows |
| [Vector Store Retrieval](vector-store-retrieval.md) | Intermediate | Semantic similarity search over embeddings |
| [RAG (Retrieval-Augmented Generation)](rag.md) | Intermediate | Fetch relevant context before generating |
| [Memory Summarization](memory-summarization.md) | Intermediate | Compress long history into summaries |
| [Memory Injection](memory-injection.md) | Intermediate | Inject retrieved memories into prompts |
| [Forgetting / Pruning](forgetting.md) | Advanced | Remove outdated or irrelevant memories |
| [Cross-Session Persistence](cross-session-persistence.md) | Advanced | Persist memory across separate sessions |
| [User Profile Memory](user-profile-memory.md) | Intermediate | Store user preferences and context |
| [User Profile](user-profile.md) | Intermediate | Build and query a structured user profile to personalize responses |
| [Fact Verification Memory](fact-verification-memory.md) | Advanced | Store verified facts to avoid hallucinations |
| [Fact Verification](fact-verification.md) | Advanced | Verify factual claims against authoritative sources; classify as verified, contradicted, or uncertain |
