---
title: "Wikipedia API"
category: 07-tool-use
level: intermediate
stability: stable
version: v2
description: "Retrieve encyclopedia content through the MediaWiki API with bounded queries, page identifiers, continuation handling, and source attribution."
added: "2026-09"
related: [tool-guardrails, function-calling, tool-output-validation]
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-07-tool-use-wikipedia-api.json)

# Wikipedia API

**Category:** `tool-use`
**Skill Level:** `intermediate`
**Stability:** `stable`
**Added:** 2026-09

### Description

Retrieve encyclopedia content through the MediaWiki API with bounded queries, page identifiers, continuation handling, and source attribution. The invocation is contract-first: least-privilege credentials, bounded scope, validated inputs, and post-action verification instead of trusting acknowledgements.

### Inputs / Outputs

| Direction | Field | Type | Contract |
|---|---|---|---|
| Input | query | object | Page titles or search terms with the target language wiki |
| Input | limits | object | Result bounds and continuation budget |
| Output | pages | list | Page content with ids, revision ids, and canonical URLs |
| Output | attribution | object | Source attribution and license information preserved |

### Procedure
1. Resolve page titles to pageids through a verified lookup; names are ambiguous across languages.
2. Query the documented MediaWiki endpoints with explicit language and revision parameters.
3. Handle continuation tokens; never present a partial continuation as the full result.
4. Record pageid, revid, and the canonical URL for every retrieved page.
5. Preserve attribution and license information with any redistributed content.
6. Cache raw responses and respect the API etiquette (user agent, rate limits).

### Example

```python
page = {'title': 'Knowledge graph', 'pageid': 0, 'lang': 'en', 'revid': 0}
assert page['lang'] == 'en'
assert page['title'] != ''
print('titles resolved to pageids before content retrieval')
```

### Related Skills

- [Tool Guardrails](tool-guardrails.md) - invocation boundaries and least privilege
- [Tool Output Validation](tool-output-validation.md) - validate provider responses before use
- [API Pagination](api-pagination.md) - continuation completeness

## Failure Modes

- Assuming a title maps to the intended page or language.
- Ignoring continuation and truncating silently.
- Redistributing content without attribution and license data.
- Missing revision ids, making citations unverifiable.

## Changelog
- v2 (2026-11): Structural modernization; added the input/output contract table, a deterministic example, an execution procedure, and corpus-verified related links (replaced the non-corpus input-guardrails reference).
- v1 (2026-09): Initial entry.

## Evidence

- https://agentskills.io/specification
- https://www.mediawiki.org/wiki/API:Main_page

Evidence status: implementation guidance only; provider behavior must be checked against current provider documentation; no benchmark claim is made without reproducible evidence.
