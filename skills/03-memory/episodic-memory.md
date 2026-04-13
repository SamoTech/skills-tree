---
title: "Episodic Memory"
category: 03-memory
level: intermediate
stability: stable
description: "Apply episodic memory in AI agent workflows."
---


![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-03-memory-episodic-memory.json)

# Episodic Memory

### Description
Records and retrieves specific past events, interactions, and experiences with temporal context. Episodic memory enables agents to recall what happened, when it happened, and what the outcome was — supporting continuity across sessions, learning from mistakes, and personalization based on interaction history.

### When to Use
- Maintaining conversational continuity across multiple sessions or agent invocations
- Recalling previous tool outcomes to avoid repeating failed approaches
- Building personalized agents that remember user preferences and past interactions
- Debugging agentic runs by inspecting the full event timeline

### Example
```python
from datetime import datetime, timezone
from typing import Any
from qdrant_client import QdrantClient, models
from openai import OpenAI

client = OpenAI()
qdrant = QdrantClient(":memory:")
qdrant.recreate_collection("episodes", vectors_config=models.VectorParams(size=1536, distance=models.Distance.COSINE))

def embed(text: str) -> list[float]:
    return client.embeddings.create(model="text-embedding-3-small", input=text).data[0].embedding

def store_episode(event: str, outcome: Any, session_id: str) -> None:
    text = f"Event: {event}\nOutcome: {outcome}"
    vec = embed(text)
    qdrant.upsert("episodes", points=[models.PointStruct(
        id=int(datetime.now(timezone.utc).timestamp() * 1000),
        vector=vec,
        payload={"event": event, "outcome": str(outcome),
                 "ts": datetime.now(timezone.utc).isoformat(), "session": session_id}
    )])

def recall_similar(query: str, top_k: int = 5) -> list[dict]:
    hits = qdrant.search("episodes", query_vector=embed(query), limit=top_k)
    return [h.payload for h in hits]
```

### Advanced Techniques
- **Temporal decay**: down-weight older episodes using `score * exp(-lambda * age_days)`
- **Episode compression**: periodically summarize clusters of related episodes into abstract memories
- **Contradiction detection**: before storing, check for episodes that contradict the new event and flag for review
- **Multi-granularity**: store raw events + summarized episodes + abstract patterns as separate memory layers

### Related Skills
- `semantic-memory`, `working-memory`, `long-term-memory`, `rag`, `memory-augmented`
