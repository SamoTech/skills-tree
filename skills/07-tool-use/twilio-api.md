---
title: "Twilio API"
category: 07-tool-use
level: intermediate
stability: stable
description: "Use Twilio APIs for authorized messaging and communications with validated destinations, rate controls, secret-safe credentials, and delivery-state handling."
added: "2026-09"
related: [07-tool-use, 14-security]
---

# Twilio API

## Description
Use Twilio APIs for authorized messaging and communications with validated destinations, rate controls, secret-safe credentials, and delivery-state handling.

## When to Use
Use this capability only when the workflow requires twilio api, the target account or resource is authorized, and the provider contract is documented.

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
    "capability": "twilio-api",
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
- Provider documentation: https://www.twilio.com/docs/usage/api
- Repository schema, Agent Skills validation, security scanning, and quality workflows define local conformance.

## Related
- tool-guardrails
- function-calling
- approval-before-destructive-tools
- input-guardrails
