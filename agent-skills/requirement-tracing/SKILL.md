---
name: requirement-tracing
description: Trace each requirement to the code, tests, and documentation that implement it, and report uncovered or ambiguous requirements before sign-off.
metadata:
  source: skills/05-code/requirement-tracing.md
  category: 05-code
  version: "v1"
---
# Requirement Tracing

## Description
Trace each requirement to the code, tests, and documentation that implement it, and report uncovered or ambiguous requirements before sign-off. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- A task requires requirement tracing before downstream steps can proceed safely.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for requirement tracing. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Normalize the task into explicit inputs, constraints, and acceptance criteria.
2. Gather the required evidence and check completeness before proceeding.
3. Apply the requirement tracing procedure using the declared criteria only.
4. Record the outcome, rejected alternatives, and the reason for each rejection.
5. Verify the result against the acceptance criteria with an independent check.
6. Report the result with evidence, and escalate explicitly when a criterion cannot be met.

## Runnable Example
```python
# Requirement Tracing: deterministic check
attempts = []
def flaky(n):
    attempts.append(n)
    return n >= 3

tries, max_tries, done = 0, 5, False
while tries < max_tries:
    tries += 1
    if flaky(tries):
        done = True
        break
assert done and tries == 3
print("succeeded after", tries, "attempts")
```

## Failure Modes
- Proceeding with requirement tracing without the required evidence or inputs.
- Treating an unverified result as verified.
- Silently swallowing errors instead of failing closed with reasons.
- Optimizing the stated metric while violating the stated constraint.
- Losing the audit trail of decisions and rejected alternatives.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Spec-to-implementation traceability recurs in 2026 coding-agent threads; auditable requirement coverage is a named enterprise request. These are dated public signals, not adoption metrics.

## Related
- code-review.md
- unit-test-generation.md
- documentation-generation.md
