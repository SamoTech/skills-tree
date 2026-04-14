---
title: "Stripe API"
category: 07-tool-use
level: intermediate
stability: stable
added: "2025-03"
description: "Apply Stripe API in AI agent workflows."
dependencies:
  - package: stripe
    min_version: "7.0.0"
    tested_version: "15.0.1"
    confidence: verified
code_blocks:
  - id: "example-stripe"
    type: executable
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-07-tool-use-stripe-api.json)

# Stripe API

**Category:** `tool-use`  
**Skill Level:** `intermediate`  
**Stability:** `stable`
**Added:** 2025-03

### Description

Create charges, manage subscriptions, retrieve invoices, and handle payment events via the Stripe Python SDK.

### Example

```python
# pip install stripe
import stripe

stripe.api_key = "sk_test_your_key"

# Create a PaymentIntent
intent = stripe.PaymentIntent.create(
    amount=2000,  # $20.00 in cents
    currency="usd",
    payment_method_types=["card"],
    metadata={"order_id": "order_123"}
)
print(f"PaymentIntent: {intent.id}, status: {intent.status}")

# List recent charges
charges = stripe.Charge.list(limit=5)
for charge in charges.auto_paging_iter():
    print(f"{charge.id}: ${charge.amount/100:.2f} {charge.currency.upper()} — {charge.status}")
```

### Related Skills
- `webhook-call`, `api-call`, `env-vars`, `sendgrid-api`
