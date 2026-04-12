**Category:** Orchestration
**Skill Level:** Intermediate
**Stability:** stable
**Added:** 2025-03

### Description
Instruments agent executions with structured tracing, span timing, and log correlation IDs. Outputs to OpenTelemetry-compatible backends (Jaeger, Datadog, Grafana) and the console. Enables debugging multi-hop workflows by linking spans across agents.

### Example
```python
import time, uuid, json
from contextlib import contextmanager
from typing import Optional

class Tracer:
    def __init__(self, service: str):
        self.service = service
        self.spans: list[dict] = []

    @contextmanager
    def span(self, name: str, parent_id: Optional[str] = None):
        span_id = str(uuid.uuid4())[:8]
        trace_id = str(uuid.uuid4())[:8]
        start = time.perf_counter()
        span = {"name": name, "span_id": span_id, "trace_id": trace_id,
                "parent_id": parent_id, "service": self.service}
        print(f"[TRACE] START {name} (span={span_id})")
        try:
            yield span_id
            span["status"] = "ok"
        except Exception as e:
            span["status"] = "error"
            span["error"] = str(e)
            raise
        finally:
            span["duration_ms"] = round((time.perf_counter() - start) * 1000, 2)
            self.spans.append(span)
            print(f"[TRACE] END   {name} ({span['duration_ms']}ms, status={span['status']})")

    def export(self) -> str:
        return json.dumps(self.spans, indent=2)

tracer = Tracer("research-agent")

with tracer.span("orchestrate") as root_id:
    with tracer.span("research", parent_id=root_id):
        time.sleep(0.05)
    with tracer.span("write", parent_id=root_id):
        time.sleep(0.03)

print(tracer.export())
```

### Related Skills
- [Audit Logging](../14-security/audit-logging.md)
- [Budget / Token Management](budget-management.md)
- [Sequential Workflow](sequential-workflow.md)
