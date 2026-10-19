---
title: "Feature Flag Management Implementation"
category: 05-code
level: advanced
stability: experimental
description: "Implement feature flag evaluation with typed targeting and recorded decisions so that agent behavior changes are gated, observable, and reversible."
added: "2026-10"
version: v1
related: [conditional-branching, config-file-parsing]
tags: [feature-flags, rollout, gating, observability]
---
# Feature Flag Management Implementation

## Description
Implement feature flag evaluation with typed targeting and recorded decisions so that agent behavior changes are gated, observable, and reversible. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- Agent behavior changes must ship behind gates with kill switches instead of deploy-time gambles.
- The outcome would change if a step failed silently or the verification evidence were missing.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | the declared input set, policy thresholds, and explicit acceptance criteria. |
| Outputs | A structured record with the decision, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Define the flag schema with default values, implement evaluation with a recorded decision log, and verify that an unknown flag evaluates to its declared safe default.
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
def evaluate(flags, key, context):
    flag = flags.get(key)
    if flag is None:
        return False
    if "rollout" in flag and context["bucket"] > flag["rollout"]:
        return False
    return bool(flag["enabled"])
f = {"beta": {"enabled": True, "rollout": 50}}
assert evaluate(f, "beta", {"bucket": 10}) and not evaluate(f, "beta", {"bucket": 90})
assert evaluate(f, "missing", {"bucket": 0}) is False
```

## Failure Modes
- An unknown flag raises instead of evaluating to its safe default and takes down the whole evaluation path.
- Flag decisions are evaluated but never logged, so kill-switch forensics have no trail.
- Rollout buckets are computed per request from a random seed, so the same user flips between variants.
- A flag is removed from code while still live in the flag store, and the default silently changes.
- Kill switches are implemented as new flags with their own rollout, adding a failure layer to the emergency path.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- 2026 agent engineering reporting treats gated rollout of behavior changes as standard delivery practice for acting agents (brandon-ta.com, dated October 2026) ([public signal](https://www.brandon-ta.com/blog/ai-agents-where-they-stand-october-2026/))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Conditional Branching](../15-orchestration/conditional-branching.md)
- [Config File Parsing](../01-perception/config-file-parsing.md)

## Changelog
| Version | Date | Notes |
|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
