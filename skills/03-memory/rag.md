---
title: "Retrieval-Augmented Generation (RAG)"
category: 03-memory
level: intermediate
stability: stable
added: "2025-03"
description: "Apply rag in AI agent workflows."
---


![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-03-memory-rag.json)

# Retrieval-Augmented Generation (RAG)

### Description
Augments LLM generation by retrieving relevant context from external knowledge stores at inference time. A full RAG pipeline includes document ingestion, chunking, embedding, indexing, query-time retrieval, reranking, and context-aware generation. Advanced variants include HyDE (Hypothetical Document Embeddings), multi-query RAG, and corrective RAG (CRAG).

### When to Use
- Reducing hallucination on factual queries by grounding responses in retrieved evidence
- Enabling LLMs to answer questions over private, proprietary, or recently updated corpora
- Building citation-backed answer systems where source attribution is required
- Combining structured (SQL) and unstructured (vector) retrieval in hybrid pipelines

### Example
```python
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import RetrievalQA
from langchain_community.document_loaders import DirectoryLoader

def build_rag_chain(docs_dir: str) -> RetrievalQA:
    loader = DirectoryLoader(docs_dir, glob="**/*.md")
    docs = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=64)
    chunks = splitter.split_documents(docs)
    vectorstore = Chroma.from_documents(chunks, OpenAIEmbeddings(model="text-embedding-3-large"))
    retriever = vectorstore.as_retriever(search_type="mmr", search_kwargs={"k": 8, "fetch_k": 30})
    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    return RetrievalQA.from_chain_type(llm=llm, retriever=retriever, return_source_documents=True)

chain = build_rag_chain("./docs")
result = chain.invoke({"query": "What are the rate limits for the API?"})
print(result["result"])
for doc in result["source_documents"]:
    print(f"  Source: {doc.metadata['source']}")
```

### Advanced Techniques
- **HyDE**: generate a hypothetical answer, embed it, use it as the query vector for better retrieval
- **Multi-query**: generate 3-5 paraphrased queries, merge retrieved sets via RRF
- **Cross-encoder reranking**: use `cross-encoder/ms-marco-MiniLM-L-12-v2` to rerank top-20 → top-5
- **CRAG**: after retrieval, score relevance; if below threshold, fall back to web search
- **Contextual compression**: extract only the relevant sentences from each chunk before generation

### Related Skills
- `semantic-memory`, `agentic-rag`, `embedding-generation`, `similarity-search`, `rag-pipeline`
