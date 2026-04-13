---
title: "Human In Loop"
category: 14-security
level: advanced
stability: stable
description: "Apply human in loop in AI agent workflows."
added: "2025-03"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-14-security-human-in-loop.json)

**Category:** Security & Safety
**Skill Level:** Advanced
**Stability:** stable
**Added:** 2025-03

### Description
Pauses agent execution when a decision exceeds a risk threshold and routes it to a human reviewer via Slack, email, or a web dashboard. Resumes or aborts based on the human's response. Implements timeout handling if no response is received.

### Example
```python
import anthropic
import time

client = anthropic.Anthropic()

PENDING_APPROVALS: dict = {}  # In production: use Redis/DB

def request_human_approval(action: str, details: dict, timeout: int = 300) -> bool:
    """Pause execution and await human approval."""
    approval_id = f"approval-{int(time.time())}"
    PENDING_APPROVALS[approval_id] = {"action": action, "details": details, "approved": None}

    # In production: send Slack message / email with approve/reject buttons
    print(f"[HUMAN REVIEW REQUIRED]")
    print(f"Action: {action}")
    print(f"Details: {details}")
    print(f"Approval ID: {approval_id}")
    print(f"Waiting up to {timeout}s for human response...")

    # Simulate waiting loop (real implementation uses webhooks)
    deadline = time.time() + timeout
    while time.time() < deadline:
        approval = PENDING_APPROVALS[approval_id]["approved"]
        if approval is not None:
            return approval
        time.sleep(5)

    print("Timeout: defaulting to DENY")
    return False

def maybe_delete_database(db_name: str) -> None:
    """High-risk action that always requires human approval."""
    approved = request_human_approval(
        action="database_delete",
        details={"database": db_name, "reason": "cleanup old data"}
    )
    if approved:
        print(f"Deleting {db_name}...")
    else:
        print("Action cancelled by human reviewer.")
```

### Related Skills
- [Permission Checking](permission-checking.md)
- [Audit Logging](audit-logging.md)
- [Harm Detection](harm-detection.md)
