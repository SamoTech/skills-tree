---
title: "RAG (Retrieval-Augmented Generation)"
category: 03-memory
level: intermediate
stability: stable
added: "2025-03"
description: "Apply RAG in AI agent workflows."
dependencies:
  - package: langchain
    min_version: "0.2.0"
    tested_version: "1.2.15"
    confidence: verified
  - package: langchain-openai
    min_version: "0.1.0"
    tested_version: "1.1.12"
    confidence: verified
  - package: langchain-community
    min_version: "0.2.0"
    tested_version: "0.4.1"
    confidence: verified
code_blocks:
  - id: "example-rag"
    type: executable
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-03-memory-rag.json)

# RAG (Retrieval-Augmented Generation)

**Category:** `memory`  
**Skill Level:** `intermediate`  
**Stability:** `stable`
**Added:** 2025-03

### Description

Augment LLM responses by retrieving relevant documents from a vector store at query time, grounding answers in external knowledge.

### Example

```python
# pip install langchain langchain-openai langchain-community
from langchain_community.document_loaders import TextLoader
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA

loader = TextLoader("knowledge_base.txt")
docs = loader.load()
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = splitter.split_documents(docs)

embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_documents(chunks, embeddings)
retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

qa_chain = RetrievalQA.from_chain_type(
    llm=ChatOpenAI(model="gpt-4o"),
    retriever=retriever,
    return_source_documents=True
)
result = qa_chain.invoke({"query": "What are the main features?"})
print(result["result"])
```

### Advanced Techniques
- **Hybrid search**: combine dense (vector) + sparse (BM25) retrieval for higher recall
- **Re-ranking**: run a cross-encoder reranker on top-20 results before passing top-4 to LLM
- **Self-query retrieval**: let the LLM generate metadata filters from the question

### Related Skills
- `vector-store-retrieval`, `semantic-memory`, `episodic-memory`, `memory-injection`
