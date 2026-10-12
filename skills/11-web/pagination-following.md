---
title: "Pagination Following"
category: 11-web
level: basic
stability: experimental
description: "Follow paginated listings through declared next-link selectors with visited-set loop detection and a hard page cap so a crawl terminates exactly where the listing does."
added: "2026-10"
version: v1
related: ["web-scraping", "link-extraction"]
---

# Pagination Following

Category: Web | Level: basic | Stability: experimental | Version: v1

## Description

Paginated content hides most of the corpus behind a “next” affordance, and a naive loop either stops early or spins forever on a circular link. This skill defines pagination traversal as a bounded graph walk: each page declares how its next link is identified, a visited set rejects cycles, and a page cap bounds the walk even when the listing is generated adversarially.

## When to Use

Use when scraping or crawling structured listings — search results, catalogs, archives — that expose next-page links or numbered pages.

Do not use for infinite-scroll feeds that expose no pagination affordance; those need event-driven capture, not link following.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `pages` | `map[url -> next_url | null]` | Yes | Observed page transitions, or a resolver producing them |
| `max_pages` | `integer` | Yes | Hard cap on pages visited per listing |
| `visited` | `set[url]` | Yes | Mutable cycle-detection state |

## Procedure

1. Declare the next-link selector convention up front — rel=next, a labeled link, or a numbered URL scheme — and use it consistently.
2. Normalize each next URL before comparison so parameter noise cannot disguise a cycle.
3. Record every visited page in the visited set; a next URL already present is a loop, and traversal stops with the loop identified.
4. Stop at the first missing next link; absence is the listing’s terminal, not an error.
5. Enforce the page cap even when the listing keeps offering links; unbounded traversal is a policy violation.
6. Emit the visited sequence plus a terminal reason — terminal, loop, or cap — so the walk is auditable.

## Outputs

| Output | Type | Description |
|---|---|---|
| `visited` | `list[url]` | Ordered pages actually fetched |
| `terminal_reason` | `string` | terminal, loop-detected, or page-cap reached |

## Runnable Example

```python
def follow_pagination(transitions, max_pages):
    """transitions: url -> next url or None; returns traversal and reason."""
    visited = []
    current = transitions["start"]
    while current is not None:
        if current in visited:
            return visited, "loop-detected"
        if len(visited) >= max_pages:
            return visited, "page-cap"
        visited.append(current)
        current = transitions.get(current)
    return visited, "terminal"

catalog = {"start": "/items?page=1", "/items?page=1": "/items?page=2",
           "/items?page=2": "/items?page=3", "/items?page=3": None}
pages, reason = follow_pagination(catalog, max_pages=10)
print(reason, pages)
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Infinite loop | Next link points to an earlier page | Detect cycles with a visited set and stop with evidence |
| Premature stop | Next-link selector misses the page’s convention | Declare the convention per site and test it on page one |
| Silent truncation | Page cap reached but reported as done | Report the cap as its own terminal reason |
| URL noise | Tracking parameters disguise repeated pages | Normalize URLs before loop detection |
| Off-list drift | Next selector matches unrelated links | Constrain following to the listing container |

## Security and Authority Boundary

Pagination traversal is still fetching; robots rules, rate limits, and terms of service apply to every page visited. The page cap is a politeness bound as much as a correctness one.

## Evidence

This skill is grounded in dated public implementation references:

1. MDN documentation for link type rel attributes including next (https://developer.mozilla.org/en-US/docs/Web/HTML/Attributes/rel).
2. The WHATWG HTML specification section on link types (https://html.spec.whatwg.org/multipage/links.html).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Web Scraping](web-scraping.md) — the extraction consumer that needs every page this walk reaches.
- [Link Extraction](link-extraction.md) — supplies the candidate next links the selector convention filters.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
