**Category:** Orchestration
**Skill Level:** Intermediate
**Stability:** stable
**Added:** 2025-03

### Description
Automatically retries failed agent steps or API calls using exponential backoff with jitter. Distinguishes between transient errors (network timeout, 429) and permanent failures (400, 404) and only retries the former.

### Example
```python
import time, random, functools
from typing import Type

RETRYABLE_ERRORS = (ConnectionError, TimeoutError)

def retry_with_backoff(
    max_attempts: int = 5,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    retryable: tuple[Type[Exception], ...] = RETRYABLE_ERRORS,
):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except retryable as e:
                    if attempt == max_attempts:
                        raise
                    delay = min(base_delay * (2 ** (attempt - 1)), max_delay)
                    jitter = random.uniform(0, delay * 0.2)
                    wait = delay + jitter
                    print(f"Attempt {attempt} failed ({e}). Retrying in {wait:.1f}s...")
                    time.sleep(wait)
        return wrapper
    return decorator

@retry_with_backoff(max_attempts=4, base_delay=2.0)
def call_external_api(url: str) -> dict:
    import requests
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    return resp.json()
```

### Related Skills
- [Rate Limiting Awareness](../14-security/rate-limiting.md)
- [Sequential Workflow](sequential-workflow.md)
- [Logging and Observability](logging-observability.md)
