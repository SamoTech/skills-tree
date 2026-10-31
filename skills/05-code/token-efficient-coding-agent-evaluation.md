---
title: "Token Efficient Coding Agent Evaluation"
category: 05-code
level: advanced
stability: experimental
description: "Evaluate coding agents on tokens consumed per solved task so selection reflects efficiency and not solve rate alone."
added: "2026-10"
version: v1
related: [rust-no-std-ml-engine-implementation, inference-efficiency-claim-verification]
tags: [token-efficiency, evaluation, coding, benchmarks]
---
# Token Efficient Coding Agent Evaluation

## Description
Evaluate coding agents on tokens consumed per solved task so selection reflects efficiency and not solve rate alone. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A team compares coding agents and must weight token consumption per solved task to control cost at scale rather than reading only solve percentages.
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
3. Normalize benchmark records to solved tasks and tokens consumed, then derive tokens per solved task and record the efficiency gain relative to the declared baseline.
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
def tokens_per_solved_task(total_tokens, solved_tasks):
    return round(total_tokens / solved_tasks, 1) if solved_tasks else None
def efficiency_gain(base, candidate):
    return round((base - candidate) / base, 3)
assert tokens_per_solved_task(4700, 10) == 470.0
assert efficiency_gain(100, 53) == 0.47
```

## Failure Modes
- Unsolved task tokens are excluded and the efficient agent only looks efficient on easy tasks.
- Tokens per task is averaged across heterogeneous benchmarks with different task costs.
- Efficiency is claimed without a declared baseline and the gain number is unverifiable.
- Cost is computed at one price point and the ranking flips under the current contract rates.
- The solve criterion is loosened to raise the solved count and the ratio silently improves.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- the Mistral Large 4 release reports matching a frontier coding model on the Artificial Analysis Coding Agent Index while consuming 47 percent fewer generation tokens (blog.luandnh.com AI Daily Digest, dated October 30, 2026) ([public signal](https://blog.luandnh.com/en/ai-daily/2026-10-30/))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Rust No Std Ml Engine Implementation](rust-no-std-ml-engine-implementation.md)
- [Inference Efficiency Claim Verification](inference-efficiency-claim-verification.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
