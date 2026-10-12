---
title: "Infinite Scroll Handling"
category: 11-web
level: basic
stability: experimental
description: "Extract complete data sets from pages that reveal content incrementally on scroll, with termination detection, batch deduplication, and bounded run budgets."
added: "2026-10"
version: v1
related: ["web-scraping","pagination-following"]
---

# Infinite Scroll Handling

Category: Web | Level: basic | Stability: experimental | Version: v1

## Description

Infinite scroll pages never announce that they are finished. The skill treats scrolling as a batch protocol: extract the visible viewport, scroll one viewport height, wait for the page to settle, deduplicate against what is already collected, and terminate on a budget, a sentinel element, or a run of empty batches. Each batch is persisted as it arrives so a late failure loses only the tail.

## When to Use

Use when a feed, gallery, or results list reveals content as the user scrolls and the full set must be collected rather than sampled.

Do not scroll until the page stops by itself without a hard budget. Some feeds generate content forever and will exhaust memory, time, or rate limits before they exhaust content.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `page` | `object` | Yes | Live page containing the scrollable content region |
| `batch_extractor` | `object` | Yes | Function returning the items visible in the current viewport |
| `budget` | `object` | No | Hard bounds: max scrolls, max items, or deadline; defaults to a fixed scroll cap |

## Procedure

1. Extract the initial viewport before any scroll and record it as the first batch.
2. Scroll by one viewport height and wait for the network or DOM to settle before extracting.
3. Re-extract and deduplicate against already-collected batches using stable item keys.
4. Terminate when the budget is hit, the sentinel appears, or several consecutive batches yield nothing new.
5. Persist each batch before scrolling again so a late failure loses only the tail.
6. Report the collected count, batch count, and the exact termination reason.

## Outputs

| Output | Type | Description |
|---|---|---|
| `items` | `array` | Deduplicated items collected across all batches |
| `batches` | `array` | Per-batch counts and persistence status |
| `termination` | `object` | Stop reason, final scroll position, and budget usage |

## Runnable Example

```python
def plan_scroll_batches(batch_sizes, budget, max_empty):
    """batch_sizes: items extracted per scroll cycle"""
    collected = 0
    empty = 0
    for i, size in enumerate(batch_sizes):
        collected += size
        if i + 1 >= budget:
            return {"stop": "budget", "collected": collected, "batches": i + 1}
        empty = 0 if size else empty + 1
        if empty >= max_empty:
            return {"stop": "exhausted", "collected": collected, "batches": i + 1}
    return {"stop": "sentinel", "collected": collected, "batches": len(batch_sizes)}

print(plan_scroll_batches([20, 20, 20, 0, 0], budget=6, max_empty=2))
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Endless scroll loop | Feed generates content indefinitely | Enforce a hard budget on scrolls, items, and time |
| Duplicate items collected | Revealed batches overlap the previous viewport | Deduplicate on stable keys before counting |
| Premature stop | Slow loading read as an exhausted feed | Require consecutive empty batches, not a single one |
| Dropped batches on crash | All items held in memory until the end | Persist per batch as it arrives |
| Rate limited mid-run | Scroll cadence exceeds server tolerance | Back off between batches and respect limits |

## Security and Authority Boundary

Scrolling is automated access even when it mimics a user. Respect robots directives and rate limits, collect only what the task requires, and avoid incrementally harvesting personal profiles or private content that a single page view would not expose.

## Evidence

This skill is grounded in dated public implementation references:

1. The MDN reference for the Intersection Observer API used by infinite scroll implementations (https://developer.mozilla.org/en-US/docs/Web/API/Intersection_Observer_API).
2. The Playwright actionability documentation for waiting on settle states (https://playwright.dev/python/docs/actionability).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Web Scraping](web-scraping.md) — the extraction layer that consumes each revealed batch.
- [Pagination Following](pagination-following.md) — the paged analogue of incremental reveal with discrete page markers.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
