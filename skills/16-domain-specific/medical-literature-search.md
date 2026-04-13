---
title: "Medical Literature Search"
category: 16-domain-specific
level: advanced
stability: stable
description: "Apply medical literature search in AI agent workflows."
added: "2025-03"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-16-domain-specific-medical-literature-search.json)

**Category:** Domain-Specific
**Skill Level:** `advanced`
**Stability:** stable
**Added:** 2026-04

### Description
Searches biomedical databases such as PubMed, Semantic Scholar, and ClinicalTrials.gov using domain-aware query expansion, MeSH term mapping, and evidence-tier filtering. Results are ranked by recency and citation count, then summarized with methodology and conclusion extraction.

### Example
```python
from Bio import Entrez

Entrez.email = "agent@example.com"

def pubmed_search(query: str, max_results: int = 5) -> list[str]:
    handle = Entrez.esearch(db="pubmed", term=query, retmax=max_results, sort="relevance")
    record = Entrez.read(handle)
    ids = record["IdList"]
    handle = Entrez.efetch(db="pubmed", id=ids, rettype="abstract", retmode="text")
    return handle.read().split("\n\n")

results = pubmed_search("glioblastoma immunotherapy 2025")
for r in results[:2]:
    print(r[:300])
```

### Related Skills
- [Paper Summarization](paper-summarization.md)
- [Web Search](../11-web/web-search.md)
- [RAG](../03-memory/rag.md)
- [Citation Attribution](../06-communication/citation-attribution.md)
