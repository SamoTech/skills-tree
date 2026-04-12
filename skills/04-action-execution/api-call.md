---
Category: Action Execution
Skill Level: Advanced
Stability: Stable
Tags: [api, http, rest, graphql, authentication, retry, rate-limiting]
---

# API Call

### Description
Executes authenticated HTTP requests to REST and GraphQL APIs with retry logic, rate-limit handling, circuit breaking, request signing, and response validation. Supports OAuth2, API key, JWT, HMAC, and mTLS authentication schemes.

### When to Use
- Triggering external services (Stripe, Twilio, GitHub, Slack, etc.) from agentic pipelines
- Posting data, creating resources, or triggering webhooks as part of task execution
- Integrating with internal microservices via REST or GraphQL

### Example
```python
import httpx, time
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

@retry(
    retry=retry_if_exception_type((httpx.HTTPStatusError, httpx.TimeoutException)),
    wait=wait_exponential(multiplier=1, min=1, max=60),
    stop=stop_after_attempt(5)
)
def call_api(method: str, url: str, token: str, **kwargs) -> dict:
    with httpx.Client(timeout=30) as client:
        r = client.request(
            method, url,
            headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
            **kwargs
        )
        if r.status_code == 429:
            retry_after = int(r.headers.get("Retry-After", 5))
            time.sleep(retry_after)
            r.raise_for_status()
        r.raise_for_status()
        return r.json()

# GraphQL example
def graphql_query(url: str, token: str, query: str, variables: dict = None) -> dict:
    return call_api("POST", url, token, json={"query": query, "variables": variables or {}})
```

### Advanced Techniques
- **Circuit breaker**: use `pybreaker` to stop calling a failing service after N consecutive failures
- **Request signing**: HMAC-SHA256 signature for AWS or Stripe webhook validation
- **mTLS**: pass `cert=('client.crt', 'client.key')` to `httpx.Client` for mutual TLS
- **Async batch**: use `httpx.AsyncClient` with `asyncio.gather` for parallel API calls

### Related Skills
- `http-request`, `webhook-trigger`, `api-tool`, `api-response-parsing`, `rate-limiting`
