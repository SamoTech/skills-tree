---
title: "Agent Deception Mechanism Audit"
category: 09-agentic-patterns
level: advanced
stability: experimental
description: "Audit an agent for mechanisms that can produce deceptive behavior, covering sycophancy, unfaithful explanations, and reward-driven misreporting, and record verified findings."
added: "2026-10"
version: v1
related: [reward-hacking-detection, runtime-behavior-baselining]
tags: [deception, audit, alignment]
---
# Agent Deception Mechanism Audit

## Description
Audit an agent for mechanisms that can produce deceptive behavior, covering sycophancy, unfaithful explanations, and reward-driven misreporting, and record verified findings. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- An agent's outputs are trusted by users and deception risk must be measured, not assumed away.
- The outcome would change if inputs were stale, ambiguous, or incomplete.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | agent deception mechanism auditing task context, candidate data, and explicit acceptance criteria. |
| Outputs | A structured record with the decision, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the agent deception mechanism auditing steps in a bounded, checkpointed way.
4. Compare the actual outcome against the acceptance criteria and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Outputs
| Area | Contract |
|---|---|
| Primary | An audit report listing each deception mechanism probed, the probe evidence, and the verified finding with severity. |
| Verification | Recorded checks, deviations, and the evidence links that support the result. |
| Failure | A fail-closed error report naming the failed step and the preserved input state. |

## Runnable Example
```python
def probe_answer(internal, external):
    faithful = internal["reason"] == external["reason"]
    return {"mechanism": "unfaithful-explanation", "detected": not faithful}
assert probe_answer({"reason": "guess"}, {"reason": "verified"})["detected"] is True
assert probe_answer({"reason": "x"}, {"reason": "x"})["detected"] is False
```

## Failure Modes
- Auditing only for explicit lies and ignoring unfaithful self-explanations.
- Designing probes the agent can recognize and answer carefully on.
- Reporting no deception after probes that never exercised the mechanism.
- Treating an internal explanation mismatch as resolved because the external answer looked right.
- Publishing deception findings without the probe methodology for independent check.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- October-2026 agentic-security reporting demands receipts-based auditing of agent deception and unfaithful explanation risks ([public signal](https://www.rockcybermusings.com/p/owasp-state-of-agentic-ai-security-2026))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Reward Hacking Detection](../09-agentic-patterns/reward-hacking-detection.md)
- [Runtime Behavior Baselining](../14-security/runtime-behavior-baselining.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
