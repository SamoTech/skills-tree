---
name: logging-observability
description: Instrument agent workflows with structured logs, correlation identifiers, metrics, and traceable state transitions.
metadata:
  source: skills/15-orchestration/logging-observability.md
  category: 15-orchestration
  version: "v2"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-15-orchestration-logging-observability.json)

# Logging Observability

**Category:** `orchestration`
**Skill Level:** `advanced`
**Stability:** `stable`
**Added:** 2025-03

### Description

Instrument agent workflows with structured logs, correlation identifiers, metrics, and traceable state transitions. The orchestration step is contract-first: validate state and inputs before acting, and verify the resulting state transition instead of trusting acknowledgements.

### Inputs / Outputs

| Direction | Field | Type | Contract |
|---|---|---|---|
| Input | events | list of object | State transitions with a correlation id and timestamp |
| Input | redaction | object | Fields minimized or masked before logging |
| Output | trace | list of object | Ordered, correlated log records suitable for replay |
| Output | metrics | object | Derived counters (durations, retries, failures) per stage |

### Procedure
1. Assign a correlation identifier at workflow start and thread it through every record.
2. Log state transitions as structured records with timestamps and stage ids.
3. Apply redaction before writing: no secrets, credentials, or personal data in logs.
4. Derive metrics (duration, retry count, failure count) from the same records.
5. Keep the trace replayable: ordered records sufficient to reconstruct state transitions.
6. Verify that a failure can be diagnosed from the trace alone, without run-log access.

### Example

```python
import json
redact = {'token': '[REDACTED]'}
events = [{'corr': 'wf-12', 'stage': 'fetch', 'ms': 120, 'token': 'sk-secret'},
          {'corr': 'wf-12', 'stage': 'verify', 'ms': 45, 'token': 'sk-secret'}]
trace = [dict(e, token=redact['token']) for e in events]
assert all(t['token'] == '[REDACTED]' for t in trace)
assert [t['stage'] for t in trace] == ['fetch', 'verify']
print(json.dumps({'metrics': {'total_ms': sum(t['ms'] for t in trace)}, 'correlated': True}))
```

### Related Skills

- [Workflow Heartbeat Monitoring](workflow-heartbeat-monitoring.md) - liveness from the same records
- [Thread-Based Resume](thread-based-resume.md) - resume from logged state
- [Audit Logging](../14-security/audit-logging.md) - tamper-evident audit records

## Failure Modes

- Secrets or personal data written into logs.
- Records without a correlation id, so stages cannot be traced together.
- A trace that cannot reconstruct the state transitions it claims to record.
- Metrics derived from a different source than the published log records.

## Changelog
- v2 (2026-11): Structural modernization; added the input/output contract table, a skill-specific execution procedure, a deterministic example, and corpus-verified related links (replaced the unresolvable cross-category related references).
- v1 (2025-03): Initial entry.

## Evidence

- https://agentskills.io/specification

Evidence status: implementation guidance only; runtime behavior must be checked against the executing framework's documentation; no benchmark claim is made without reproducible evidence.
