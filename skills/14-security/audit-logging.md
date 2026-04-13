---
title: "Audit Logging"
category: 14-security
level: advanced
stability: stable
description: "Apply audit logging in AI agent workflows."
added: "2025-03"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-14-security-audit-logging.json)

**Category:** Security
**Skill Level:** `advanced`
**Stability:** stable
**Added:** 2026-04

### Description
Records a tamper-evident, structured audit trail of agent actions, tool calls, data accesses, and decisions. Supports compliance reporting, forensic investigation, and anomaly detection over agent behaviour.

### Example
```python
import json, time, hashlib
from dataclasses import dataclass, asdict

@dataclass
class AuditEntry:
    timestamp: float
    action: str
    actor: str
    resource: str
    outcome: str
    prev_hash: str = ""
    hash: str = ""

    def compute_hash(self) -> str:
        payload = json.dumps(asdict(self), sort_keys=True).encode()
        return hashlib.sha256(payload).hexdigest()

log: list[AuditEntry] = []

def record(action: str, actor: str, resource: str, outcome: str):
    prev = log[-1].hash if log else ""
    entry = AuditEntry(time.time(), action, actor, resource, outcome, prev_hash=prev)
    entry.hash = entry.compute_hash()
    log.append(entry)

record("READ", "agent-1", "db:users:42", "success")
record("WRITE", "agent-1", "db:orders:new", "success")
print([e.action for e in log])
```

### Related Skills
- [Human In Loop](human-in-loop.md)
- [Logging & Observability](../15-orchestration/logging-observability.md)
