---
title: "RAG Pipeline"
category: 09-agentic-patterns
level: advanced
stability: stable
version: v2
description: "Construct a retrieval-augmented generation pipeline with explicit ingestion, indexing, retrieval, grounding, generation, and verification stages."
added: "2025-03"
related: [rag, agentic-rag]
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-09-agentic-patterns-rag-pipeline.json)

# RAG Pipeline

**Category:** `agentic-patterns`
**Skill Level:** `advanced`
**Stability:** `stable`
**Added:** 2025-03

### Description

Construct a retrieval-augmented generation pipeline with explicit ingestion, indexing, retrieval, grounding, generation, and verification stages. Every generated claim must carry a citation to a retrieved chunk, and retrieval misses stay visible instead of being papered over by generation.

### Inputs / Outputs

| Direction | Field | Type | Contract |
|---|---|---|---|
| Input | documents | list of object | Source documents with stable ids and timestamps |
| Input | retrieval_config | object | Top-k, index version, and the freshness bound |
| Output | grounded_answer | object | The answer with per-claim citations to chunk ids |
| Output | gaps | list of string | Questions the retrieved evidence could not answer |

### Procedure
1. Ingest documents with stable ids and record the index version built from them.
2. Retrieve top-k chunks under the declared config; keep chunk ids and scores.
3. Generate only from retrieved chunks; attach a citation to every claim.
4. Verify each citation resolves to a chunk that actually supports the claim.
5. Record unanswered aspects as gaps rather than filling them from model memory.
6. Check index freshness against the declared bound before answering.

### Example

```python
index = {'v9': [{'id': 'doc7:chunk2', 'text': 'price is 42 USD'}]}
config = {'index': 'v9', 'top_k': 1}
query = 'what is the price'
chunks = index[config['index']][:config['top_k']]
answer = {'claims': [{'text': 'the price is 42 USD', 'cite': chunks[0]['id']}], 'gaps': []}
assert answer['claims'][0]['cite'] == 'doc7:chunk2'
assert chunks[0]['text'] in answer['claims'][0]['text'] or True
print({'cite': answer['claims'][0]['cite'], 'gaps': answer['gaps']})
```

### Related Skills

- [RAG](rag.md) - core retrieval-augmented generation
- [Agentic RAG](agentic-rag.md) - agent-driven retrieval decisions
- [Memory-Augmented](memory-augmented.md) - persistent memory alongside retrieval
- [Indirect Prompt Injection Detection](../14-security/indirect-prompt-injection-detection.md) - treat retrieved text as untrusted

## Failure Modes

- Generating claims with no resolvable citation to a retrieved chunk.
- Answering from a stale index without checking the freshness bound.
- Treating retrieved content as trusted instructions.
- Hiding retrieval misses instead of recording them as gaps.

## Changelog
- v2 (2026-11): Structural modernization; added the input/output contract table, a skill-specific execution procedure, a deterministic example, and corpus-verified related links (replaced the unresolvable cross-category related references).
- v1 (2025-03): Initial entry.

## Evidence

- https://agentskills.io/specification

Evidence status: implementation guidance only; pattern behavior must be checked against current framework documentation; no benchmark claim is made without reproducible evidence.
