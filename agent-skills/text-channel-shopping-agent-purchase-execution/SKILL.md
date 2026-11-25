---
name: text-channel-shopping-agent-purchase-execution
description: Execute product search, cart mutation, and purchase steps through a text-message shopping agent with idempotent, confirmable actions.
metadata:
  source: skills/04-action-execution/text-channel-shopping-agent-purchase-execution.md
  category: 04-action-execution
  version: "v1"
---

# Text Channel Shopping Agent Purchase Execution

## Description
Execute product search, cart mutation, and purchase steps through a text-message shopping agent with idempotent, confirmable actions. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A shopping agent acts on text-message instructions.
- A purchase step needs explicit authorization and idempotency.
- A support review must reconstruct what the agent executed.

## Inputs
| Area | Contract |
|---|---|
| Inputs | The message thread, the catalog service contract, and the purchase authorization. |
| Outputs | An execution record naming each action, its idempotency key, and its confirmation state. |
| Safety | Fail closed by refusing purchases without an explicit authorization in the thread. |

## Procedure
1. Parse the message into a bounded intent with product, quantity, and action.
2. Resolve the intent against the catalog contract.
3. Assign an idempotency key to each cart mutation.
4. Execute the mutation and record the service response.
5. Collect the purchase authorization and verify it against the recorded cart state.
6. Emit the execution record with confirmations and any withheld steps.

## Outputs
| Area | Contract |
|---|---|
| Primary | An execution record naming each action, its idempotency key, and its confirmation state. |
| Verification | The recorded inputs and intermediate values that reproduce the primary output from the runnable example. |
| Failure | A fail-closed hold naming the unmet precondition and the withheld primary output. |

## Runnable Example
```python
def execute_step(messages, cart, authorized):
    if not authorized:
        return {"ok": False, "reason": "authorization_missing"}
    key = messages[-1]["id"]
    before = len(cart["items"])
    cart["items"].append({"sku": messages[-1]["sku"], "key": key})
    return {"ok": True, "idempotent": len(cart["items"]) == before + 1, "key": key}

cart = {"items": []}
msgs = [{"id": "m1", "sku": "sku-9"}]
r = execute_step(msgs, cart, True)
assert r["ok"] and r["key"] == "m1"
assert execute_step(msgs, cart, False)["reason"] == "authorization_missing"
```

## Failure Modes
- Purchases proceed without an explicit authorization in the thread..
- Cart mutations run without idempotency keys and double on retries..
- Parsed intents are trusted without catalog resolution..
- Service responses are not recorded with each action..
- Withheld steps are retried until they succeed..

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- Amazon began rolling out a text-message interface for its Alexa AI agent that searches products, adds items to a cart, and completes purchases for selected US customers (AI Agent News Today, November 8, 2026) ([public signal](https://aiagentstore.ai/ai-agent-news/daily/2026-11-08))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Http Request](http-request.md)
- [Batch Processing](batch-processing.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |
