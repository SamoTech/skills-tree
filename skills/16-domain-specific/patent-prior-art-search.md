---
title: "Patent Prior Art Search"
category: 16-domain-specific
level: advanced
stability: experimental
description: "Search patent and non-patent literature for prior art against a claim set, building a structured evidence file with citations, claim-mapping, and explicit search-coverage disclosure."
added: "2026-10"
version: v1
related: ["legal-research","literature-review"]
---

# Patent Prior Art Search

Category: Domain-Specific | Level: advanced | Stability: experimental | Version: v1

## Description

Prior art search is coverage accounting plus claim mapping. The skill covers decomposing the subject into searchable facets, running parallel queries across patent classifications and non-patent literature, mapping each hit against the claim elements, and disclosing what was searched, where, and with which queries, so a reviewer can judge coverage rather than trust a conclusion. A hit list without claim mapping is a reading list, not prior art.

## When to Use

Use when a product idea, draft application, or existing patent must be checked against what was already published or patented.

Do not present a clean result as proof of novelty. A search is a coverage statement over queries run, not a guarantee that nothing exists.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `disclosure` | `text` | Yes | The invention description or claim set to search against |
| `scope` | `object` | Yes | Jurisdictions, date bounds, and sources to cover |
| `depth` | `enum` | No | `screening` or `claim-mapped` (default) analysis depth |

## Procedure

1. Decompose the disclosure into claim elements and searchable technical facets.
2. Build a query matrix: facet terms across patent classifications and non-patent literature.
3. Run the matrix, logging every query, source, and date for coverage disclosure.
4. Screen hits at title and abstract level; promote relevant ones to full-text review.
5. Map each promoted hit against the claim elements it anticipates or renders obvious.
6. Emit the evidence file with citations, mappings, and the coverage statement.

## Outputs

| Output | Type | Description |
|---|---|---|
| `prior_art_file` | `table` | Hits with citation, relevance, and claim-element mapping |
| `coverage_statement` | `object` | Sources, queries, and dates searched, and known gaps |
| `claim_map` | `table` | Claim elements against the hits that read on them |

## Runnable Example

```python
def map_claim_elements(elements, hits):
    """elements: [text]; hits: {id: [matched elements]}"""
    unmapped = [e for e in elements if not any(e in ms for ms in hits.values())]
    return {"mapped": len(elements) - len(unmapped), "unmapped": unmapped}

print(map_claim_elements(
    ["a rotating drum", "a heated nozzle", "a wireless transmitter"],
    {"us-111": ["a rotating drum"], "gb-222": ["a heated nozzle"]},
))
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| False novelty conclusion | Coverage gaps read as clean results | Disclose sources, queries, and gaps explicitly |
| Keyword-only querying | Synonyms and drafting conventions missed | Classification plus synonym expansion in the query matrix |
| Reading-list output | Hits collected without claim mapping | Map every promoted hit to claim elements |
| Non-patent literature skipped | Search confined to patent databases | Include journals, manuals, and open repositories in scope |
| Stale classifications | Reclassification shifts missed the target class | Verify current classification placement before final coverage |

## Security and Authority Boundary

Prior art searches can reveal competitive strategy and, when run for litigation, carry privilege considerations. Keep search scopes and results confidential, attribute sources correctly in any output, and do not file or prosecute based on automation output without qualified review.

## Evidence

This skill is grounded in dated public implementation references:

1. The Google Patents public patent search service (https://patents.google.com/).
2. The United States Patent and Trademark Office search resources (https://www.uspto.gov/).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Legal Research](legal-research.md) — the source-evaluation and citation discipline this search shares.
- [Literature Review](literature-review.md) — the non-patent literature coverage half of the search.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
