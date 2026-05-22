---
title: "Fact Verification Memory"
category: 03-memory
level: advanced
stability: stable
tags: [memory, fact-checking, grounding, cache, hallucination]
description: "Maintain a persistent cache of verified and refuted facts to prevent re-checking and ground future reasoning in confirmed truths."
added: "2025-03"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-03-memory-fact-verification-memory.json)

# Fact Verification Memory

**Category:** `memory`  
**Skill Level:** `advanced`  
**Stability:** `stable`  
**Added:** 2025-03

---

## Description

Fact verification memory is a specialized knowledge cache that records claims the agent has already verified (or disproved), along with the evidence and source that supported the verdict. Its primary purpose is to eliminate duplicate verification work and to give downstream reasoning a stable, auditable ground truth to build on.

Without this pattern, an agent may verify the same claim repeatedly across sessions, reach inconsistent conclusions due to different retrieved context, or silently build further reasoning on an unverified premise. The cache acts as a fact ledger — it doesn't prevent the agent from re-examining a claim, but it makes the prior verdict and evidence immediately available.

---

## When to Use

- Research agents that verify multiple claims over a long session or across sessions
- Any agent that calls external APIs or search tools to check facts — these are expensive; caching avoids redundant calls
- Multi-agent pipelines where one specialist agent verifies facts for others to consume
- QA systems that need explainability: "Why do you believe X?" → cite the stored evidence

---

## Data Model

```python
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Literal, Optional


@dataclass
class FactRecord:
    claim: str                                  # normalized claim text
    verdict: Literal["true", "false", "uncertain"]
    confidence: float                           # 0.0 – 1.0
    source: Optional[str] = None               # URL, document ID, or tool name
    evidence: Optional[str] = None             # supporting excerpt
    verified_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    expires_at: Optional[str] = None           # ISO timestamp; None = no expiry
```

---

## Implementation Pattern

```python
import hashlib
from typing import Optional


class FactMemory:
    """In-process fact cache. Swap `_store` for Redis or a DB in production."""

    def __init__(self):
        self._store: dict[str, FactRecord] = {}

    @staticmethod
    def _key(claim: str) -> str:
        """Normalise and hash the claim to produce a stable lookup key."""
        normalised = " ".join(claim.lower().split())
        return hashlib.sha256(normalised.encode()).hexdigest()[:16]

    def store(self, record: FactRecord) -> None:
        self._store[self._key(record.claim)] = record

    def lookup(self, claim: str) -> Optional[FactRecord]:
        rec = self._store.get(self._key(claim))
        if rec is None:
            return None
        # Honour TTL if set
        if rec.expires_at:
            from datetime import datetime, timezone
            if datetime.now(timezone.utc).isoformat() > rec.expires_at:
                del self._store[self._key(claim)]
                return None
        return rec

    def is_known(self, claim: str) -> bool:
        return self.lookup(claim) is not None

    def verdict(self, claim: str) -> Optional[str]:
        rec = self.lookup(claim)
        return rec.verdict if rec else None
```

### Agent integration

```python
fact_memory = FactMemory()

def verify(claim: str) -> FactRecord:
    # 1. Check cache first
    cached = fact_memory.lookup(claim)
    if cached:
        return cached

    # 2. Run expensive verification (web search, tool call, etc.)
    result = run_external_verifier(claim)   # your implementation

    record = FactRecord(
        claim=claim,
        verdict=result["verdict"],
        confidence=result["confidence"],
        source=result["source"],
        evidence=result["snippet"],
    )
    fact_memory.store(record)
    return record
```

---

## Claim Normalisation

The same fact can be stated many ways: "Paris is the capital of France", "France's capital is Paris", "the capital city of France is Paris". Normalisation is the hard part. Strategies:

1. **Lowercasing + stopword removal** — cheap but misses paraphrase
2. **Entity extraction** — extract subject/predicate/object triples; match on canonical form
3. **Embedding similarity** — encode claim, check cosine similarity against stored claim embeddings; retrieve if above threshold (e.g. > 0.92)
4. **Hybrid** — exact hash as primary key, embedding fallback for near-duplicate detection

For most agentic use cases, option 3 or 4 gives the best recall.

---

## Pitfalls

- **Stale facts**: Real-world truth changes. Always set `expires_at` on time-sensitive facts (news, prices, software versions). Use a short TTL (hours to days) for rapidly changing domains.
- **False confidence**: A high-confidence cached verdict may have come from a flawed source. Store the source so it can be audited or invalidated.
- **Poisoning**: If the verifier can be manipulated (e.g. via prompt injection in retrieved content), an attacker can persist false facts. Validate sources before writing to the cache.
- **Over-specificity**: Caching "The CEO of Acme Corp is Alice" at a specific timestamp avoids polluting reasoning with stale authority. Always include `verified_at`.

---

## Related Skills

- [Semantic Memory](semantic-memory.md)
- [Fact Verification](fact-verification.md)
- [Self-Correction](../02-reasoning/self-correction.md)
- [RAG](rag.md)
