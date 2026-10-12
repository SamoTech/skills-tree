---
title: "Memory Indexing"
category: 03-memory
level: intermediate
stability: experimental
description: "Index stored memories for retrieval — keyword, inverted, and vector structures — with stated ranking, measured recall, and maintenance against index drift."
added: "2026-10"
version: v1
related: ["vector-store-retrieval", "semantic-memory"]
---

# Memory Indexing

Category: Memory | Level: intermediate | Stability: experimental | Version: v1

## Description

An agent's memory is only as good as its retrieval, and retrieval is only as fast as its index. This skill covers choosing and building the right structure for the query mix — exact keyword lookups, full-text search, similarity search — measuring recall against the corpus, and maintaining the index as memories are written, updated, and expired rather than letting it drift from the store.

## When to Use

Use when the memory store grows beyond a scan-all lookup and queries must select a bounded subset — long-term memory, knowledge bases, session archives.

Do not trust an index without measuring it; a silently degraded index returns plausible-but-wrong memories.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `corpus` | `list` | Yes | Stored memory records with fields |
| `query_mix` | `map` | Yes | Expected query types and frequency |
| `budget` | `map` | No | Latency and memory limits for the index |

## Procedure

1. Characterize the query mix before choosing the structure — exact lookups need inverted indexes, fuzzy recall needs vector or trigram structures.
2. Build the index on the corpus fields queries actually filter on, not every field available.
3. Measure recall against a labeled query set: what the index returns versus what a full scan would return.
4. Keep the index updated in the same transaction as the store, or run a stated reconciliation sweep for the gap.
5. Record index metadata — build time, size, last reconciliation — so drift is observable.
6. Rebuild from the corpus when drift exceeds a stated bound instead of patching forward.

## Outputs

| Output | Type | Description |
|---|---|---|
| `index` | `map` | The built index with its structure and fields |
| `recall` | `map` | Measured recall against the labeled query set |
| `stats` | `map` | Index size, build time, and last reconciliation |

## Runnable Example

```python
def build_inverted_index(records):
    index = {}
    for r in records:
        for word in set(r["text"].lower().split()):
            index.setdefault(word, []).append(r["id"])
    return index

def search(index, query, limit=5):
    hits = {}
    for word in query.lower().split():
        for rid in index.get(word, []):
            hits[rid] = hits.get(rid, 0) + 1
    ranked = sorted(hits.items(), key=lambda kv: -kv[1])
    return ranked[:limit]

corpus = [
    {"id": "m1", "text": "user prefers terse replies"},
    {"id": "m2", "text": "user asked about invoice format"},
]
print(search(build_inverted_index(corpus), "terse replies"))
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Silent drift | The index diverges from the store | Reconcile on a schedule and measure the gap |
| Unmeasured recall | Nobody knows what retrieval misses | Measure recall against a labeled query set |
| Wrong structure | Vector search for exact lookups or scans for fuzzy recall | Match the index to the query mix |
| Unbounded growth | Deleted and expired entries linger in the index | Remove index entries in the same transaction as deletes |
| Hidden ranking | Result order is unexplained | State the ranking signal per query type |

## Security and Authority Boundary

Indexes leak corpus content in their structures — term lists, embeddings, and summaries are readable from the index itself. Apply the same access control to the index as to the records, and never build shared indexes across principals with different visibility.

## Evidence

This skill is grounded in dated public implementation references:

1. The SQLite FTS5 full-text search extension documentation (https://www.sqlite.org/fts5.html).
2. Wikipedia's overview of full-text search structures (https://en.wikipedia.org/wiki/Full-text_search).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Vector Store Retrieval](vector-store-retrieval.md) — the similarity-search counterpart to keyword indexing.
- [Semantic Memory](semantic-memory.md) — the durable store whose records this skill indexes.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
