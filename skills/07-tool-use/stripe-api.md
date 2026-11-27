---
title: "Stripe API"
category: 07-tool-use
level: intermediate
stability: stable
version: v2
description: "Use Stripe APIs for authorized payment and billing operations with idempotency, secret-safe authentication, explicit amounts, and post-action verification."
added: "2026-09"
related: [tool-guardrails, function-calling, tool-output-validation]
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-07-tool-use-stripe-api.json)

# Stripe API

**Category:** `tool-use`
**Skill Level:** `intermediate`
**Stability:** `stable`
**Added:** 2026-09

### Description

Use Stripe APIs for authorized payment and billing operations with idempotency, secret-safe authentication, explicit amounts, and post-action verification. The invocation is contract-first: least-privilege credentials, bounded scope, validated inputs, and post-action verification instead of trusting acknowledgements.

### Inputs / Outputs

| Direction | Field | Type | Contract |
|---|---|---|---|
| Input | operation | enum | Payment, refund, or customer operation, explicitly authorized |
| Input | amount | object | Exact integer amount in the smallest currency unit with the currency code |
| Output | response | object | Provider object with its id and status preserved |
| Output | verification | object | Retrieve or event check confirming the final state |

### Procedure
1. Confirm the operation and API version against current Stripe documentation.
2. Authenticate with a restricted key scoped to the operation; never log secret keys.
3. Express amounts as integers in the smallest currency unit with an explicit currency.
4. Send an idempotency key on every write so retries cannot double-charge.
5. Verify the final state by retrieving the object or consuming the webhook event, not by trusting the response status alone.
6. Keep payment data out of logs; store only provider identifiers.

### Example

```python
charge = {'amount': 4999, 'currency': 'usd', 'idempotency_key': 'order-42'}
assert isinstance(charge['amount'], int) and charge['amount'] == 4999
assert charge['currency'] == 'usd'
print('amount in smallest currency unit; idempotent retry safe')
```

### Related Skills

- [Tool Guardrails](tool-guardrails.md) - invocation boundaries and least privilege
- [Tool Output Validation](tool-output-validation.md) - validate provider responses before use
- [Approval Before Destructive Tools](../14-security/approval-before-destructive-tools.md) - gate mutating or external-effect operations

## Failure Modes

- Floating-point amounts or missing currency codes.
- Retries without idempotency keys double-charging.
- Logging card data or secret keys.
- Treating a succeeded response as final without the retrieval or event check.

## Changelog
- v2 (2026-11): Structural modernization; added the input/output contract table, a deterministic example, an execution procedure, and corpus-verified related links (replaced the non-corpus input-guardrails reference).
- v1 (2026-09): Initial entry.

## Evidence

- https://agentskills.io/specification
- https://docs.stripe.com/api

Evidence status: implementation guidance only; provider behavior must be checked against current provider documentation; no benchmark claim is made without reproducible evidence.
