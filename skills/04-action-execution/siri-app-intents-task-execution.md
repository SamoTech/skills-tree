---
title: "Siri App Intents Task Execution"
category: 04-action-execution
level: advanced
stability: experimental
description: "Execute developer-defined Siri tasks through App Intents by binding each intent to a declared app capability and confirming results."
added: "2026-11"
version: v1
related: [http-request, long-running-action-monitoring]
tags: [execution, siri, intents, mobile]
---
# Siri App Intents Task Execution

## Description
Execute developer-defined Siri tasks through App Intents by binding each intent to a declared app capability and confirming results. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A developer exposes app capabilities to Siri through App Intents.
- Each voice-invoked intent must bind to a declared capability.
- Execution results must be confirmed to the invoking user.

## Inputs
| Area | Contract |
|---|---|
| Inputs | The declared intent catalog, the voice invocation, and the app capability handlers. |
| Outputs | An executed Siri intent naming the declared capability, parameters, and confirmed result. |
| Safety | Fail closed by refusing undeclared intents even when a handler exists for them. |

## Procedure
1. Load the declared intent catalog for the app.
2. Parse the voice invocation into an intent name and parameters.
3. Check that the intent is declared before dispatching.
4. Dispatch to the matching capability handler and capture the result.
5. Confirm the result against the declared intent contract.
6. Emit the executed intent with its confirmation and recorded handler output.

## Outputs
| Area | Contract |
|---|---|
| Primary | An executed Siri intent naming the declared capability, parameters, and confirmed result. |
| Verification | Recorded handler outputs and contract checks that reproduce the confirmation. |
| Failure | A fail-closed report naming the undeclared intent and the refused dispatch. |

## Runnable Example
```python
def dispatch(catalog, invocation, handlers):
    name, params = invocation["intent"], invocation["params"]
    if name not in catalog:
        return {"ok": False, "refused": name}
    result = handlers[name](params)
    return {"ok": result == catalog[name]["expected"], "result": result}
cat = {"send-msg": {"expected": "sent"}}
hs = {"send-msg": lambda p: "sent"}
assert dispatch(cat, {"intent": "send-msg", "params": {}}, hs)["ok"] is True
assert dispatch(cat, {"intent": "read-mail", "params": {}}, hs)["ok"] is False
```

## Failure Modes
- A handler is dispatched for an intent missing from the declared catalog.
- The result is assumed successful without a contract check.
- Parameters are passed through unvalidated to the handler.
- A failed confirmation is retried silently until it passes.
- The user is not told the execution result.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- Apple opened Siri AI to all developers via the App Intents preview, letting apps expose capabilities to Siri (AIBriefs AI News Today, dated November 5, 2026) ([public signal](https://aibriefs.news/ai-news-today))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [HTTP Request](http-request.md)
- [Long Running Action Monitoring](long-running-action-monitoring.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |
