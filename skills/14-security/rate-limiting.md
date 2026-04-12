**Category:** Security & Safety
**Skill Level:** Basic
**Stability:** stable
**Added:** 2025-03

### Description
Detects and respects API rate limits by inspecting response headers (`X-RateLimit-Remaining`, `Retry-After`) and implementing exponential backoff with jitter. Prevents agents from hammering APIs and triggering bans.

### Example
```python
import time, random, requests
from functools import wraps

def rate_limit_aware(max_retries: int = 5, base_delay: float = 1.0):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                response = func(*args, **kwargs)
                if response.status_code == 429:
                    retry_after = float(
                        response.headers.get("Retry-After", base_delay * (2 ** attempt))
                    )
                    jitter = random.uniform(0, retry_after * 0.1)
                    wait = retry_after + jitter
                    print(f"Rate limited. Waiting {wait:.1f}s (attempt {attempt+1}/{max_retries})")
                    time.sleep(wait)
                    continue
                return response
            raise RuntimeError("Max retries exceeded after rate limiting")
        return wrapper
    return decorator

@rate_limit_aware(max_retries=5, base_delay=2.0)
def call_api(url: str) -> requests.Response:
    return requests.get(url)
```

### Related Skills
- [HTTP Request](../04-action-execution/http-request.md)
- [Audit Logging](audit-logging.md)
- [Retry with Backoff](../15-orchestration/retry-backoff.md)
