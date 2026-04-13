![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-07-tool-use-stripe-api.json)

# Stripe API

**Category:** `tool-use`  
**Skill Level:** `advanced`  
**Stability:** `stable`
**Added:** 2025-03

### Description

Process payments, manage subscriptions, create invoices, and retrieve customer data via the Stripe API.

### Example

```python
import stripe
stripe.api_key = STRIPE_KEY

payment_intent = stripe.PaymentIntent.create(
    amount=2000,
    currency='usd',
    payment_method_types=['card'],
)
print(payment_intent.client_secret)
```

### Related Skills

- [Custom API Wrapper](custom-api-wrapper.md)
- [Notification Sending](../04-action-execution/notification-sending.md)
