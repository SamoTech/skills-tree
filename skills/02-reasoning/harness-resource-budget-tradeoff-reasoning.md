---
title: "Harness Resource Budget Tradeoff Reasoning"
category: 02-reasoning
level: advanced
stability: experimental
description: "Reason about the resource cost of an agent harness against the constraints of the host before selecting or running it."
added: "2026-11"
version: v1
related: [model-tier-task-split-reasoning, refusal-scope-appeal-reasoning]
tags: [reasoning, harness, resources, budgeting]
---

# Harness Resource Budget Tradeoff Reasoning

## Description
Reason about the resource cost of an agent harness against the constraints of the host before selecting or running it. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A harness choice must be justified against measured resource use on the target machine rather than feature lists.
- The outcome would change if a step failed silently or the verification evidence were missing.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | the host resource envelope, the candidate harnesses, and their measured or claimed resource figures. |
| Outputs | A structured record with the decision, rejected alternatives, and the verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Declare the host resource envelope for memory, CPU, and disk before comparing harnesses.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Measure or gather the resource figures per harness under representative load and compare with the envelope.
4. Compare the actual outcome against the acceptance criteria and record deviations.
5. Where a figure is a vendor claim without measurement, record it as unverified and test before committing.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Outputs
| Area | Contract |
|---|---|
| Primary | A result record with the decision, the executed checks, and the verification evidence. |
| Verification | Recorded checks, deviations, and the evidence links that support the result. |
| Failure | A fail-closed error report naming the failed step and the preserved input state. |

## Runnable Example
```python
def fits(harness, envelope):
    if harness["ram_mb"] > envelope["ram_mb"]:
        return {"fits": False, "reason": "ram"}
    return {"fits": True, "verified": harness["measured"]}
r = fits({"ram_mb": 512, "measured": False}, {"ram_mb": 1024})
assert r["fits"] is True and r["verified"] is False
```

## Failure Modes
- Order-of-magnitude vendor claims are recorded as measured figures.
- Harness memory is measured at idle instead of under representative load.
- Subscription or provider constraints are discovered only after adoption.
- The budget check is skipped because the session is expected to be short.
- The host envelope is never written down so later runs cannot repeat the comparison.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- Prospero arriving as a native C++ coding harness for Windows, macOS, and Linux whose author says it uses around two orders of magnitude fewer resources than others, with no model provider built in and no Claude subscription support (Munder Difflin agent-tools daily brief, dated November 1, 2026) ([public signal](https://munderdiffl.in/blog/agent-tools-today-2026-11-01/))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Model Tier Task Split Reasoning](model-tier-task-split-reasoning.md)
- [Refusal Scope Appeal Reasoning](refusal-scope-appeal-reasoning.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |
