# Similarity Search

**Category:** `data`  
**Skill Level:** `intermediate`  
**Stability:** `stable`
**Added:** 2025-03

### Description

Find the most semantically similar items to a query using vector embeddings and approximate nearest-neighbor (ANN) algorithms.

### Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `query` | `string` | ✅ | Query text or vector |
| `top_k` | `int` | ❌ | Number of results to return (default: 5) |
| `index` | `VectorStore` | ✅ | Pre-built vector index to search |

### Outputs

| Output | Type | Description |
|---|---|---|
| `results` | `list[dict]` | Top-K matches with scores and metadata |

### Example

```python
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings()
vectorstore = FAISS.load_local('my_index', embeddings)

results = vectorstore.similarity_search('How do I reset my password?', k=5)
for doc in results:
    print(doc.page_content)
```

### Frameworks / Models

- **LangChain** — `vectorstore.similarity_search()`
- **FAISS** — Meta's fast ANN library
- **Pinecone** — Managed vector database
- **Weaviate** — Open-source vector DB
- **Qdrant** — High-performance vector search
- **Chroma** — Local-first vector store
- **pgvector** — Vector search inside PostgreSQL

### Notes

- Distance metrics: cosine similarity, dot product, Euclidean (L2)
- For large indexes (>1M vectors), use HNSW or IVF indexing for speed
- Hybrid search (keyword + vector) improves precision for many use cases

### Related Skills

- [Embedding Generation](embedding-generation.md)
- [RAG](../03-memory/rag.md)
- [Vector DB Tool](../07-tool-use/vector-db-tool.md)
