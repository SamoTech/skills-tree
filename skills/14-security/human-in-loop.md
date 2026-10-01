---
title: "Human In Loop"
category: 14-security
level: advanced
stability: stable
description: "Pause high-risk agent actions for explicit human approval with deny-by-default timeouts, auditable decisions, and safe resume or abort behavior."
added: "2025-03"
updated: "2026-10"
version: v2
related: [permission-checking, audit-logging, rollback-undo]
---

# Human In Loop

## Description

Human-in-the-loop control inserts an explicit approval boundary before actions whose risk, authority, cost, or irreversibility exceeds an established threshold. The agent should prepare the proposed action and evidence, then wait for a decision from an authorized reviewer.

Approval must be bound to the exact action being approved. A generic approval such as "yes, continue" should not authorize a different action later in the workflow.

## Inputs / Outputs

| Input | Type | Required | Description |
|---|---|---:|---|
| `action` | string | yes | Canonical action identifier |
| `target` | string | yes | Resource or target affected |
| `risk` | string | yes | Policy risk classification |
| `evidence` | dict | no | Facts needed by the reviewer |
| `timeout_seconds` | int | no | Maximum approval wait |

| Output | Type | Description |
|---|---|---|
| `approved` | bool | Explicit approval result |
| `decision_id` | string | Audit correlation identifier |
| `reason` | string | Reviewer decision reason when supplied |

## Runnable Example

```python
from dataclasses import dataclass
import time

@dataclass(frozen=True)
class Approval:
    approved: bool
    decision_id: str
    reason: str

def require_approval(action: str, target: str, timeout: int = 30) -> Approval:
    decision_id = f"approval:{action}:{target}"
    deadline = time.monotonic() + timeout
    # Replace this deterministic demo with an authenticated approval service.
    if time.monotonic() >= deadline:
        return Approval(False, decision_id, "timeout")
    return Approval(False, decision_id, "no reviewer decision in demo")

print(require_approval("account.delete", "acct-42"))
```

The demo deliberately denies by default. A production implementation should use an authenticated, durable approval channel and bind the reviewer decision to an immutable action summary.

## Failure Modes

| Failure | Cause | Mitigation |
|---|---|---|
| Approval replay | Old approval reused for a new action | Bind approval to action, target, parameters, and expiry |
| Wrong reviewer | Reviewer lacks authority | Check reviewer identity and required scope |
| Timeout bypass | Agent continues after timeout | Timeout must produce a deny/escalate state |
| Approval fatigue | Too many low-risk approvals | Use explicit risk thresholds and batch only equivalent safe actions |
| Missing evidence | Reviewer cannot understand the action | Present concise, relevant evidence and expected effects |
| Race condition | Target changes after approval | Revalidate target state immediately before execution |

## Design Rules

- Deny by default on timeout or unavailable approval service.
- Never interpret silence as approval.
- Make approvals single-purpose and time-bounded.
- Re-check permissions and target state after approval.
- Record who approved what, when, and under which policy version.
- Provide an explicit abort path.

## References

- NIST AI Risk Management Framework: https://www.nist.gov/itl/ai-risk-management-framework
- NIST AI RMF FAQs: https://www.nist.gov/itl/ai-risk-management-framework/ai-risk-management-framework-faqs

Evidence status: guidance is based on general AI risk-management and accountability principles; no claim is made that human review alone guarantees safe behavior.

## Related Skills

- [Permission Checking](permission-checking.md)
- [Audit Logging](audit-logging.md)
- [Rollback / Undo](rollback-undo.md)
