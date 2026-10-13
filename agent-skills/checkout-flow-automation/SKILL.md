---
name: checkout-flow-automation
description: Automate web checkout flows with pre-flight cost checks, explicit payment limits, and post-order verification before considering a purchase complete.
metadata:
  source: skills/11-web/checkout-flow-automation.md
  category: 11-web
  version: "v1"
---

# Checkout Flow Automation

## Description
Automate web checkout flows with pre-flight cost checks, explicit payment limits, and post-order verification before considering a purchase complete. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- a purchase flow must be automated with explicit spend limits and completion checks.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for checkout flow automation work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the checkout flow automation steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def checkout_guard(total, limit, in_stock):
    if not in_stock:
        return 'abort'
    return 'proceed' if total <= limit else 'abort'

assert checkout_guard(49, 100, True) == 'proceed'
assert checkout_guard(150, 100, True) == 'abort'
assert checkout_guard(49, 100, False) == 'abort'
```

## Failure Modes
- Proceeding without a pre-flight total check against the limit.
- Treating a confirmation screen as proof of order success.
- Ignoring currency or tax changes that move the total past the limit.
- Retrying a failed payment without checking for duplicate orders.
- Proceeding when stock disappeared mid-flow.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Guarded checkout automation appears in 2026 commerce-automation requests; this is a dated signal, not an adoption metric.

## Related
- form-filling.md
- web-login.md
- popup-dialog-handling.md
