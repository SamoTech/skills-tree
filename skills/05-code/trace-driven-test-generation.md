---
title: "Trace Driven Test Generation"
category: 05-code
level: advanced
stability: experimental
description: "Derive regression tests from recorded execution traces so real failure paths are covered instead of invented happy paths."
added: "2026-10"
version: v1
related: [unit-test-generation, property-based-testing, stack-trace-analysis]
tags: [testing, traces, regression]
---

# Trace Driven Test Generation

## Description
Derive regression tests from recorded execution traces so real failure paths are covered instead of invented happy paths. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- a failure was observed in production and the trace of it is available before tests are written.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for trace driven test generation work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the trace driven test generation steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def cases_from_trace(trace):
    cases = []
    for step in trace:
        if step["status"] == "error":
            cases.append({"input": step["input"], "expect": step["expected"]})
    return cases

trace = [
    {"status": "ok", "input": 1, "expected": 2},
    {"status": "error", "input": 3, "expected": 4},
]
cases = cases_from_trace(trace)
assert len(cases) == 1 and cases[0]["input"] == 3
```

## Failure Modes
- Writing tests from imagination while the trace sits unread.
- Copying personal data from traces into test fixtures.
- Asserting only the happy path of the failing flow.
- Not pinning the trace version the test came from.
- Deleting the test after the bug is fixed.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Trace-driven evaluation of coding agents is a documented 2026 observability practice in public coverage; this is a dated signal, not an adoption metric.

## Related
- unit-test-generation.md
- property-based-testing.md
- stack-trace-analysis.md
