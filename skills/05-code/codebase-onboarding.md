---
title: "Codebase Onboarding"
category: 05-code
level: intermediate
stability: experimental
description: "Build a working map of an unfamiliar codebase, including entry points, conventions, hot paths, and test layout, before making changes, using measured signals rather than guessing."
added: "2026-10"
version: v1
related: [code-reading, code-search, ide-integration]
tags: [codebase, onboarding, code]
---

# Codebase Onboarding

## Description
Build a working map of an unfamiliar codebase, including entry points, conventions, hot paths, and test layout, before making changes, using measured signals rather than guessing. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- A task requires codebase onboarding before downstream steps can proceed safely.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for codebase onboarding. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Normalize the task into explicit inputs, constraints, and acceptance criteria.
2. Gather the required evidence and check completeness before proceeding.
3. Apply the codebase onboarding procedure using the declared criteria only.
4. Record the outcome, rejected alternatives, and the reason for each rejection.
5. Verify the result against the acceptance criteria with an independent check.
6. Report the result with evidence, and escalate explicitly when a criterion cannot be met.

## Runnable Example
```python
# Codebase Onboarding: deterministic check
candidates = [{"id": "a", "score": 0.8, "cost": 2}, {"id": "b", "score": 0.95, "cost": 9}]
eligible = [c for c in candidates if c["score"] >= 0.8]
selected = min(eligible, key=lambda c: c["cost"])
assert selected["id"] == "a"
print("selected:", selected["id"])
```

## Failure Modes
- Proceeding with codebase onboarding without the required evidence or inputs.
- Treating an unverified result as verified.
- Silently swallowing errors instead of failing closed with reasons.
- Optimizing the stated metric while violating the stated constraint.
- Losing the audit trail of decisions and rejected alternatives.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Coding agents joining new repositories is a dominant 2026 use case; public coding-agent threads request structured onboarding maps. These are dated public signals, not adoption metrics.

## Related
- code-reading.md
- code-search.md
- ide-integration.md
