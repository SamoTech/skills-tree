---
title: "Compliance Review Workflows"
category: 16-domain-specific
level: advanced
stability: stable
description: "Design agent workflows that enforce multi-step regulatory and policy review before finalising outputs."
added: "2026-04"
version: v2
---

# Compliance Review Workflows
Category: domain-specific | Level: advanced | Stability: stable | Version: v2

## Description
Compliance review workflows embed mandatory review checkpoints into agent pipelines for regulated domains: financial advice, medical recommendations, legal documents, or marketing copy. The agent drafts content, an interrupt gate surfaces it for compliance review (human or automated policy engine), and execution continues only after sign-off. Full audit trails are maintained for regulatory accountability.

## Inputs
- `draft_output`: agent-generated content requiring review
- `compliance_policy`: rules the content must satisfy (regulatory, legal, brand)
- `reviewer`: human compliance officer or automated policy LLM
- `interrupt_before`: LangGraph node list for compliance checkpoints
- `audit_store`: append-only log with reviewer ID, timestamp, decision, notes

## Outputs
- Approved content returned to end user
- Rejected content returned to agent with specific failure reasons for revision
- Immutable audit log entry created for every review decision

## Example
```python
def compliance_check_node(state):
    draft = state["draft"]
    # Automated policy check
    violations = policy_engine.check(draft)
    if violations:
        return {"status": "rejected", "violations": violations}
    return {"status": "pending_human_review"}

def human_review_node(state):
    decision = interrupt({
        "draft": state["draft"],
        "auto_check": state["status"]
    })
    return {"approved": decision["approved"], "reviewer_id": decision["reviewer_id"]}
```

## Failure Modes
| Cause | Symptom | Mitigation |
|---|---|---|
| Policy engine misses jurisdiction-specific rules | Non-compliant content approved | Maintain per-jurisdiction rule sets, not one global policy |
| Reviewer approves without reading | Liability exposure | Require reviewers to annotate specific sections they approved |
| Audit log tampered or deleted | No evidence for audit | Use append-only, cryptographically signed audit store |

## Prompt Patterns
**Basic:** `"Draft the document, then pause for compliance review before sending."`

**Chain-of-Thought:** `"Identify all regulatory requirements → generate compliant draft → run automated checks → route for human sign-off."`

**Constrained Output:** `"Never finalise or send output without a recorded approval decision in the audit log."`

## Model Comparison
| Capability | GPT-4o | Claude 3.7 Sonnet | Gemini 2.0 Flash |
|---|---|---|---|
| Regulatory content quality | ✅ Strong | ✅ Very Strong | ⚠️ Moderate |
| Policy violation detection | ✅ Good | ✅ Strong | ⚠️ Misses edge cases |
| Audit trail design advice | ✅ Detailed | ✅ Very Detailed | ⚠️ Basic |
| Multi-jurisdiction awareness | ✅ Good | ✅ Strong | ⚠️ US-centric |
| Cost | Moderate | Moderate | Low |

## Related
- `human-approval-gates.md` · `approval-before-destructive-tools.md` · `interruptible-agent-flows.md` · `output-guardrails.md`

## Changelog
- v2 (2026-04): Full expansion
