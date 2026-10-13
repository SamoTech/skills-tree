---
title: "Spreadsheet Formula Writing"
category: 04-action-execution
level: advanced
stability: experimental
description: "Write and validate spreadsheet formulas with explicit cell references and error handling, verify computed results against expected values, and avoid volatile recomputation traps."
added: "2026-10"
version: v1
related: [file-write, action-result-verification, api-call]
tags: [spreadsheets, formulas, automation]
---

# Spreadsheet Formula Writing

## Description
Write and validate spreadsheet formulas with explicit cell references and error handling, verify computed results against expected values, and avoid volatile recomputation traps. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- cells must be populated with formulas whose results can be checked before downstream steps can proceed safely.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for spreadsheet formula writing work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the spreadsheet formula writing steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def eval_sumif(rows, col, predicate):
    return sum(r[col] for r in rows if predicate(r))

rows = [{"region": "eu", "amt": 10}, {"region": "us", "amt": 20}]
assert eval_sumif(rows, "amt", lambda r: r["region"] == "eu") == 10

def check_formula(expected, got):
    return abs(expected - got) < 1e-9

assert check_formula(10, eval_sumif(rows, "amt", lambda r: r["region"] == "eu"))
```

## Failure Modes
- Writing formulas without verifying the computed result.
- Hard-coding values that should be references.
- Leaving division with no zero guard.
- Using locale-dependent separators.
- Chaining volatile functions that recalculate constantly.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Spreadsheet automation remains a recurring 2026 computer-use request signal in public coverage; this is a dated signal, not an adoption metric.

## Related
- file-write.md
- action-result-verification.md
- api-call.md
