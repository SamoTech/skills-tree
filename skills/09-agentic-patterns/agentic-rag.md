---
title: "Agentic RAG"
category: 09-agentic-patterns
level: advanced
stability: stable
description: "Use an agentic retrieval loop that decides whether to retrieve, what to retrieve, when to re-retrieve, and when evidence is sufficient."
related: [03-memory/rag, 09-agentic-patterns/react, 01-perception/document-parsing]
added: "2025-03"
version: v2
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-09-agentic-patterns-agentic-rag.json)

# Agentic RAG

## Description

Agentic retrieval extends ordinary RAG with an explicit control loop. The agent decides whether retrieval is necessary, selects a bounded query strategy, evaluates returned evidence, and stops when the evidence threshold is satisfied or the retrieval budget is exhausted.

## When to Use

Use when a fixed retrieve-once pipeline cannot reliably determine the right query, source, or number of retrieval iterations. Do not use an agentic loop when deterministic retrieval is sufficient; extra iterations add latency and failure surface.

## Inputs / Outputs

Input: a user task, retrieval interface, source policy, evidence threshold, and hard iteration/token budget. Output: an answer plan or answer supported by retrieved evidence plus a trace of retrieval decisions and unresolved uncertainty.

## Example

```python
MAX_ITERATIONS = 3


def retrieval_loop(task, retrieve, sufficient):
    evidence = []
    for iteration in range(MAX_ITERATIONS):
        query = task if iteration == 0 else f"clarify: {task}"
        batch = retrieve(query)
        evidence.extend(batch)
        if sufficient(evidence):
            return {"evidence": evidence, "iterations": iteration + 1, "complete": True}
    return {"evidence": evidence, "iterations": MAX_ITERATIONS, "complete": False}
```

## Failure Modes

- Retrieval budget exhausted: return the best supported result with an explicit incompleteness signal.
- Conflicting sources: preserve the conflict rather than selecting a preferred claim without justification.
- Empty retrieval: do not infer that no evidence exists; distinguish no result from no source.
- Query drift: constrain each re-query to the original task and documented retrieval policy.
- Prompt injection in retrieved content: treat retrieved text as untrusted data, not as control instructions.

## Output Contract

The result must distinguish retrieved evidence from generated interpretation. Every material claim should be traceable to one or more retrieved items when the task requires evidence. The loop must expose whether it stopped because evidence was sufficient, the budget was exhausted, or retrieval failed.

## Design Rules

Bound iterations, tokens, and retrieval fan-out. Preserve provenance and source identity. Keep retrieval content outside the instruction channel. Prefer deterministic stopping criteria over subjective loop continuation.

## Related Skills

- `03-memory/rag`
- `09-agentic-patterns/react`
- `01-perception/document-parsing`

## Changelog

- v2 (2026-09): normalized frontmatter and replaced generic guidance with a bounded retrieval-loop contract.
