# Stripe API

**Category:** `tool-use`  
**Skill Level:** `advanced`  
**Stability:** `stable`

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
