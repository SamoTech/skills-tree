---
title: "SendGrid API"
category: 07-tool-use
level: intermediate
stability: stable
version: v2
description: "Send authorized transactional email with validated recipients, secret-safe authentication, and delivery-state verification."
added: "2026-09"
related: [tool-guardrails, function-calling, tool-output-validation]
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-07-tool-use-sendgrid-api.json)

# SendGrid API

**Category:** `tool-use`
**Skill Level:** `intermediate`
**Stability:** `stable`
**Added:** 2026-09

### Description

Send authorized transactional email with validated recipients, secret-safe authentication, and delivery-state verification. The invocation is contract-first: least-privilege credentials, bounded scope, validated inputs, and post-action verification instead of trusting acknowledgements.

### Inputs / Outputs

| Direction | Field | Type | Contract |
|---|---|---|---|
| Input | message | object | Validated sender, recipients, subject, and template/content payload |
| Input | authorization | reference | Least-privilege API key reference; never an inline secret |
| Output | response | object | Provider message id and accepted status |
| Output | delivery | object | Delivery-state follow-up evidence for important sends |

### Procedure
1. Validate recipients and sender domain before composing the send.
2. Authenticate with a scoped API key from the authorized channel; never log it.
3. Use templates or structured content with validated personalization fields.
4. Send with an idempotency discipline so retries cannot duplicate messages.
5. Check the delivery state for important sends instead of trusting the accepted status.
6. Keep recipient data out of logs; minimize retention.

### Example

```python
msg = {'to': ['user@example.com'], 'subject': 'Receipt', 'template_id': 'd-123', 'idempotency_key': 'ord-9'}
assert all('@' in r for r in msg['to'])
assert msg['idempotency_key'] != ''
print('recipients validated; retry-safe idempotency key present')
```

### Related Skills

- [Tool Guardrails](tool-guardrails.md) - invocation boundaries and least privilege
- [Tool Output Validation](tool-output-validation.md) - validate provider responses before use
- [Approval Before Destructive Tools](../14-security/approval-before-destructive-tools.md) - gate mutating or external-effect operations

## Failure Modes

- Hard-coding the API key or exposing it in logs.
- Retries without idempotency duplicating messages.
- Sending to unvalidated recipient lists.
- Treating an accepted status as delivered.

## Changelog
- v2 (2026-11): Structural modernization; added the input/output contract table, a deterministic example, an execution procedure, and corpus-verified related links (replaced the non-corpus input-guardrails reference).
- v1 (2026-09): Initial entry.

## Evidence

- https://agentskills.io/specification

Evidence status: implementation guidance only; provider behavior must be checked against current provider documentation; no benchmark claim is made without reproducible evidence.
