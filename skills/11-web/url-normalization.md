---
title: "URL Normalization"
category: 11-web
level: basic
stability: experimental
description: "Normalize URLs by lowercasing scheme and host, removing default ports and fragments, sorting query parameters, and collapsing path noise so identical resources compare equal."
added: "2026-10"
version: v1
related: ["url-fetching", "link-extraction"]
---

# URL Normalization

Category: Web | Level: basic | Stability: experimental | Version: v1

## Description

Two strings that differ can still name the same page: mixed case, an explicit :443, a stray fragment, unsorted parameters. Naive deduplication misses them all. Normalization applies a declared, ordered set of transformations — scheme and host lowercased, default ports removed, empty fragments dropped, parameters sorted — producing one canonical form per resource so equality checks mean something.

## When to Use

Use before storing, deduplicating, or comparing URLs from crawls, logs, or user input, and as the canonicalization step of any fetch cache key.

Do not normalize URLs whose case-sensitive path is part of an API contract; preserve those verbatim and exclude them from normalization by policy.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `url` | `string` | Yes | The URL to canonicalize |
| `sort_params` | `boolean` | No | Whether query parameters are sorted; default true |
| `strip_fragment` | `boolean` | No | Whether to drop the fragment; default true |

## Procedure

1. Split the URL into scheme, host, port, path, query, and fragment before any transformation.
2. Lowercase scheme and host; they are case-insensitive by URL grammar.
3. Drop ports that are the scheme default (443 for https, 80 for http); keep non-default ports.
4. Collapse an empty fragment; when stripping is on, drop any fragment per policy.
5. Sort query parameters by name then value so parameter order stops producing duplicates.
6. Normalize the path — collapse duplicate slashes, resolve dot segments — without changing case.
7. Return the canonical string and use it, not the input, as every comparison and cache key.

## Outputs

| Output | Type | Description |
|---|---|---|
| `canonical` | `string` | The normalized URL |
| `changed` | `boolean` | Whether normalization altered the input |

## Runnable Example

```python
from urllib.parse import urlsplit, urlunsplit, parse_qsl

def normalize_url(url, sort_params=True, strip_fragment=True):
    parts = urlsplit(url)
    scheme = parts.scheme.lower()
    host = (parts.hostname or "").lower()
    default = (scheme == "https" and parts.port == 443) or (scheme == "http" and parts.port == 80)
    netloc = host if parts.port is None or default else f"{host}:{parts.port}"
    query = parts.query
    if sort_params:
        query = "&".join(f"{k}={v}" for k, v in sorted(parse_qsl(query)))
    fragment = "" if strip_fragment else parts.fragment
    path = parts.path or "/"
    return urlunsplit((scheme, netloc, path, query, fragment))

raw = "https://Example.COM:443/a/b/?z=1&a=2#frag"
print(normalize_url(raw))
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Case-sensitive paths | Host rules applied to the path | Lowercase scheme and host only; paths stay as-is |
| Parameter-order duplicates | Same resource stored twice | Sort query parameters before comparison |
| Port mishandling | Non-default ports stripped | Strip only scheme-default ports |
| Cache fragmentation | Raw keys used in the fetch cache | Key every cache on the canonical form |
| Over-normalization | API URLs altered under contract | Exempt case-sensitive paths by explicit policy |

## Security and Authority Boundary

Normalization rewrites identifiers; it must never rewrite authority. Credentials embedded in URLs are a separate defect to flag and strip deliberately, not silently, and canonical forms inherit the trust level of their source.

## Evidence

This skill is grounded in dated public implementation references:

1. RFC 3986 defining URI syntax and normalization (https://www.rfc-editor.org/rfc/rfc3986).
2. Wikipedia’s overview of URI normalization (https://en.wikipedia.org/wiki/URI_normalization).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [URL Fetching](url-fetching.md) — the consumer whose cache keys become collision-free after normalization.
- [Link Extraction](link-extraction.md) — the producer whose raw links require canonicalization before storage.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
