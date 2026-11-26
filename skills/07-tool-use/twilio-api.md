---
title: "Twilio API"
category: 07-tool-use
level: intermediate
stability: stable
version: v2
description: "Use Twilio APIs for authorized messaging and communications with validated destinations, rate controls, secret-safe credentials, and delivery-state handling."
added: "2026-09"
related: [tool-guardrails, function-calling, tool-output-validation]
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-07-tool-use-twilio-api.json)

# Twilio API

**Category:** `tool-use`
**Skill Level:** `intermediate`
**Stability:** `stable`
**Added:** 2026-09

### Description

Use Twilio APIs for authorized messaging and communications with validated destinations, rate controls, secret-safe credentials, and delivery-state handling. The invocation is contract-first: least-privilege credentials, bounded scope, validated inputs, and post-action verification instead of trusting acknowledgements.

### Inputs / Outputs

| Direction | Field | Type | Contract |
|---|---|---|---|
| Input | destination | object | E.164-validated recipient number or verified sender identity |
| Input | message | object | Bounded body content and the authorized sending route |
| Output | response | object | Provider message sid and queued status |
| Output | delivery | object | Delivery-state follow-up for important messages |

### Procedure
1. Validate destination numbers in E.164 format before sending.
2. Authenticate with scoped credentials from the authorized channel; never embed them in code.
3. Respect the authorized sending route, sender identity, and regional rules.
4. Bound send rates; batch respectfully and honor provider limits.
5. Track delivery states (queued, sent, delivered, failed) for important messages and act on failed.
6. Keep message content and recipient data out of logs.

### Example

```python
sms = {'to': '+15551234567', 'from_': '+15550001111', 'body': 'Your code expires in 10 minutes'}
assert sms['to'].startswith('+') and len(sms['to']) >= 12
assert len(sms['body']) <= 160
print('E.164 destination validated; body within segment bound')
```

### Related Skills

- [Tool Guardrails](tool-guardrails.md) - invocation boundaries and least privilege
- [Tool Output Validation](tool-output-validation.md) - validate provider responses before use
- [Approval Before Destructive Tools](../14-security/approval-before-destructive-tools.md) - gate mutating or external-effect operations

## Failure Modes

- Sending to unvalidated or mistyped destinations.
- Exceeding rate limits or regional sending rules.
- Hard-coding credentials or logging message content.
- Treating queued as delivered.

## Changelog
- v2 (2026-11): Structural modernization; added the input/output contract table, a deterministic example, an execution procedure, and corpus-verified related links (replaced the non-corpus input-guardrails reference).
- v1 (2026-09): Initial entry.

## Evidence

- https://agentskills.io/specification
- https://www.twilio.com/docs/usage/api

Evidence status: implementation guidance only; provider behavior must be checked against current provider documentation; no benchmark claim is made without reproducible evidence.
