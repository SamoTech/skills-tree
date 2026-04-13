![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-12-data-embedding-generation.json)

# Embedding Generation

**Category:** `data`  
**Skill Level:** `intermediate`  
**Stability:** `stable`
**Added:** 2025-03

### Description

Convert text, images, or other data into dense vector representations (embeddings) for semantic search, clustering, and classification.

### Example

```python
from openai import OpenAI
client = OpenAI()
response = client.embeddings.create(
    input='The capital of Egypt is Cairo.',
    model='text-embedding-3-small'
)
vector = response.data[0].embedding  # 1536-dim float list
```

### Frameworks

- OpenAI `text-embedding-3-small` / `text-embedding-3-large`
- Cohere Embed v3
- HuggingFace `sentence-transformers`
- Google `text-embedding-004`

### Related Skills

- [Similarity Search](similarity-search.md)
- [Vector DB Tool](../07-tool-use/vector-db-tool.md)
- [RAG](../03-memory/rag.md)
