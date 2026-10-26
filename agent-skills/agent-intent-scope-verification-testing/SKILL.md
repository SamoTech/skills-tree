---
name: agent-intent-scope-verification-testing
description: Test that agent actions stay within the recorded user intent scope by replaying intent-action pairs against a declared scope contract.
metadata:
  source: skills/09-agentic-patterns/agent-intent-scope-verification-testing.md
  category: 09-agentic-patterns
  version: "v1"
---

# Agent Intent Scope Verification Testing

## Description
Test that agent actions stay within the recorded user intent scope by replaying intent-action pairs against a declared scope contract. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- An operator needs this capability to proceed safely and verifiably.
- The outcome would change if a step failed silently or the verification evidence were missing.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | the declared input set, policy thresholds, and explicit acceptance criteria. |
| Outputs | A structured record with the decision, rejected alternatives, and the verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Bind each recorded intent to its declared scope contract, replay the action history against it, and flag every action outside the declared scope as a scope violation.
4. Compare the actual outcome against the acceptance criteria and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Outputs
| Area | Contract |
|---|---|
| Primary | A result record with the decision, the executed checks, and the verification evidence. |
| Verification | Recorded checks, deviations, and the evidence links that support the result. |
| Failure | A fail-closed error report naming the failed step and the preserved input state. |

## Runnable Example
```python
def verify_intent_scope(pairs):
    violations = []
    for p in pairs:
        allowed = set(p["intent_scope"])
        for a in p["actions"]:
            if a not in allowed:
                violations.append({"intent": p["intent"], "action": a})
    return violations

pairs = [{"intent":"buy-milk","intent_scope":["search","add_to_cart","checkout"],"actions":["search","add_to_cart","checkout","read_payment_info"]}]
v = verify_intent_scope(pairs)
assert v == [{"intent":"buy-milk","action":"read_payment_info"}]
```

## Failure Modes
- The scope contract is written after the actions and simply ratifies whatever the agent did.
- Intent is inferred from the action history instead of recorded before execution.
- Scope violations are logged but not enforced and repeat in the next session.
- Multi-step intents inherit the widest scope of any step and the contract never narrows.
- Intent-action pairs are replayed without timestamps so out-of-scope actions are attributed to expired intents.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- Walmart terms require that agents cannot act beyond the shopper intent, making intent-scope verification a published compliance condition (agenticexpo.ai, dated October 23, 2026) ([public signal](https://www.agenticexpo.ai/news/weekly-roundup-23-october-2026))
- The roundup describes customer control through per-agent caps, approval gates, and codified terms as the transferable architecture for non-human shoppers (agenticexpo.ai, dated October 23, 2026) ([public signal](https://www.agenticexpo.ai/news/weekly-roundup-23-october-2026))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [09 Agentic Patterns/purchase Intent Binding Patterns.md](../09-agentic-patterns/purchase-intent-binding-patterns.md.md)
- [09 Agentic Patterns/goal Contract Checking.md](../09-agentic-patterns/goal-contract-checking.md.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
