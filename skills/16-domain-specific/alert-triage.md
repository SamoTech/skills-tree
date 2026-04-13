---
title: "Alert Triage"
category: 16-domain-specific
level: advanced
stability: stable
description: "Apply alert triage in AI agent workflows."
added: "2025-03"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-16-domain-specific-alert-triage.json)

**Category:** Domain-Specific
**Skill Level:** `advanced`
**Stability:** stable
**Added:** 2026-04

### Description
Classifies, deduplicates, and prioritises monitoring alerts from sources like PagerDuty, Datadog, or Prometheus. Suppresses noise, identifies correlated root causes, routes to the correct team, and generates concise summaries for on-call engineers.

### Example
```python
from typing import List

ALERT_WEIGHTS = {"critical": 3, "warning": 2, "info": 1}

def triage_alerts(alerts: List[dict]) -> List[dict]:
    # Deduplicate by name, keep highest severity
    seen = {}
    for alert in alerts:
        name = alert["name"]
        if name not in seen or ALERT_WEIGHTS[alert["severity"]] > ALERT_WEIGHTS[seen[name]["severity"]]:
            seen[name] = alert
    return sorted(seen.values(), key=lambda a: -ALERT_WEIGHTS[a["severity"]])

alerts = [
    {"name": "db_down", "severity": "critical", "service": "postgres"},
    {"name": "db_down", "severity": "warning", "service": "postgres"},
    {"name": "cpu_high", "severity": "warning", "service": "api"},
    {"name": "disk_low", "severity": "info", "service": "worker"},
]
print(triage_alerts(alerts))
```

### Related Skills
- [Incident Response](incident-response.md)
- [Log Analysis](log-analysis.md)
- [Prioritization](../02-reasoning/prioritization.md)
