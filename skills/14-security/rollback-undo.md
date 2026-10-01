---
title: "Rollback / Undo"
category: 14-security
level: advanced
stability: stable
description: "Make high-impact agent mutations reversible with explicit snapshots, transaction boundaries, postcondition checks, and safe rollback semantics."
added: "2025-03"
updated: "2026-10"
version: v2
related: [audit-logging, permission-checking, human-in-loop]
---

# Rollback / Undo

## Description

Rollback protects against failed or undesired agent actions by preserving enough state to restore a known-good condition. It is appropriate for multi-step mutations where partial completion could leave inconsistent state.

Rollback is not equivalent to deletion or backup. A rollback design must define what state is captured, when it is captured, which operations are reversible, and how concurrent changes are handled.

## Inputs / Outputs

| Input | Type | Required | Description |
|---|---|---:|---|
| `action` | callable/object | yes | Reversible mutation |
| `snapshot` | object | yes | State required to restore the prior state |
| `expected_state` | object | no | Preconditions/postconditions |
| `policy` | dict | no | Retry, timeout, and recovery rules |

| Output | Type | Description |
|---|---|---:|---|
| `status` | string | `committed` or `rolled_back` |
| `error` | string | Failure reason when recovery occurs |
| `audit_id` | string | Correlation identifier |

## Runnable Example

```python
from dataclasses import dataclass

@dataclass
class Document:
    content: str

class Transaction:
    def __init__(self, document: Document):
        self.document = document
        self.before = document.content

    def commit(self, new_content: str) -> None:
        self.document.content = new_content

    def rollback(self) -> None:
        self.document.content = self.before

doc = Document("safe")
tx = Transaction(doc)
tx.commit("new")
tx.rollback()
print(doc.content)
```

The example is in-memory and does not address concurrent writers. Production systems need transactional storage, version checks, or compensating operations appropriate to the target system.

## Failure Modes

| Failure | Cause | Mitigation |
|---|---|---|
| Partial rollback | Not all side effects are reversible | Use transactions or explicit compensating actions |
| Stale snapshot | Another actor changed state after snapshot | Use version/ETag checks and conflict detection |
| Rollback failure | Recovery path has its own failure | Make recovery observable and escalate to an operator |
| Irreversible side effect | Email/payment/external call cannot be undone | Require approval before execution and use compensating actions |
| Lost snapshot | Snapshot stored in same failure domain | Store recovery state separately with controlled access |
| Silent divergence | State restores but external side effects remain | Verify postconditions and record residual effects |

## Design Rules

- Capture state immediately before mutation.
- Bind rollback to the exact action/version being reverted.
- Prefer native transactions when available.
- Use compensating actions for irreversible external effects.
- Never claim successful rollback without a postcondition check.
- Audit both commit and rollback outcomes.

## References

- OWASP Transaction Authorization guidance: https://cheatsheetseries.owasp.org/cheatsheets/Transaction_Authorization_Cheat_Sheet.html
- Python context manager protocol: https://docs.python.org/3/reference/datamodel.html#context-managers

Evidence status: guidance is grounded in transaction and recovery principles; rollback completeness is system-specific.

## Related Skills

- [Audit Logging](audit-logging.md)
- [Permission Checking](permission-checking.md)
- [Human In Loop](human-in-loop.md)
