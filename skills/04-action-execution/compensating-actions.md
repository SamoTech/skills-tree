---
title: "Compensating Actions"
category: 04-action-execution
level: intermediate
stability: experimental
description: "Design undo for side effects that cannot be transactional — reverse operations, saga compensation in reverse order, and recorded forward-recovery paths for each step."
added: "2026-10"
version: v1
related: ["database-write", "file-delete"]
---

# Compensating Actions

Category: Action Execution | Level: intermediate | Stability: experimental | Version: v1

## Description

Some operations cannot be wrapped in a transaction: money moves between systems, messages leave, external state changes. When one step in a chain fails, earlier effects must be reversed — and that reversal needs to be designed, not improvised. This skill maps each step of a multi-system workflow to its compensating action and records what happens when compensation itself fails.

## When to Use

Use when a workflow spans multiple systems without a shared transaction — order plus payment plus shipping, provision plus notify — and partial failure must leave a coherent state.

Do not assume every step can be undone; some can only be acknowledged and corrected, and that difference belongs in the design.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `workflow` | `list` | Yes | Ordered steps with their side effects |
| `compensations` | `map` | Yes | Reverse action per step, or explicit not-compensable |
| `policy` | `map` | No | Forward-recovery and manual-intervention rules |

## Procedure

1. List the workflow steps with their side effects before writing any of them; compensation design needs the full picture.
2. For each step, define its compensating action — the reverse operation, an acknowledge-and-correct path, or explicit not-compensable.
3. Define failure handling as a saga: on failure at a given step, run compensations for all earlier steps in reverse order.
4. Record semantic invariants — what the compensations must restore in meaning, not just mechanics — and check them after recovery.
5. Plan for compensation failure: retry the compensation, then fall back to a recorded manual-intervention path.
6. Log forward progress for steps that cannot be reversed, so operators see what was done rather than guessing.

## Outputs

| Output | Type | Description |
|---|---|---|
| `compensation_plan` | `map` | Per-step reverse actions and their order |
| `invariants` | `list` | What the recovery must restore |
| `recovery_log` | `list` | Compensations attempted, with outcomes |

## Runnable Example

```python
def run_saga(steps, compensations):
    done = []
    for step in steps:
        try:
            step["action"]()
            done.append(step["name"])
        except Exception as err:
            log = [f"failed at {step[chr(110)+chr(97)+chr(109)+chr(101)]}: {err}"]
            for prev in reversed(done):
                compensations[prev]()
                log.append(f"compensated {prev}")
            return {"status": "rolled-back", "log": log}
    return {"status": "completed", "steps": done}

def charge():
    raise RuntimeError("payment gateway down")

steps = [
    {"name": "reserve", "action": lambda: print("reserved")},
    {"name": "charge", "action": charge},
    {"name": "ship", "action": lambda: print("shipped")},
]
compensations = {"reserve": lambda: print("released reservation")}
print(run_saga(steps, compensations))
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Improvised undo | Reversal is invented during the incident | Design compensations before the chain runs |
| Uncompensable silence | Irreversible steps are not marked | Mark not-compensable steps explicitly |
| Compensation failure | Undo itself fails with no fallback | Retry, then route to a recorded manual path |
| Lost invariants | Recovery restores mechanics but not meaning | Check semantic invariants after recovery |
| Phantom success | A step is reported done but never landed | Verify each compensation effect instead of assuming |

## Security and Authority Boundary

Compensating actions carry the same authority as the actions they reverse — a refund moves money, an unprovision removes access. Scope compensation credentials narrowly, log every compensation in an operator-visible record, and treat unexpected compensation triggers as an audit event.

## Evidence

This skill is grounded in dated public implementation references:

1. The saga pattern description for distributed transactions (https://microservices.io/patterns/data/saga.html).
2. Wikipedia's overview of compensating transactions (https://en.wikipedia.org/wiki/Compensating_transaction).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Database Write](database-write.md) — the local transactional path that chains try to emulate.
- [File Delete](file-delete.md) — the destructive primitive often used as a compensation.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
