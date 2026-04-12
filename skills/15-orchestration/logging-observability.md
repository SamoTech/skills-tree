**Category:** Orchestration
**Skill Level:** `advanced`
**Stability:** stable
**Added:** 2026-04

### Description
Instruments multi-agent workflows with structured logging, distributed tracing, and metrics collection. Provides visibility into agent steps, latency, token usage, and failure modes for debugging and monitoring.

### Example
```python
import time, uuid, json
from contextlib import contextmanager

TRACE_LOG: list[dict] = []

@contextmanager
def span(name: str, trace_id: str = None):
    span_id = str(uuid.uuid4())[:8]
    trace_id = trace_id or str(uuid.uuid4())[:8]
    start = time.perf_counter()
    record = {"span_id": span_id, "trace_id": trace_id, "name": name, "status": "ok"}
    try:
        yield record
    except Exception as e:
        record["status"] = "error"
        record["error"] = str(e)
        raise
    finally:
        record["duration_ms"] = round((time.perf_counter() - start) * 1000, 2)
        TRACE_LOG.append(record)

with span("planner") as s:
    with span("tool_call", s["trace_id"]):
        time.sleep(0.01)

print(json.dumps(TRACE_LOG, indent=2))
```

### Related Skills
- [Audit Logging](../14-security/audit-logging.md)
- [Budget Management](budget-management.md)
