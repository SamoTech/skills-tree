---
title: "Adversarial Reasoning"
category: 02-reasoning
level: intermediate
stability: experimental
description: "Generate the strongest counterarguments and attack paths against a plan or claim before committing, using red-team perspectives with explicit severity and rebuttal steps."
added: "2026-10"
version: v1
related: [risk-assessment, self-correction, threat-modeling]
tags: [adversarial, reasoning, reasoning]
---
# Adversarial Reasoning

## Description
Generate the strongest counterarguments and attack paths against a plan or claim before committing, using red-team perspectives with explicit severity and rebuttal steps. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- A task requires adversarial reasoning before downstream steps can proceed safely.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for adversarial reasoning. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Normalize the task into explicit inputs, constraints, and acceptance criteria.
2. Gather the required evidence and check completeness before proceeding.
3. Apply the adversarial reasoning procedure using the declared criteria only.
4. Record the outcome, rejected alternatives, and the reason for each rejection.
5. Verify the result against the acceptance criteria with an independent check.
6. Report the result with evidence, and escalate explicitly when a criterion cannot be met.

## Runnable Example
```python
# Adversarial Reasoning: deterministic check
allowed = {"idle": {"running"}, "running": {"done", "failed"}, "failed": {"idle"}}

def transition(state, nxt):
    return nxt in allowed.get(state, set())

assert transition("idle", "running")
assert not transition("idle", "done")
print("transitions checked")
```

## Failure Modes
- Proceeding with adversarial reasoning without the required evidence or inputs.
- Treating an unverified result as verified.
- Silently swallowing errors instead of failing closed with reasons.
- Optimizing the stated metric while violating the stated constraint.
- Losing the audit trail of decisions and rejected alternatives.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Agent red-teaming is a named 2026 security practice; OWASP-style agentic guidance recommends structured adversarial review of agent plans. These are dated public signals, not adoption metrics.

## Related
- risk-assessment.md
- self-correction.md
- threat-modeling.md
