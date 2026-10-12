---
title: "Semantic Version Management"
category: 05-code
level: basic
stability: experimental
description: "Decide version bumps from the actual change surface using semver rules and changelog evidence, and block releases whose declared version contradicts their changes."
added: "2026-10"
version: v1
related: [git-operations, cicd-generation, code-review]
tags: [semantic, version, management, code]
---

# Semantic Version Management

## Description
Decide version bumps from the actual change surface using semver rules and changelog evidence, and block releases whose declared version contradicts their changes. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- The task has explicit constraints such as time, budget, or safety that must gate the outcome.
- A silent failure mode exists that must be surfaced rather than swallowed.
- Verification evidence is required before the result is trusted.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for semantic version management. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Normalize the task into explicit inputs, constraints, and acceptance criteria.
2. Gather the required evidence and check completeness before proceeding.
3. Apply the semantic version management procedure using the declared criteria only.
4. Record the outcome, rejected alternatives, and the reason for each rejection.
5. Verify the result against the acceptance criteria with an independent check.
6. Report the result with evidence, and escalate explicitly when a criterion cannot be met.

## Runnable Example
```python
# Semantic Version Management: deterministic check
def check_budget(estimate, limit):
    if estimate > limit:
        raise ValueError("estimate %s exceeds limit %s" % (estimate, limit))
    return "approved"

assert check_budget(3, 5) == "approved"
try:
    check_budget(7, 5)
    raise AssertionError("should have raised")
except ValueError:
    print("guard held")
```

## Failure Modes
- Proceeding with semantic version management without the required evidence or inputs.
- Treating an unverified result as verified.
- Silently swallowing errors instead of failing closed with reasons.
- Optimizing the stated metric while violating the stated constraint.
- Losing the audit trail of decisions and rejected alternatives.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Release automation correctness is a 2026 concern; this repository own orphaned-release incident demonstrates version and tag consistency demand. These are dated public signals, not adoption metrics.

## Related
- git-operations.md
- cicd-generation.md
- code-review.md
