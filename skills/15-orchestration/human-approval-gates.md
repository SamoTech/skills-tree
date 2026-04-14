---
title: "Human Approval Gates"
category: 15-orchestration
level: intermediate
stability: stable
description: "Pause an agent graph before a sensitive node and wait for human approval before continuing."
added: "2026-04"
version: v2
---

# Human Approval Gates
Category: orchestration | Level: intermediate | Stability: stable | Version: v2

## Description
Human approval gates interrupt an agent graph before a designated node (e.g. database write, email send, code deploy) and suspend execution until a human explicitly approves or rejects. In LangGraph, this is implemented with `interrupt_before=["node_name"]` at compile time, combined with a checkpointer. After review, the run is resumed with `graph.invoke(None, config)` or cancelled.

## Inputs
- `interrupt_before`: list of node names where execution should pause
- `checkpointer`: persistent checkpointer (SQLite/Postgres) for durable suspension
- `thread_id`: unique run identifier for the approval workflow
- `approval_decision`: human-provided bool (approve/reject) consumed on resume

## Outputs
- Graph paused at interrupt node with full state accessible for review
- On approval: resumed execution through remaining nodes
- On rejection: graph terminated with rejection recorded in state

## Example
```python
app = graph.compile(
    checkpointer=SqliteSaver(conn),
    interrupt_before=["deploy"]
)
config = {"configurable": {"thread_id": "deploy-42"}}

# Run pauses before 'deploy'
app.invoke({"action": "deploy to prod"}, config)

# Human reviews state
state = app.get_state(config)
print(state.values)  # Show pending action

# Approve and resume
app.invoke(None, config)
```

## Failure Modes
| Cause | Symptom | Mitigation |
|---|---|---|
| Approval request never surfaced to human | Graph waits forever | Build notification layer (email/Slack) triggered on interrupt |
| Human approves stale state | Wrong action executed | Show state diff and timestamp in approval UI |
| No timeout on approval | Indefinite suspension | Add TTL on pending approvals with auto-reject on expiry |

## Prompt Patterns
**Basic:** `"Interrupt before any node that writes to production systems."`

**Chain-of-Thought:** `"Identify all destructive or irreversible actions and add them to interrupt_before."`

**Constrained Output:** `"Resume only after storing the approval decision in the run state for audit."`

## Model Comparison
| Capability | GPT-4o | Claude 3.7 Sonnet | Gemini 2.0 Flash |
|---|---|---|---|
| HITL pattern design | ✅ Strong | ✅ Very Strong | ⚠️ Moderate |
| State inspection advice | ✅ Detailed | ✅ Detailed | ⚠️ Generic |
| LangGraph API accuracy | ✅ High | ✅ High | ⚠️ May hallucinate params |
| Security recommendation quality | ✅ Good | ✅ Strong | ⚠️ Shallow |
| Cost | Moderate | Moderate | Low |

## Related
- `langgraph-checkpointing.md` · `thread-based-resume.md` · `interruptible-agent-flows.md` · `approval-before-destructive-tools.md` · `compliance-review-workflows.md`

## Changelog
- v2 (2026-04): Full expansion
