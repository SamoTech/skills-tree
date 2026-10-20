---
title: "Computer Use Capability Regression Testing"
category: 05-code
level: advanced
stability: experimental
description: "Regression-test computer-use capabilities against a fixed scenario grid so UI control changes are caught before release rather than in production."
added: "2026-10"
version: v1
related: [agent-tool-call-replay-testing, regression-window-bisection-automation]
tags: [regression-testing, computer-use, baselines, capability]
---
# Computer Use Capability Regression Testing

## Description
Regression-test computer-use capabilities against a fixed scenario grid so UI control changes are caught before release rather than in production. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A model or harness update may have changed how the agent drives real applications and the capability must be re-verified.
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
3. Run the fixed scenario grid against the candidate, compare each scenario's action trace with the recorded baseline, and emit a regression report naming every scenario that drifted beyond tolerance.
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
def regress(baseline, current, tol=0):
    drifted = [k for k in baseline if baseline[k] != current.get(k)]
    return drifted if len(drifted) > tol else []
b = {"login": "ok", "checkout": "ok"}
c = {"login": "ok", "checkout": "timeout"}
assert regress(b, c) == ["checkout"]
```

## Failure Modes
- Scenarios are re-authored each run and no stable baseline exists.
- Screenshots change trivially and pixel diffing floods the report with noise.
- Only happy-path scenarios run and failure recovery is never re-verified.
- Scenario outcomes are judged ad hoc instead of by recorded criteria.
- The regression report names failing scenarios without traces and cannot be reproduced.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- 2026 Anthropic ships Claude Opus 5.5 with computer use as a flagship capability, making regression grids for UI control a standing need (anthropic.com, dated September 2026) ([public signal](https://www.anthropic.com/claude-opus-5-5))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Agent Tool Call Replay Testing](../05-code/agent-tool-call-replay-testing.md)
- [Regression Window Bisection Automation](../05-code/regression-window-bisection-automation.md)

## Changelog
| Version | Date | Notes |
|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
