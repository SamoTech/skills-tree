**Category:** Domain-Specific
**Skill Level:** `advanced`
**Stability:** stable
**Added:** 2026-04

### Description
Parses structured and unstructured application, infrastructure, and security logs to identify errors, anomaly clusters, performance regressions, and root-cause signals. Integrates with alerting and incident workflows.

### Example
```python
import re
from collections import Counter

SEVERITY = re.compile(r"^(ERROR|WARN|INFO|DEBUG)")

def analyse_logs(lines: list[str]) -> dict:
    counts = Counter()
    errors = []
    for line in lines:
        m = SEVERITY.match(line)
        if m:
            level = m.group(1)
            counts[level] += 1
            if level == "ERROR":
                errors.append(line[:120])
    return {"counts": dict(counts), "sample_errors": errors[:3]}

logs = [
    "ERROR db timeout after 30s",
    "INFO request processed in 42ms",
    "ERROR auth service returned 503",
    "WARN memory usage at 87%",
]
print(analyse_logs(logs))
```

### Related Skills
- [Incident Response](incident-response.md)
- [Anomaly Detection](../12-data/anomaly-detection.md)
- [Monitoring Alert Triage](alert-triage.md)
