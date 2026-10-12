---
title: "Alert Triage"
category: 16-domain-specific
level: advanced
stability: stable
description: "Apply alert triage in an AI workflow with explicit scope, domain constraints, validation, and documented failure handling."
related: ["16-domain-specific", "input-guardrails", "output-guardrails"]
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

## Failure Modes

- **Suppression masking:** aggressive noise suppression hiding a genuine incident that correlates with routine alerts; every suppression rule needs a measured false-negative check.
- **Wrong-team routing:** misrouted alerts creating silent queues; verify routing keys against the current on-call ownership map.
- **Deduplication collisions:** distinct incidents merged because they share a signature; correlation keys must carry enough distinguishing fields.
- **Summarization loss:** compressed on-call summaries dropping severity, affected service, or required action; those three fields are mandatory.
- **Stale severity mappings:** static priority rules that no longer match the service's current criticality.

## Evidence
The canonical skill file is the authoritative repository implementation. Repository schema, validation workflows, and the Agent Skills projection contract define structural conformance. Domain-specific factual claims must remain traceable to supplied or independently verified authoritative sources.

### Related
- 16-domain-specific
- input-guardrails
- output-guardrails
