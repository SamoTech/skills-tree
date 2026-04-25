---
title: "HTTP Request"
category: 04-action-execution
level: beginner
stability: stable
added: "2025-03"
updated: "2026-04"
version: v3
description: "Make an outbound HTTP call with authentication, retries, timeouts, idempotency keys, and a strict response contract. The fundamental tool every agent needs to talk to anything beyond itself."
tags: [action, http, networking, retries, idempotency]
dependencies:
  - package: httpx
    min_version: "0.28.0"
    tested_version: "0.28.1"
    confidence: verified
  - package: tenacity
    min_version: "9.0.0"
    tested_version: "9.0.0"
    confidence: verified
code_blocks:
  - id: "example-http-request"
    type: executable
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-04-action-execution-http-request.json)

# HTTP Request

## Description

An outbound HTTP call is the most common side-effect an agent performs. The naive `requests.get(url)` is fine for a script and a bug factory in production: no timeout, no retries, no idempotency, no structured logging, leaks credentials in error messages.

This skill is the production HTTP client every agent should use: explicit timeouts, exponential-backoff retries on **idempotent** methods only (GET / PUT / DELETE; never POST without an idempotency key), a strict response contract with typed errors, and a `safe_log` helper that never logs `Authorization` headers.

## When to Use

- The agent needs to call **any** HTTP endpoint — REST, JSON-RPC, webhook, anything.
- You want **uniform** retry / timeout / logging behaviour across all calls.
- Even when a "client library" exists — wrap *its* failures in this contract for consistent agent ergonomics.
- **Don't reimplement** when calling a major SaaS provider's SDK that already handles retries (Stripe, Anthropic, OpenAI). Use this for everything else.

## Inputs / Outputs

| Field | Type | Description |
|---|---|---|
| `method` | `Literal["GET","POST","PUT","PATCH","DELETE"]` | HTTP verb |
| `url` | `str` | Absolute URL |
| `headers` | `dict` | Extra headers (Authorization is auto-redacted in logs) |
| `params` | `dict` | Query string |
| `json` | `Any` | JSON body |
| `idempotency_key` | `str \| None` | Required for retried POST |
| `timeout` | `float` | Seconds, total (default 30) |
| → `status` | `int` | HTTP status code |
| → `data` | `Any` | Parsed JSON, or raw text |
| → `headers` | `dict` | Response headers |

## Runnable Example

```python
# pip install httpx tenacity
from __future__ import annotations
import json
import logging
import uuid
from dataclasses import dataclass
from typing import Any
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

log = logging.getLogger("http")

class HttpError(Exception):
    def __init__(self, status: int, body: str, url: str) -> None:
        super().__init__(f"HTTP {status} on {url}: {body[:200]}")
        self.status = status
        self.body = body
        self.url = url

class RetriableHttpError(HttpError):
    """5xx and 429 — safe to retry on idempotent methods."""

@dataclass
class HttpResponse:
    status: int
    data: Any
    headers: dict

_IDEMPOTENT = {"GET", "PUT", "DELETE", "HEAD", "OPTIONS"}

def _safe_headers(headers: dict) -> dict:
    """Redact secrets before logging."""
    redacted = dict(headers)
    for k in list(redacted):
        if k.lower() in {"authorization", "x-api-key", "cookie", "set-cookie"}:
            redacted[k] = "***REDACTED***"
    return redacted

@retry(
    reraise=True,
    stop=stop_after_attempt(4),
    wait=wait_exponential(multiplier=1, min=1, max=20),
    retry=retry_if_exception_type((httpx.TransportError, RetriableHttpError)),
)
def _send(client: httpx.Client, method: str, url: str, **kwargs) -> httpx.Response:
    log.info("http %s %s headers=%s", method, url, _safe_headers(kwargs.get("headers") or {}))
    r = client.request(method, url, **kwargs)
    if r.status_code >= 500 or r.status_code == 429:
        raise RetriableHttpError(r.status_code, r.text, url)
    return r

def http_request(
    method: str,
    url: str,
    *,
    headers: dict | None = None,
    params: dict | None = None,
    json_body: Any = None,
    idempotency_key: str | None = None,
    timeout: float = 30.0,
) -> HttpResponse:
    method = method.upper()
    headers = dict(headers or {})
    if method == "POST":
        # Set or generate an idempotency key so retries don't double-bill.
        headers.setdefault("Idempotency-Key", idempotency_key or str(uuid.uuid4()))
    elif method not in _IDEMPOTENT:
        # PATCH is iffy; force the caller to commit to idempotency.
        if "Idempotency-Key" not in headers:
            headers["Idempotency-Key"] = idempotency_key or str(uuid.uuid4())

    with httpx.Client(timeout=timeout, follow_redirects=True) as client:
        r = _send(client, method, url,
                  headers=headers, params=params, json=json_body)

    if r.status_code >= 400:
        raise HttpError(r.status_code, r.text, url)

    ct = r.headers.get("content-type", "")
    data: Any = r.json() if "json" in ct else r.text
    return HttpResponse(status=r.status_code, data=data, headers=dict(r.headers))

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    out = http_request("GET", "https://httpbin.org/json")
    print(f"status={out.status}")
    print(json.dumps(out.data, indent=2)[:200])
```

## Failure Modes

| Failure | Cause | Mitigation |
|---|---|---|
| Hangs forever | No timeout configured | `timeout=` is required, not optional |
| Double-billed POST | Retry without idempotency | Always send `Idempotency-Key` on POST |
| Retries swallow 4xx | Retrying client errors does nothing | Only retry on 5xx / 429 / `TransportError` |
| Auth header logged | Naive `print(headers)` | Always redact via `_safe_headers` before logging |
| DNS failure not retried | Treated as fatal | `httpx.TransportError` covers DNS + connect — retry it |
| Connection pool exhaustion | New `httpx.Client` per call in a loop | Reuse a long-lived `Client`; close on shutdown |
| 429 ignored | No `Retry-After` honour | Read header; sleep at least that long before retry |
| Cert error in dev | Self-signed CA | `verify=False` only for local dev — never in prod |

## Variants

| Variant | When |
|---|---|
| **Sync `httpx`** (above) | Default; reads like `requests`, faster, `httpx`-native |
| **Async `httpx`** | High-fan-out agents (`asyncio.gather` over many URLs) |
| **`aiohttp`** | Pure async; slightly different ergonomics |
| **gRPC / Protobuf** | When the service requires it; reuse the retry pattern |
| **Mock layer** | `respx` for httpx-based tests |

## Frameworks & Models

| Framework | Notes |
|---|---|
| `httpx` (above) | HTTP/2, sync+async, `requests`-compatible API |
| `requests` | Long-time default; sync only; slower |
| `aiohttp` | Async-first |
| `urllib3` | Standard lib level; verbose |

## Related Skills

- [Web Search](../11-web/web-search.md) — uses HTTP under the hood
- [Web Scraping](../11-web/web-scraping.md) — HTTP + HTML extraction
- [Retry & Backoff](../15-orchestration/retry-backoff.md) — generic retry pattern
- [Rate Limiting](../14-security/rate-limiting.md) — be a good citizen
- [Audit Logging](../14-security/audit-logging.md) — record every outbound call

## Changelog

| Date | Version | Change |
|---|---|---|
| 2025-03 | v1 | Stub |
| 2026-04 | v3 | Battle-tested: idempotency keys, retry-on-idempotent-only, header redaction, typed exceptions |
