# RAG (Retrieval-Augmented Generation)

**Category:** `memory`  
**Skill Level:** `intermediate`  
**Stability:** `stable`
**Added:** 2025-03

### Description

Fetch relevant context from an external knowledge store before generating a response. Reduces hallucinations and grounds outputs in real documents.

### Pipeline

```
1. Embed the user query
2. Search vector store for similar documents
3. Inject retrieved docs into prompt context
4. Generate response grounded in retrieved content
```

### Example

```python
from langchain.chains import RetrievalQA
qa = RetrievalQA.from_chain_type(llm=llm, retriever=vectorstore.as_retriever())
result = qa.run('What is the refund policy?')
```

### Frameworks

- LangChain, LlamaIndex, Haystack
- OpenAI Assistants (file search)
- Cohere RAG

### Related Skills

- [Vector Store Retrieval](vector-store-retrieval.md)
- [Embedding Generation](../12-data/embedding-generation.md)
- [Similarity Search](../12-data/similarity-search.md)
