# Vector DB Tool

**Category:** `tool-use`  
**Skill Level:** `intermediate`  
**Stability:** `stable`
**Added:** 2025-03

### Description

Perform semantic search and document storage operations against a vector database as an agent tool.

### Example

```python
import chromadb

client = chromadb.Client()
collection = client.get_or_create_collection("docs")

# Upsert documents
collection.upsert(
    documents=["LangChain is a framework for LLM apps."],
    ids=["doc-1"]
)

# Semantic search
results = collection.query(query_texts=["LLM frameworks"], n_results=3)
print(results["documents"])
```

### Supported Databases

| Database | Type | Notes |
|---|---|---|
| Pinecone | Managed | Fast, scalable |
| Qdrant | Self-hosted/Managed | Rust-based, high performance |
| Weaviate | Self-hosted/Managed | GraphQL interface |
| Chroma | Local | Great for development |
| FAISS | Local library | Meta's ANN library |
| pgvector | PostgreSQL extension | SQL + vectors |

### Related Skills

- [Similarity Search](../12-data/similarity-search.md)
- [Embedding Generation](../12-data/embedding-generation.md)
- [RAG](../03-memory/rag.md)
