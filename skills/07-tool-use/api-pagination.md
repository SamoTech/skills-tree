---
title: "API Pagination"
category: 07-tool-use
level: intermediate
stability: experimental
description: "Walk paged API result sets to completion — cursor or page parameters, per-request limits, and a terminal condition — without missing or double-processing records."
added: "2026-10"
version: v1
related: ["custom-api-wrapper", "stripe-api"]
---

# API Pagination

Category: Tool Use | Level: intermediate | Stability: experimental | Version: v1

## Description

A paged response is a promise that the full list exists and a refusal to hand it over at once. This skill treats the pager as an explicit state machine: the request carries the continuation token, the response carries the next one, and iteration stops only when the API says it is finished. Rate limits are part of the traversal, not an error condition — a pager that ignores them will be right about the data and wrong about the budget.

## When to Use

Use whenever an API returns lists with a cursor, page token, or offset parameter — directories, event logs, resource listings — and the task needs the complete set.

Do not fetch all pages when the task only needs a bounded prefix; a search that stops at the first match should not traverse the whole corpus.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `endpoint` | `string` | Yes | The paged API operation to traverse |
| `page_size` | `integer` | Yes | Records requested per page, within the API maximum |
| `collect` | `callable` | Yes | What to do with each record as pages arrive |
| `rate_limit` | `map` | No | The request budget the traversal must respect |

## Procedure

1. Read the API contract for its pagination style — cursor, offset, or page token — before writing any loop.
2. Issue the first request with the largest page size the API allows, because fewer round trips is fewer chances to rate-limit.
3. Hand each record to the collector as its page arrives, rather than accumulating every page in memory.
4. Persist the continuation token between requests, and treat an absent or null token as the terminal condition — never a missing key.
5. Respect the rate limit: back off when the API says so, and prefer the retry-after guidance over a fixed sleep when it is offered.
6. Record the traversal outcome — pages fetched, records seen, terminal reason — so an incomplete walk is detectable after the fact.

## Outputs

| Output | Type | Description |
|---|---|---|
| `records` | `iterator` | Each record delivered as its page arrives |
| `traversal` | `map` | Page count, record count, and terminal condition |

## Runnable Example

```python
def walk_pages(fetch_page, collect, max_pages=None):
    token = None
    pages = 0
    while True:
        response = fetch_page(token)
        for record in response["items"]:
            collect(record)
        pages += 1
        token = response.get("next_token")
        if token is None:
            return {"pages": pages, "stopped": "terminal"}
        if max_pages is not None and pages >= max_pages:
            return {"pages": pages, "stopped": "budget"}

seen = []

def fake_fetch(token):
    # returns one page, then signals completion via a null token
    return {"items": ["record-1", "record-2"], "next_token": None}

result = walk_pages(fake_fetch, seen.append, max_pages=10)
print(result, "collected:", len(seen))
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Dropped records | A null next-token value misread as an error | Treat the documented null token as the sole terminal condition |
| Double processing | A retried page appended twice | Make the collector idempotent or track the last token processed |
| Memory blowout | Every page held until the end | Collect per page; never retain the full traversal |
| Rate-limit storms | Consecutive throttled responses during the walk | Back off on the first signal, not the third |
| Silent truncation | A walk stopped early and nobody noticed | Report pages, records, and stop reason at the end |

## Security and Authority Boundary

Continuation tokens are credentials for data position: they can leak record ranges and query context when logged or shared, so treat them as sensitive in logs, and scope every traversal to the caller whose credentials opened it — a walk must never resume under a different principal.

## Evidence

This skill is grounded in dated public implementation references:

1. The Stripe API documentation on pagination (https://docs.stripe.com/api/pagination).
2. Wikipedia's overview of rate limiting (https://en.wikipedia.org/wiki/Rate_limiting).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Custom API Wrapper](custom-api-wrapper.md) — the adapter layer that exposes paging cleanly.
- [Stripe API](stripe-api.md) — a concrete paginated API this pattern walks.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
