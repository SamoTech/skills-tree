![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-16-domain-specific-incident-response.json)

**Category:** Domain-Specific
**Skill Level:** `advanced`
**Stability:** stable
**Added:** 2026-04

### Description
Coordinates the full incident lifecycle: detection, severity classification, hypothesis-driven diagnosis, mitigation execution, stakeholder communication, and post-mortem generation. Combines log analysis, runbook execution, and escalation logic.

### Example
```python
from dataclasses import dataclass
from typing import Callable

@dataclass
class Incident:
    name: str
    error_rate: float
    latency_p99_ms: int

def triage(incident: Incident) -> dict:
    if incident.error_rate > 0.1 or incident.latency_p99_ms > 5000:
        severity = "SEV-1"
        action = "page oncall, rollback last deploy"
    elif incident.error_rate > 0.01:
        severity = "SEV-2"
        action = "investigate db connection pool, check error logs"
    else:
        severity = "SEV-3"
        action = "monitor for 15 min"
    return {"severity": severity, "action": action}

print(triage(Incident("api-gateway", error_rate=0.15, latency_p99_ms=6200)))
```

### Related Skills
- [Log Analysis](log-analysis.md)
- [Monitoring Alert Triage](alert-triage.md)
- [Risk Assessment](../02-reasoning/risk-assessment.md)
