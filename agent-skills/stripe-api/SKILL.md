---
name: stripe-api
description: Use Stripe APIs for authorized payment and billing operations with idempotency, secret-safe authentication, explicit amounts, and post-action verification.
metadata:
  source: skills/07-tool-use/stripe-api.md
  category: 07-tool-use
---

# Stripe API

## Description
Use Stripe APIs for authorized payment and billing operations with idempotency, secret-safe authentication, explicit amounts, and post-action verification.

## When to Use
Use this capability only when the workflow requires stripe api, the target account or resource is authorized, and the provider contract is documented.

## Inputs / outputs / failure modes

| Area | Guidance |
|---|---|
| Authentication | Keep credentials outside source code and prompts; use least privilege. |
| Scope | Bound the target resource, operation, and result set. |
| Inputs | Validate identifiers, filters, amounts, content, and provider-required fields. |
| Outputs | Preserve structured results and provider identifiers needed downstream. |
| Verification | Re-read or otherwise verify important outcomes and side effects. |
| Safety | Apply authorization, rate limits, and sensitive-data controls. |
| Failure modes | Invalid input, permission denial, rate limit, provider outage, stale state, or malformed response. |

## Runnable Example

```python
import os

request = {
    "capability": "stripe-api",
    "authorized": bool(os.getenv("TOOL_AUTH")),
}
assert request["authorized"]
print("validated tool invocation")
```

## Failure modes
- Hard-coding credentials or placing secrets in tool arguments.
- Assuming provider identifiers or schemas are portable across accounts.
- Performing mutations without authorization and current-state checks.
- Treating a successful API response as proof of the desired business outcome.
- Using unbounded retries, pagination, or result sets.

## Evidence
- Provider documentation: https://docs.stripe.com/api
- Repository schema, Agent Skills validation, security scanning, and quality workflows define local conformance.

## Related
- tool-guardrails
- function-calling
- approval-before-destructive-tools
- input-guardrails
