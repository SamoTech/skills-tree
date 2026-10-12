---
title: "CI Failure Triage"
category: 05-code
level: intermediate
stability: experimental
description: "Classify CI failures by category, such as flake, environment, product, or configuration, with the responsible component identified and evidence attached, before retrying or escalating."
added: "2026-10"
version: v1
related: [debugging, cicd-generation, stack-trace-analysis]
tags: [ci, failure, triage, code]
---

# CI Failure Triage

## Description
Classify CI failures by category, such as flake, environment, product, or configuration, with the responsible component identified and evidence attached, before retrying or escalating. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- A task requires ci failure triage before downstream steps can proceed safely.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for ci failure triage. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the ci failure triage steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
# CI Failure Triage: deterministic check
def validate(record, required):
    missing = [k for k in required if k not in record]
    return (True, []) if not missing else (False, missing)

ok, missing = validate({"id": "x", "source": "y"}, ["id", "source"])
assert ok and not missing
print("validated")
```

## Failure Modes
- Acting outside the declared task boundary.
- Assuming an estimate or preview equals the verified effect.
- Retrying without preserving state or evidence.
- Using stale inputs as if they were current.
- Reporting success without checking the resulting state.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
CI failure triage is a top coding-agent use case in 2026; public threads request failure classification before retry. These are dated public signals, not adoption metrics.

## Related
- debugging.md
- cicd-generation.md
- stack-trace-analysis.md
