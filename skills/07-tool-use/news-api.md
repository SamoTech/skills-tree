---
title: "News API"
category: 07-tool-use
level: intermediate
stability: stable
version: v2
description: "Query documented news APIs with bounded searches, explicit freshness windows, source metadata, pagination limits, and verified responses."
added: "2026-09"
related: [tool-guardrails, api-pagination, tool-result-caching]
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-07-tool-use-news-api.json)

# News API

**Category:** `tool-use`
**Skill Level:** `intermediate`
**Stability:** `stable`
**Added:** 2026-09

### Description

Query documented news APIs with bounded searches, explicit freshness windows, source metadata, pagination limits, and verified responses. The invocation is contract-first: validate the tool interface and inputs before calling, and verify the observable outcome afterwards rather than trusting acknowledgements.

### Inputs / Outputs

| Direction | Field | Type | Contract |
|---|---|---|---|
| Input | query | object | Search terms with an explicit freshness window and language/region filters |
| Input | limits | object | Page size, max pages, and rate-limit budget |
| Output | articles | list | Deduplicated results with source, date, and URL metadata |
| Output | coverage | object | Window, pages fetched, and any truncation disclosed |

### Procedure
1. Define the search terms, freshness window, and language/region filters before querying.
2. Authenticate with least-privilege credentials managed outside source code.
3. Bound the result set: page size, max pages, and rate-limit budget.
4. Deduplicate by canonical URL and keep source and date metadata per item.
5. Validate the response schema; disclose truncation instead of presenting partial results as complete.
6. Cache raw responses for reproducibility within the freshness window.

### Example

```python
q = {'terms': 'agent skills', 'window_days': 7, 'page_size': 50, 'max_pages': 2}
assert q['window_days'] > 0 and q['max_pages'] > 0
assert q['page_size'] <= 100
print('bounded news query with explicit freshness window')
```

### Related Skills

- [Tool Guardrails](tool-guardrails.md) - invocation boundaries
- [API Pagination](api-pagination.md) - bounded completeness
- [Tool Result Caching](tool-result-caching.md) - reproducible raw responses

## Failure Modes

- Hard-coding credentials or exposing them in logs.
- Unbounded pagination or retries.
- Presenting a truncated result set as complete.
- Dropping source and date metadata needed for verification.

## Changelog
- v2 (2026-11): Structural modernization; added the input/output contract table, a deterministic example, an execution procedure, and corpus-verified related links (replaced the non-corpus input-guardrails/AI_CONSTITUTION.md pointers where present).
- v1 (2026-09): Initial entry.

## Evidence

- https://agentskills.io/specification

Evidence status: implementation guidance only; provider behavior must be checked against current provider documentation; no benchmark claim is made without reproducible evidence.
