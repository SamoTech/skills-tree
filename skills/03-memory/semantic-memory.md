---
title: "Semantic Memory"
category: 03-memory
level: intermediate
stability: stable
added: "2025-03"
description: "Apply semantic memory in AI agent workflows."
---


![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-03-memory-semantic-memory.json)

# Semantic Memory

### Description
Stores and retrieves factual, conceptual, and relational knowledge independent of specific episodes. Semantic memory powers knowledge bases, domain-specific fact stores, and entity graphs. Implemented via vector databases, knowledge graphs, or hybrid stores combining dense retrieval with sparse keyword matching.

### When to Use
- Grounding agent responses in a private or domain-specific knowledge corpus
- Building knowledge graphs of entities, relations, and attributes for structured reasoning
- Hybrid search combining BM25 keyword matching with dense vector similarity
- Cross-document fact synthesis across large corpora

### Example
```python
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext
from llama_index.vector_stores.qdrant import QdrantVectorStore
from qdrant_client import QdrantClient

def build_semantic_store(docs_path: str, collection: str) -> VectorStoreIndex:
    qdrant = QdrantClient(url="http://localhost:6333")
    store = QdrantVectorStore(client=qdrant, collection_name=collection)
    ctx = StorageContext.from_defaults(vector_store=store)
    docs = SimpleDirectoryReader(docs_path).load_data()
    index = VectorStoreIndex.from_documents(docs, storage_context=ctx, show_progress=True)
    return index

def query_knowledge(index: VectorStoreIndex, question: str, top_k: int = 8) -> str:
    engine = index.as_query_engine(similarity_top_k=top_k, response_mode="tree_summarize")
    return str(engine.query(question))
```

### Advanced Techniques
- **Hybrid BM25 + dense**: use `rank_bm25` + FAISS and RRF (Reciprocal Rank Fusion) to merge results
- **Knowledge graph overlay**: extract (subject, predicate, object) triples with SpanBERT or GPT-4o, store in Neo4j
- **Self-updating store**: on each agent run, extract new facts from tool outputs and upsert into the store
- **Namespace partitioning**: separate collections per domain/user to prevent cross-contamination

### Related Skills
- `episodic-memory`, `rag`, `rag-pipeline`, `agentic-rag`, `embedding-generation`, `similarity-search`
