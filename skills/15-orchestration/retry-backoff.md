---
title: "Retry Backoff"
category: 15-orchestration
level: advanced
stability: stable
version: v2
description: "Retry transient workflow failures using explicit retryable conditions, attempt limits, and backoff policy."
added: "2025-03"
related: [idempotency-keys, circuit-breaking]
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-15-orchestration-retry-backoff.json)

# Retry Backoff

**Category:** `orchestration`
**Skill Level:** `advanced`
**Stability:** `stable`
**Added:** 2025-03

### Description

Retry transient workflow failures using explicit retryable conditions, attempt limits, and backoff policy. The orchestration step is contract-first: validate state and inputs before acting, and verify the resulting state transition instead of trusting acknowledgements.

### Inputs / Outputs

| Direction | Field | Type | Contract |
|---|---|---|---|
| Input | failure | object | The failed operation with its error class and idempotency key |
| Input | policy | object | Retryable error classes, attempt limit, and backoff schedule |
| Output | decision | enum | retry, escalate, or abort, with the attempt number |
| Output | side_effect_check | object | Confirmation the operation is idempotent or effects are bounded |

### Procedure
1. Classify the failure against the declared retryable error classes; never retry unclassified errors.
2. Verify the operation is idempotent or its side effects are bounded before repeating it.
3. Apply the declared backoff schedule with a deterministic attempt limit.
4. Record each attempt with its attempt number, delay, and outcome.
5. Escalate or abort at the limit instead of resetting the counter.
6. Report the final decision with the attempt history so the retry behavior is auditable.

### Example

```python
policy = {'retryable': ['timeout', '5xx'], 'max_attempts': 3, 'backoff_s': [1, 2]}
attempts = [{'n': 1, 'err': 'timeout'}, {'n': 2, 'err': 'timeout'}]
last = attempts[-1]
decision = 'retry' if last['err'] in policy['retryable'] and len(attempts) < policy['max_attempts'] else 'escalate'
next_delay = policy['backoff_s'][len(attempts) - 1]
assert decision == 'retry' and next_delay == 2 and len(attempts) < policy['max_attempts']
print({'decision': decision, 'attempt': len(attempts) + 1, 'delay_s': next_delay})
```

### Related Skills

- [Idempotency Keys](idempotency-keys.md) - safe repetition of operations
- [Circuit Breaking](circuit-breaking.md) - stop hammering a failing dependency
- [Agent Pool Autoscaling](agent-pool-autoscaling.md) - capacity response to sustained retries

## Failure Modes

- Retrying a non-idempotent operation and duplicating its side effects.
- Retrying permanent failures (4xx-class errors) as if transient.
- Unbounded attempts or a reset backoff counter.
- Escalation never happening because the limit is never checked.

## Changelog
- v2 (2026-11): Structural modernization; added the input/output contract table, a skill-specific execution procedure, a deterministic example, and corpus-verified related links (replaced the unresolvable cross-category related references).
- v1 (2025-03): Initial entry.

## Evidence

- https://agentskills.io/specification

Evidence status: implementation guidance only; runtime behavior must be checked against the executing framework's documentation; no benchmark claim is made without reproducible evidence.
