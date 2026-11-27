---
name: similarity-search
description: Retrieve semantically similar items with matched embedding models, declared metrics, thresholds, and returned provenance.
metadata:
  source: skills/12-data/similarity-search.md
  category: 12-data
  version: "v2"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-12-data-similarity-search.json)

# Similarity Search

**Category:** `data`
**Skill Level:** `advanced`
**Stability:** `stable`
**Added:** 2025-03

### Description

Retrieve semantically similar items with matched embedding models, declared metrics, thresholds, and returned provenance. The data step is contract-first: validate the input contract before transforming, and verify the output against explicit expectations rather than trusting the pipeline.

### Inputs / Outputs

| Direction | Field | Type | Contract |
|---|---|---|---|
| Input | query | object | The query text with its embedding model and metric declared |
| Input | index_profile | object | The vector index, its metric (cosine/L2), and top_k |
| Output | matches | list of object | Top-k items with scores from the declared metric |
| Output | search_report | object | Candidates examined, threshold applied, model ids |

### Procedure
1. Embed the query with the same model that built the index.
2. Use the index's declared metric; never mix cosine and L2 scores.
3. Retrieve top-k, then apply the declared relevance threshold.
4. Verify match metadata (ids, sources) is returned with the scores.
5. Report the model, metric, and threshold so results are reproducible.

### Example

```python
import math
q, docs = [1.0, 0.0], [{'id': 'a', 'v': [1.0, 0.0]}, {'id': 'b', 'v': [0.0, 1.0]}]
def cosine(u, v):
    dot = sum(x*y for x, y in zip(u, v))
    return dot / (math.sqrt(sum(x*x for x in u)) * math.sqrt(sum(y*y for y in v)))
scored = sorted(({'id': d['id'], 'score': round(cosine(q, d['v']), 6)} for d in docs), key=lambda m: -m['score'])
assert scored[0]['id'] == 'a' and scored[0]['score'] == 1.0
print(scored)
```

### Related Skills

- [Embedding Generation](embedding-generation.md) - produce the vectors being searched
- [Vector Index Tuning](vector-index-tuning.md) - tune the index for recall and latency
- [Embedding Model Selection](embedding-model-selection.md) - choose one model for index and query

## Failure Modes

- Query embedded with a different model than the index.
- Metric mismatch (cosine vs L2) making scores incomparable.
- No relevance threshold, so irrelevant top-k results surface as matches.
- Match provenance (ids, sources) dropped, making results unverifiable.

## Changelog
- v2 (2026-11): Structural modernization; added the input/output contract table, a skill-specific execution procedure, a deterministic example, and corpus-verified related links (replaced the unresolvable cross-category related references).
- v1 (2025-03): Initial entry.

## Evidence

- https://agentskills.io/specification

Evidence status: implementation guidance only; runtime behavior must be checked against the executing pipeline's documentation; no benchmark claim is made without reproducible evidence.
