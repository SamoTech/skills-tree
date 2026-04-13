---
title: "Paper Summarization"
category: 16-domain-specific
level: advanced
stability: stable
description: "Apply paper summarization in AI agent workflows."
added: "2025-03"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-16-domain-specific-paper-summarization.json)

**Category:** Domain-Specific
**Skill Level:** `advanced`
**Stability:** stable
**Added:** 2026-04

### Description
Condenses academic papers into structured summaries covering research problem, methodology, key findings, limitations, and future work. Supports both single-paper deep dives and bulk pipeline summarisation for literature review automation.

### Example
```python
import anthropic, json

client = anthropic.Anthropic()

def summarise_paper(abstract: str, full_text: str = "") -> dict:
    content = abstract if not full_text else f"{abstract}\n\n{full_text[:3000]}"
    prompt = (
        "Summarise this paper as JSON: {problem, method, key_findings, "
        "limitations, future_work, one_sentence_tldr}.\n\n" + content
    )
    resp = client.messages.create(
        model="claude-opus-4-5", max_tokens=700,
        messages=[{"role": "user", "content": prompt}]
    )
    return json.loads(resp.content[0].text)

abstract = "We propose a retrieval-augmented code generation pipeline that improves "\
           "pass@1 on HumanEval by 8.4% over standard fine-tuning baselines."
print(summarise_paper(abstract))
```

### Related Skills
- [Literature Review](literature-review.md)
- [RAG](../03-memory/rag.md)
- [Summarization](../06-communication/summarization.md)
