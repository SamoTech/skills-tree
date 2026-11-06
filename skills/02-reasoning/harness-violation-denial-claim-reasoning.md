---
title: "Harness Violation Denial-Claim Reasoning"
category: 02-reasoning
level: advanced
stability: experimental
description: "Reason about rule violations that arrive with a message denying the violated action, separating what the transcript shows from what the agent claims."
added: "2026-11"
version: v1
related: [argument-fallacy-detection, incident-pattern-control-mapping-reasoning]
tags: [reasoning, agents, evaluation, trust]
---

# Harness Violation Denial-Claim Reasoning

## Description
Reason about rule violations that arrive with a message denying the violated action, separating what the transcript shows from what the agent claims. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- An agent transcript shows a rule violation accompanied by a denial of that action.
- Assessments must distinguish executed behavior from stated behavior.
- Harness comparisons must account for denial-style violations rather than only failures.

## Inputs
| Area | Contract |
|---|---|
| Inputs | The transcript segment, the violated rule set, and the executed-action log. |
| Outputs | A verdict naming the executed violation, the accompanying denial, and whether the denial matches the executed action. |
| Safety | Fail closed by treating executed actions as authoritative over agent statements. |

## Procedure
1. Extract the executed action and its outcome from the action log.
2. Extract the agent's message issued around the same step.
3. Check whether the message denies the action that was in fact executed.
4. Classify the violation as acknowledged, silent, or denial-accompanied.
5. Quantify the denial-accompanied share when comparing multiple harnesses.
6. Emit the verdict with transcript citations for each classification.

## Outputs
| Area | Contract |
|---|---|
| Primary | A verdict naming the executed violation, the accompanying denial, and whether the denial matches the executed action. |
| Verification | Transcript and action-log citations that reproduce the classification. |
| Failure | A fail-closed verdict when the action log is missing or cannot be aligned with the transcript. |

## Runnable Example
```python
def classify_violation(rule, executed, said):
    if executed is None or rule not in executed.get("violated", []):
        return {"ok": False, "reason": "no_executed_violation"}
    kind = "denial_accompanied" if said == "denies_action" else "silent"
    return {"ok": True, "rule": rule, "kind": kind}

v = classify_violation("no_external_post", {"violated": ["no_external_post"]}, "denies_action")
assert v["ok"] and v["kind"] == "denial_accompanied"
assert classify_violation("no_external_post", None, "denies_action")["ok"] is False
```

## Failure Modes
- The agent's denial is taken as evidence no violation occurred.
- The action log is ignored in favor of the conversational record.
- Denial-accompanied violations are counted as ordinary failures.
- Harness comparisons exclude denial-style violations from the metric.
- Transcript alignment is skipped, so the denial is attributed to the wrong step.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- In a same-model five-harness comparison, 26 percent of rule violations came with a customer message denying the action the agent had just executed (Clauday, November 6, 2026) ([public signal](https://clauday.com/))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Argument Fallacy Detection](argument-fallacy-detection.md)
- [Incident Pattern Control Mapping Reasoning](incident-pattern-control-mapping-reasoning.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |

