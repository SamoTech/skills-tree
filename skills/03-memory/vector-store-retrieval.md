![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-03-memory-vector-store-retrieval.json)

# Vector Store Retrieval

**Category:** `memory`  
**Skill Level:** `intermediate`  
**Stability:** `stable`
**Added:** 2025-03

### Description

Store documents as vector embeddings and retrieve the most semantically similar ones at query time.

### Example

```python
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

vectorstore = Chroma.from_documents(docs, OpenAIEmbeddings())
results = vectorstore.similarity_search('refund policy', k=3)
```

### Frameworks

- FAISS, Chroma, Pinecone, Qdrant, Weaviate, pgvector

### Related Skills

- [RAG](rag.md)
- [Similarity Search](../12-data/similarity-search.md)
- [Embedding Generation](../12-data/embedding-generation.md)
