---
title: "Metric Convergence Refinement Loops"
category: 02-reasoning
level: advanced
stability: experimental
description: "Drive an agent to keep refining a generated artifact until measured differences against a reference recording converge to explicit numeric thresholds."
added: "2026-11"
version: v1
related: [booking-preference-inference, fiction-encoded-behavior-detection]
tags: [refinement-loops, convergence, reasoning, verification]
---
# Metric Convergence Refinement Loops

## Description
Drive an agent to keep refining a generated artifact until measured differences against a reference recording converge to explicit numeric thresholds. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A generated artifact must match a reference within measured tolerances and best-effort single passes keep missing them.
- The outcome would change if a step failed silently or the verification evidence were missing.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | the reference recording, the generated artifact, the numeric comparison metrics, and the convergence thresholds. |
| Outputs | A structured record with the decision, rejected alternatives, and the verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the numeric comparison metrics and the threshold each must reach before the loop may stop.
2. Measure the current artifact against the reference and record every metric value.
3. Apply the largest-gap improvement to the artifact and re-measure after each change.
4. Stop only when all metrics satisfy their thresholds on consecutive measurements.
5. On a stall without convergence, fail closed and report the stuck metrics with their history.
6. Emit a structured result with the metric history, iteration count, and the convergence decision.

## Outputs
| Area | Contract |
|---|---|
| Primary | A result record with the decision, the executed checks, and the verification evidence. |
| Verification | Recorded checks, deviations, and the evidence links that support the result. |
| Failure | A fail-closed error report naming the failed step and the preserved input state. |

## Runnable Example
```python
def refine_step(artifact, reference, thresholds):
    metrics = {k: abs(artifact[k] - reference[k]) for k in thresholds}
    worst = max(metrics, key=lambda k: metrics[k] / thresholds[k])
    if all(metrics[k] <= thresholds[k] for k in thresholds):
        return {"done": True, "metrics": metrics}
    artifact[worst] = reference[worst]
    return {"done": False, "fixed": worst, "metrics": metrics}
ref = {"fps": 30, "chars": 12}
art = {"fps": 24, "chars": 12}
th = {"fps": 2, "chars": 1}
r1 = refine_step(art, ref, th); assert r1["done"] is False and r1["fixed"] == "fps"
r2 = refine_step(art, ref, th); assert r2["done"] is False
art["fps"] = 29
assert refine_step(art, ref, th)["done"] is True
```

## Failure Modes
- The loop stops on the first metric that satisfies its threshold instead of requiring all of them.
- Metrics are redefined mid-loop so earlier measurements cannot be compared.
- The loop runs unbounded with no stall detection and burns budget without convergence.
- Convergence is declared from a single measurement instead of consecutive ones.
- The artifact is hand-edited outside the loop and the metric history no longer explains it.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- the reanimate Claude Code skill that records an animation from a live site or recording, rebuilds it in code, and compares the two so the agent keeps going until the numbers match (Munder Difflin agent-tools daily, dated November 1, 2026) ([public signal](https://munderdiffl.in/blog/agent-tools-today-2026-11-01/))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Booking Preference Inference](booking-preference-inference.md)
- [Fiction Encoded Behavior Detection](fiction-encoded-behavior-detection.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |
