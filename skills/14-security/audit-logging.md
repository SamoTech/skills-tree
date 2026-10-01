---
title: "Audit Logging"
category: 14-security
level: advanced
stability: stable
description: "Record security-relevant agent actions in a structured, tamper-evident audit trail without logging secrets or unnecessary personal data."
added: "2025-03"
updated: "2026-10"
version: v2
related: [human-in-loop, permission-checking, secret-scanning]
---

# Audit Logging

## Description

Audit logging gives an agent system an attributable record of security-relevant actions: tool calls, resource access, authorization decisions, approvals, failures, and externally visible side effects. The log should support investigation and accountability without becoming a second data-leak channel.

Use structured events with stable event types, actor identity, correlation IDs, timestamps, outcome, and a minimal resource reference. Do not record API keys, passwords, session cookies, full prompts containing sensitive data, or raw tool responses by default.

## Inputs / Outputs

| Input | Type | Required | Description |
|---|---|---:|---|
| `actor_id` | string | yes | Agent, service, or human identity responsible for the event |
| `action` | string | yes | Stable action name such as `tool.call` or `approval.decision` |
| `resource` | string | yes | Minimal resource identifier; avoid embedding sensitive payloads |
| `outcome` | string | yes | `success`, `failure`, `denied`, or `timeout` |
| `correlation_id` | string | no | Identifier linking related events across a workflow |
| `metadata` | dict | no | Non-sensitive structured context |

Output is a structured audit event containing timestamp, identity, action, resource reference, outcome, and an integrity field.

## Runnable Example

```python
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
import hashlib, json

@dataclass(frozen=True)
class AuditEvent:
    actor_id: str
    action: str
    resource: str
    outcome: str
    timestamp: str
    previous_hash: str = ""

def event_hash(event: AuditEvent) -> str:
    body = json.dumps(asdict(event), sort_keys=True).encode()
    return hashlib.sha256(body).hexdigest()

events: list[AuditEvent] = []
event = AuditEvent(
    actor_id="agent/research",
    action="tool.call",
    resource="search:public-web",
    outcome="success",
    timestamp=datetime.now(timezone.utc).isoformat(),
    previous_hash="",
)
events.append(event)
print(event_hash(event))
```

The example demonstrates an append-only hash chain primitive. A production implementation also needs protected storage, clock handling, access controls, retention policy, and key management where stronger authenticity guarantees are required.

## Failure Modes

| Failure | Cause | Mitigation |
|---|---|---|
| Secret leakage | Raw tool input/output is logged | Allowlist fields and redact secrets before serialization |
| Unattributed action | Shared or missing actor identity | Require authenticated actor/service identity |
| Broken correlation | Each component invents unrelated IDs | Propagate a workflow correlation ID |
| Log tampering | Logs are writable by the workload being audited | Separate writer and reader permissions and use append-only storage |
| Excessive retention | Logs become a privacy/security liability | Define retention by purpose and data class |
| Clock ambiguity | Host clocks differ | Store UTC timestamps and use a trusted event ordering strategy |
| High-cardinality noise | Every internal operation becomes an event | Log security-relevant state transitions, not arbitrary debug output |

## Design Rules

1. Treat logs as sensitive data.
2. Log decisions and outcomes rather than secrets or complete payloads.
3. Make actor and correlation identity explicit.
4. Separate operational debugging from compliance/security audit records.
5. Define retention and deletion rules before deployment.
6. Test that denied actions generate auditable events.
7. Never treat a hash chain alone as proof of external authenticity.

## References

- OWASP Logging Cheat Sheet: https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html
- NIST AI Risk Management Framework: https://www.nist.gov/itl/ai-risk-management-framework
- Python `hashlib` documentation: https://docs.python.org/3/library/hashlib.html

Evidence status: implementation guidance is grounded in the cited security guidance; no compliance certification or performance claim is made.

## Related Skills

- [Human In Loop](human-in-loop.md)
- [Permission Checking](permission-checking.md)
- [Secret Scanning](secret-scanning.md)

## Changelog

| Date | Version | Change |
|---|---|---|
| 2025-03 | v1 | Initial stub |
| 2026-10 | v2 | Added structured event contract, tamper-evident example, failure modes, and evidence references |
