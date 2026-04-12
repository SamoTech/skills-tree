---
title: Human-in-the-Loop
category: blueprints
version: v1
stability: stable
---

# Human-in-the-Loop

> Pattern for inserting mandatory human approval gates into agent pipelines — with escalation logic, audit trails, and timeout handling.

## When to Use

- Agent actions are irreversible (send email, charge card, deploy to prod)
- Confidence score falls below threshold
- Regulatory / compliance requirement for human sign-off
- High-cost operations where mistakes are expensive

## Architecture

```
  Agent proposes action
          │
          ▼
  ┌─────────────────┐
  │  Risk Classifier  │
  │  (low/med/high)   │
  └──────┬──────┬────┘
          │        │
         low      med/high
          │        │
    auto-approve   ▼
          │   Approval Queue
          │   (Slack / email / UI)
          │        │
          │   Human reviews
          │    │       │
          │  approve  reject
          │    │       │
          └───┴────────┘
                │
         Execute or abort
                │
         Audit log entry
```

## Implementation

```python
import anthropic
import uuid
import time
from datetime import datetime

client = anthropic.Anthropic()

RISK_SYSTEM = """
Classify the risk of this agent action as low, medium, or high.
Output JSON: {"risk": "low|medium|high", "reason": "..."}
High = irreversible or costly. Medium = reversible but significant. Low = read-only or trivial.
"""

# In production: replace with real queue (Redis, SQS, Supabase)
APPROVAL_QUEUE: dict[str, dict] = {}
AUDIT_LOG: list[dict] = []

def classify_risk(action: str, params: dict) -> dict:
    import json
    resp = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=256,
        system=RISK_SYSTEM,
        messages=[{"role": "user", "content": f"Action: {action}\nParams: {params}"}]
    )
    return json.loads(resp.content[0].text)

def request_approval(action: str, params: dict, requester: str) -> str:
    ticket_id = str(uuid.uuid4())[:8]
    APPROVAL_QUEUE[ticket_id] = {
        "action": action, "params": params, "requester": requester,
        "status": "pending", "created_at": datetime.utcnow().isoformat()
    }
    # In production: send Slack message / email here
    print(f"[APPROVAL NEEDED] Ticket {ticket_id}: {action}")
    return ticket_id

def wait_for_approval(ticket_id: str, timeout_s: int = 300) -> bool:
    deadline = time.time() + timeout_s
    while time.time() < deadline:
        ticket = APPROVAL_QUEUE.get(ticket_id, {})
        if ticket.get("status") == "approved":
            return True
        if ticket.get("status") == "rejected":
            return False
        time.sleep(5)
    # Timeout → auto-reject
    APPROVAL_QUEUE[ticket_id]["status"] = "timeout"
    return False

def execute_with_hitl(action: str, params: dict, executor, requester: str = "agent"):
    risk = classify_risk(action, params)
    log_entry = {"action": action, "params": params, "risk": risk, "ts": datetime.utcnow().isoformat()}

    if risk["risk"] == "low":
        result = executor(action, params)
        AUDIT_LOG.append({**log_entry, "outcome": "auto-approved", "result": str(result)})
        return result

    ticket = request_approval(action, params, requester)
    approved = wait_for_approval(ticket)
    outcome = "approved" if approved else "rejected"
    AUDIT_LOG.append({**log_entry, "outcome": outcome, "ticket": ticket})

    if approved:
        return executor(action, params)
    raise PermissionError(f"Action '{action}' rejected or timed out (ticket {ticket})")
```

## Escalation Tiers

| Risk Level | Auto-approve? | Notify | Timeout |
|---|---|---|---|
| Low | ✅ Yes | No | — |
| Medium | ❌ No | Team lead | 30 min |
| High | ❌ No | Director + legal | 24 h |

## Failure Modes

| Failure | Fix |
|---|---|
| Approver never responds | Timeout → auto-reject with audit entry |
| Risk classifier wrong | Add explicit deny-list for critical action verbs (delete, charge, deploy) |
| Audit log lost | Write to append-only store (S3, Supabase) not in-memory dict |

## Related

- `blueprints/self-healing-agent.md`
- `skills/14-security/audit-logs.md`
- `systems/customer-support-bot.md`

## Changelog

- `v1` (2026-04) — Initial HITL with risk classifier, approval queue, audit log, timeout handling
