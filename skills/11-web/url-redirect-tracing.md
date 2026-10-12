---
title: "URL Redirect Tracing"
category: 11-web
level: intermediate
stability: experimental
description: "Trace redirect chains hop by hop with loop detection and a hard hop cap so agents know the final canonical target of a URL before trusting or storing it."
added: "2026-10"
version: v1
related: ["url-fetching", "browser-navigation"]
---

# URL Redirect Tracing

Category: Web | Level: intermediate | Stability: experimental | Version: v1

## Description

A URL that redirects is a claim about where content really lives, and the chain matters: shorteners launder destinations, loops waste budgets, and mixed http-to-https hops change the security posture mid-chain. This skill records every hop as (from, to, status-class), detects cycles, and refuses to follow past a declared hop cap.

## When to Use

Use when resolving shortened or syndicated links into their final targets, when auditing where a stored URL actually lands, or before treating a fetched origin as trustworthy.

Do not use to bypass a site’s redirect intent; if a host routes you to a consent or login page, that response is the answer, not an obstacle.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `hops` | `map[url -> next_url | null]` | Yes | Observed redirect transitions with terminal markers |
| `max_hops` | `integer` | Yes | Hard cap on followed redirects per trace |
| `visited` | `set[url]` | Yes | Mutable loop-detection state |

## Procedure

1. Record each hop as it happens — from URL, to URL, status class — never reconstruct the chain from memory after the fact.
2. Normalize URLs before cycle comparison; a loop hidden by a trailing slash is still a loop.
3. Treat a repeated URL as a cycle and stop immediately, reporting the loop entry point.
4. Stop at the hop cap and report it distinctly from a terminal resolution.
5. Preserve the full chain in the result; a bare final URL without its chain is unauditable.
6. Flag scheme downgrades (https to http) in the chain as a security-relevant event.

## Outputs

| Output | Type | Description |
|---|---|---|
| `chain` | `list[(from, to, status_class)]` | The full recorded redirect chain |
| `final_url` | `string | null` | Terminal target, or null when unresolved |
| `status` | `string` | terminal, loop-detected, or hop-cap reached |

## Runnable Example

```python
def trace_redirects(hops, max_hops=10):
    """hops: url -> next url or None; returns chain and status."""
    chain = []
    visited = set()
    current = hops["start"]
    while current is not None:
        if current in visited:
            return chain, "loop-detected"
        if len(chain) >= max_hops:
            return chain, "hop-cap"
        visited.add(current)
        nxt = hops.get(current)
        chain.append((current, nxt))
        current = nxt
    return chain, "terminal"

hops = {"start": "http://a.example", "http://a.example": "https://a.example",
        "https://a.example": "https://www.example.com/", "https://www.example.com/": None}
chain, status = trace_redirects(hops)
print(status)
for source, target in chain:
    print(source, "->", target)
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Redirect loops | Two URLs redirect to each other | Detect cycles with a visited set and stop |
| Unbounded chains | Adversarial chains exhaust the budget | Enforce a hard hop cap per trace |
| Memory-reconstructed chains | Hops inferred after fetching completes | Record every hop as it happens |
| Scheme downgrade missed | https-to-http hop treated as neutral | Flag downgrades in the chain report |
| Noise loops | Trailing-slash variants seen as cycles | Normalize URLs before comparison |

## Security and Authority Boundary

Redirect chains cross trust boundaries: a chain that ends off-origin changes what credentials and cookies are safe to send. Trace before trusting, and never forward authentication material to a target the chain has not resolved.

## Evidence

This skill is grounded in dated public implementation references:

1. MDN documentation for HTTP 301 permanent redirect (https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/301).
2. Wikipedia’s overview of URL redirection (https://en.wikipedia.org/wiki/URL_redirection).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [URL Fetching](url-fetching.md) — the transport whose observed responses become this trace’s hops.
- [Browser Navigation](browser-navigation.md) — user-visible navigation that this tracing makes auditable.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
