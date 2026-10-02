---
name: code-github-api
description: Work with GitHub APIs using documented endpoints, authentication boundaries, pagination, error handling, and least-privilege access.
metadata:
  source: skills/05-code/github-api.md
  category: 05-code
---

## Description
Work with GitHub APIs using documented endpoints, authentication boundaries, pagination, error handling, and least-privilege access. Validate response semantics and avoid assuming that an API response proves a repository state change unless the resulting state is checked.

## When to Use
Use when an implementation or automation must interact with GitHub's API.

## Inputs / outputs / failure modes

| Area | Guidance |
|---|---|
| Inputs | API documentation, endpoint, authentication scope, request data, and expected response. |
| Outputs | Correct API interaction and independently verified resulting state. |
| Failure modes | Wrong endpoint, insufficient scope, pagination errors, rate limits, or false completion claims. |

## Runnable Example

```python
from urllib.parse import urlparse

url = 'https://api.github.com/repos/example/project'
parts = urlparse(url)
print(parts.netloc)
print(parts.path)
```

## Failure modes
- Using undocumented endpoint behavior.
- Exposing credentials in source or logs.
- Ignoring pagination or rate limits.
- Treating a request response as proof without verifying resulting state.

## Related
- 05-code
- AI_CONSTITUTION.md
- meta/AGENT_OPERATING_MODEL.md

## Evidence
Repository-backed implementation guidance grounded in repository governance and validation workflows; no external benchmark claim is made.
