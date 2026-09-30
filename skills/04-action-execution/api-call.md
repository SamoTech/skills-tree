---
title: "API Call"
category: 04-action-execution
level: intermediate
stability: stable
description: "Execute authenticated HTTP API requests with explicit timeouts, bounded retries, response validation, and secret-safe error handling."
added: "2026-09"
related: [http-request, api-response-parsing, rate-limiting]
---

# API Call

## Description

Execute an HTTP API operation as an agent action while making authentication, timeout, retry, idempotency, and response validation explicit. Credentials must come from secret-safe configuration and must never be embedded in source or logs.

## When to Use

- Calling REST or GraphQL services.
- Creating or updating remote resources.
- Integrating an external action into an agent workflow.

## Inputs / outputs / failure modes

| Input | Output | Failure mode |
|---|---|---|
| Method, URL, headers, body | Status and parsed response | Invalid request |
| Secret/token reference | Authenticated request | Missing credential |
| Timeout and retry policy | Bounded execution | Retry exhaustion |
| Idempotency policy | Safe retry decision | Duplicate side effect |

## Runnable example

```python
import json
import urllib.request

def api_call(url, token, method="GET", body=None, timeout=20):
    data = None if body is None else json.dumps(body).encode()
    req = urllib.request.Request(url, data=data, method=method,
        headers={"Authorization": f"Bearer {token}", "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return response.status, json.load(response)

status, result = api_call("https://example.invalid/items", "TOKEN")
print(status, result)
```

## Failure modes

- Retry non-idempotent mutations without an idempotency key.
- Log authorization headers or secret-bearing response data.
- Use unbounded retries or no timeout.
- Treat HTTP success as proof that the response schema is valid.

## Related

- http-request.md
- ../01-perception/api-response-parsing.md
- ../07-tool-use/tool-guardrails.md

## Evidence

- AI_CONSTITUTION.md
- AGENTS.md
- Repository security and validation workflows
