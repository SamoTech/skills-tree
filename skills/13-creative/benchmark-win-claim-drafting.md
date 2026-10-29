---
title: "Benchmark Win Claim Drafting"
category: 13-creative
level: advanced
stability: experimental
description: "Draft benchmark-win claims so that every published sentence survives an audit against the raw result record."
added: "2026-10"
version: v1
related: [agent-tool-launch-announcement-copywriting, benchmark-result-ledger-memory]
tags: [claims, benchmarks, drafting, audit]
---
# Benchmark Win Claim Drafting

## Description
Draft benchmark-win claims so that every published sentence survives an audit against the raw result record. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A team wants to state that its model or agent won a benchmark and needs copy that is both compelling and exact.
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
3. Draft the claim from the ledger entry, quote the benchmark version and score exactly, and run an audit pass where every sentence is checked against the raw record before release.
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
def audit(claim, ledger):
    problems = []
    if claim["score"] != ledger["score"]:
        problems.append("score mismatch")
    if ledger["version"] not in claim["text"]:
        problems.append("version missing")
    return problems
led = {"score": 88.2, "version": "SEC-bench Pro"}
assert audit({"score": 88.2, "text": "first on SEC-bench Pro"}, led) == []
assert audit({"score": 90.0, "text": "first on SEC-bench Pro"}, led) != []
```

## Failure Modes
- The claim uses a rounded score that flatters the result.
- A relative win is drafted without naming the comparison set.
- The audit pass is skipped under deadline pressure.
- The claim borrows a benchmark name without its version qualifier.
- Copy implies causation from a single benchmark correlation.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- the Gemini 4 Carbon launch reported first place among frontier systems on SEC-bench Pro at 88.2 percent (blog.luandnh.com, dated October 29, 2026) ([public signal](https://blog.luandnh.com/en/ai-daily/2026-10-29/))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Agent Tool Launch Announcement Copywriting](agent-tool-launch-announcement-copywriting.md)
- [Benchmark Result Ledger Memory](../03-memory/benchmark-result-ledger-memory.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
