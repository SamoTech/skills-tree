---
title: "Llm Cost Usage Accounting"
category: 12-data
level: advanced
stability: experimental
description: "Account per-feature LLM token spend by tagging requests with dimensions and reconciling against provider invoices."
added: "2026-10"
version: v1
related: [action-cost-estimation, agent-cost-accounting, tool-token-budget-management]
tags: [llm, cost, usage, accounting]
---
# Llm Cost Usage Accounting

## Description
Account per-feature LLM token spend by tagging requests with dimensions and reconciling against provider invoices. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- A task requires llm cost usage accounting before downstream steps can proceed safely.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for llm cost usage accounting. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the llm cost usage accounting steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def cost(tokens, rate):
    return tokens * rate
def reconcile(billed, ledger):
    return abs(billed - ledger) <= 0.01
assert reconcile(cost(1000, 0.001), 1.0) is True
```

## Failure Modes
- Acting outside the declared task boundary.
- Assuming an estimate or preview equals the verified effect.
- Retrying without preserving state or evidence.
- Using stale inputs as if they were current.
- Reporting success without checking the resulting state.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Token cost attribution per feature and team is a standing 2026 platform engineering request. These are dated public signals, not adoption metrics.

## Related
- action-cost-estimation.md
- agent-cost-accounting.md
- tool-token-budget-management.md
