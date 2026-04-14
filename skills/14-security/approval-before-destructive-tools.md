---
title: "Approval Before Destructive Tools"
category: 14-security
level: intermediate
stability: stable
description: "Require explicit human or automated approval before any agent executes an irreversible tool action."
added: "2026-04"
version: v2
---

# Approval Before Destructive Tools
Category: security | Level: intermediate | Stability: stable | Version: v2

## Description
Destructive tools — database deletes, file overwrites, API calls that send emails or charge customers, infrastructure changes — must never execute based solely on LLM intent. An approval gate enforces a mandatory review step: the agent proposes the action, execution is interrupted, a human or automated policy approves or rejects, and only then does the tool run. This prevents hallucination-driven data loss.

## Inputs
- `tool_call`: proposed tool name and arguments from the agent
- `approval_policy`: function or human reviewer deciding approve/reject
- `interrupt_mechanism`: LangGraph `interrupt_before`, OpenAI guardrail, or custom middleware
- `audit_log`: append-only log recording every decision

## Outputs
- Approved: tool executes, result returned to agent
- Rejected: agent receives structured rejection with reason, can propose alternative

## Example
```python
DESTRUCTIVE = {"delete_records", "send_email", "charge_customer", "drop_table"}

def approval_middleware(tool_name: str, tool_args: dict) -> bool:
    if tool_name in DESTRUCTIVE:
        print(f"[APPROVAL REQUIRED] {tool_name}({tool_args})")
        return input("Approve? (y/n): ").strip().lower() == "y"
    return True  # Auto-approve non-destructive tools
```

## Failure Modes
| Cause | Symptom | Mitigation |
|---|---|---|
| Destructive tool not in blocklist | Auto-executed without approval | Maintain allowlist of safe tools, block everything else by default |
| Approver rubber-stamps requests | No real oversight | Require approver to confirm by typing action name, not just clicking OK |
| Agent bypasses middleware | Approval skipped | Enforce at infrastructure level, not only application code |

## Prompt Patterns
**Basic:** `"Tag all tools that modify or delete data as requiring approval."`

**Chain-of-Thought:** `"For each tool: classify as read/write/delete/irreversible, then assign approval tier."`

**Constrained Output:** `"Default-deny: only tools explicitly allowlisted as safe may execute without human approval."`

## Model Comparison
| Capability | GPT-4o | Claude 3.7 Sonnet | Gemini 2.0 Flash |
|---|---|---|---|
| Risk classification accuracy | ✅ High | ✅ Very High | ⚠️ Moderate |
| Policy design quality | ✅ Good | ✅ Strong | ⚠️ Generic |
| Allowlist recommendation | ✅ Detailed | ✅ Detailed | ⚠️ Vague |
| Audit log design advice | ✅ Good | ✅ Strong | ⚠️ Minimal |
| Cost | Moderate | Moderate | Low |

## Related
- `input-guardrails.md` · `output-guardrails.md` · `tool-review-loops.md` · `human-approval-gates.md` · `tool-permission-scoping.md`

## Changelog
- v2 (2026-04): Full expansion
