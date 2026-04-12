# Human-in-the-Loop Blueprint

**Category:** blueprints | **Stability:** stable | **Version:** v1

## What This Solves

High-stakes agent actions — sending emails, making purchases, deleting data, publishing content — must not execute without human approval. This blueprint adds structured approval gates, escalation paths, and full audit trails to any agent pipeline.

**Use when:**
- Actions are irreversible (send, delete, publish, pay)
- Compliance requires a human sign-off record
- Agent confidence is below a threshold
- The user explicitly configured "always ask"

---

## Architecture

```
  Agent produces action
         │
         ▼
  ┌───────────────┐
  │  Risk Classifier │
  └───────┬───────┘
           │
    ┌─────┴─────┐
    │           │
  low risk    high risk
    │           │
  Auto-run   Approval Gate
             │
    ┌───────┴───────┐
    │               │
  Approve         Reject
    │               │
  Execute        Abort +
  + Audit Log    Explain
```

---

## Full Implementation

```python
import anthropic
import json
from datetime import datetime
from typing import Callable, Optional
from enum import Enum

client = anthropic.Anthropic()

class RiskLevel(Enum):
    LOW = "low"       # Auto-execute
    MEDIUM = "medium" # Log + notify
    HIGH = "high"     # Require explicit approval
    CRITICAL = "critical" # Block, require dual approval

@dataclass
class AgentAction:
    action_type: str         # e.g., "send_email", "delete_file", "api_call"
    description: str         # Human-readable description
    payload: dict            # Action parameters
    risk_level: RiskLevel
    agent_confidence: float  # 0.0–1.0

from dataclasses import dataclass

RISK_CLASSIFIER_SYSTEM = """
You classify the risk level of agent actions. Output JSON:
{
  "risk_level": "low|medium|high|critical",
  "reason": "one sentence explanation",
  "reversible": true/false,
  "estimated_impact": "description of what happens if this goes wrong"
}

Risk guidelines:
- low: read-only, reversible, low-value (search, read file, get API data)
- medium: creates new data, but reversible (create draft, add to list)
- high: sends, publishes, or deletes (send email, post tweet, delete record)
- critical: financial transactions, admin actions, mass operations
"""

def classify_risk(action: dict) -> dict:
    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=256,
        system=RISK_CLASSIFIER_SYSTEM,
        messages=[{"role": "user", "content": f"Action: {json.dumps(action)}"}]
    )
    return json.loads(response.content[0].text)

AUDIT_LOG: list[dict] = []

def log_action(action: dict, decision: str, approver: Optional[str] = None):
    AUDIT_LOG.append({
        "timestamp": datetime.utcnow().isoformat(),
        "action": action,
        "decision": decision,
        "approver": approver,
    })

def request_human_approval(
    action: dict,
    risk_info: dict,
    approval_fn: Callable[[dict, dict], bool]
) -> bool:
    """
    approval_fn: your UI/notification layer.
    Returns True if approved, False if rejected.
    In production: send to Slack, web UI, email, etc.
    """
    print(f"\n⚠️  APPROVAL REQUIRED")
    print(f"   Action  : {action['action_type']}")
    print(f"   Details : {action['description']}")
    print(f"   Risk    : {risk_info['risk_level']} — {risk_info['reason']}")
    print(f"   Reversible: {risk_info['reversible']}")
    print(f"   Impact  : {risk_info['estimated_impact']}")

    return approval_fn(action, risk_info)

def execute_with_hitl(
    action: dict,
    executor: Callable[[dict], any],
    approval_fn: Callable[[dict, dict], bool] = None,
    auto_approve_below: RiskLevel = RiskLevel.MEDIUM,
) -> dict:
    """Main HITL gate. Returns {status, result, audit}."""
    risk_info = classify_risk(action)
    risk_level = RiskLevel(risk_info["risk_level"])

    # Auto-execute low-risk actions
    if risk_level.value <= auto_approve_below.value:
        result = executor(action)
        log_action(action, "auto-approved", approver="system")
        return {"status": "executed", "result": result, "risk": risk_info}

    # High-risk: require human approval
    if approval_fn is None:
        # CLI fallback
        approval_fn = lambda a, r: input("Approve? [y/N]: ").lower() == "y"

    approved = request_human_approval(action, risk_info, approval_fn)

    if approved:
        result = executor(action)
        log_action(action, "human-approved", approver="user")
        return {"status": "executed", "result": result, "risk": risk_info}
    else:
        log_action(action, "rejected", approver="user")
        return {"status": "rejected", "result": None, "risk": risk_info}

# Example
if __name__ == "__main__":
    action = {
        "action_type": "send_email",
        "description": "Send weekly report to 150 subscribers",
        "payload": {"to": "list@company.com", "subject": "Weekly Report", "body": "..."},
    }

    def fake_send(action): return "email_sent_id_abc123"

    result = execute_with_hitl(action, executor=fake_send)
    print(f"Result: {result['status']}")
    print(f"Audit log: {AUDIT_LOG}")
```

---

## Approval Channels

```python
# Slack approval
def slack_approval(action: dict, risk: dict) -> bool:
    import httpx
    webhook = "https://hooks.slack.com/services/..."
    msg = f"⚠️ Agent wants to: *{action['description']}*\nRisk: {risk['risk_level']}"
    httpx.post(webhook, json={"text": msg})
    # In production: block until Slack button click callback
    return True  # simplified

# Email approval
def email_approval(action: dict, risk: dict) -> bool:
    # Send email with approve/reject links containing signed tokens
    # Block until token is consumed via webhook
    pass
```

---

## Failure Modes

| Failure | Mitigation |
|---|---|
| Approval request ignored | Set timeout → auto-reject after N minutes |
| Risk misclassification | Add explicit action type allowlist/blocklist |
| Audit log loss on crash | Write audit to append-only DB immediately |
| Approval fatigue | Auto-approve repetitive low-risk patterns after 3 human approvals |

---

## Related

- `blueprints/self-healing-agent.md` — Recovery when an approved action fails
- `skills/15-orchestration/escalation.md` · `skills/14-security/audit-logs.md`

## Changelog

- **v1** (2026-04) — Initial blueprint: risk classifier, approval gate, audit log
