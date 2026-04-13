---
title: "Summarization"
category: 06-communication
level: intermediate
stability: stable
description: "Apply summarization in AI agent workflows."
---


![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-06-communication-summarization.json)

# Summarization

### Description
Condenses long documents, conversations, or multi-document corpora into concise, accurate summaries at adjustable levels of detail. Supports extractive (sentence selection), abstractive (generative), hierarchical (chunk-then-summarize), and query-focused summarization. Handles documents longer than the context window via map-reduce or refine strategies.

### When to Use
- Condensing meeting transcripts, research papers, legal documents, or code reviews
- Building executive summaries from large corpora with preserved citations
- Preprocessing documents before injecting into RAG pipelines
- Generating changelog summaries from Git diffs or PR descriptions

### Example
```python
from langchain_openai import ChatOpenAI
from langchain.chains.summarize import load_summarize_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

def summarize_long_document(text: str, style: str = "bullet points") -> str:
    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    splitter = RecursiveCharacterTextSplitter(chunk_size=4000, chunk_overlap=200)
    chunks = splitter.create_documents([text])

    chain = load_summarize_chain(
        llm, chain_type="map_reduce",
        map_prompt=f"Summarize the following in {style}. Be concise:\n\n{{text}}",
        combine_prompt=f"Combine these partial summaries into one coherent {style} summary:\n\n{{text}}"
    )
    return chain.invoke({"input_documents": chunks})["output_text"]

# Multi-document summarization with source attribution
def multi_doc_summary(docs: list[str], query: str = None) -> str:
    llm = ChatOpenAI(model="gpt-4o")
    prompt = f"Synthesize the following documents" + (f" focusing on: {query}" if query else "") + ":\n\n"
    prompt += "\n\n---\n\n".join(f"[Doc {i+1}]: {d[:3000]}" for i, d in enumerate(docs))
    return llm.invoke(prompt).content
```

### Advanced Techniques
- **Hierarchical summarization**: recursively summarize chunks, then summarize summaries for very long documents
- **Query-focused**: inject the user's question into the map prompt to bias toward relevant content
- **Faithfulness scoring**: use `BERTScore` or `FactCC` to verify summary claims against source
- **Incremental summarization**: maintain a running summary updated as new content arrives (streaming)

### Related Skills
- `text-reading`, `rag`, `meeting-summary`, `document-parsing`, `report-writing`
