---
title: "Background Job Cancel And Cleanup"
category: 04-action-execution
level: advanced
stability: experimental
description: "Cancel in-flight background jobs and clean up their partial artifacts with compensating actions that leave the system consistent."
added: "2026-10"
version: v1
related: [compensating-actions, background-job-submission]
tags: [jobs, cancellation, cleanup]
---
# Background Job Cancel And Cleanup

## Description
Cancel in-flight background jobs and clean up their partial artifacts with compensating actions that leave the system consistent. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- An agent must stop a background job and remove its partial effects without leaving stale state.
- The outcome would change if inputs were stale, ambiguous, or incomplete.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | background job cancel and cleanup task context, candidate data, and explicit acceptance criteria. |
| Outputs | A structured record with the decision, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the background job cancel and cleanup steps in a bounded, checkpointed way.
4. Compare the actual outcome against the acceptance criteria and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Outputs
| Area | Contract |
|---|---|
| Primary | A cancellation record with job identity, partial-artifact cleanup list, and final consistency check. |
| Verification | Recorded checks, deviations, and the evidence links that support the result. |
| Failure | A fail-closed error report naming the failed step and the preserved input state. |

## Runnable Example
```python
def cleanup_plan(job):
    steps = ["cancel"]
    steps += [f"rm {a}" for a in job.get("artifacts", [])]
    steps.append("verify")
    return steps
assert cleanup_plan({"artifacts": ["t.tmp"]}) == ["cancel", "rm t.tmp", "verify"]
```

## Failure Modes
- Acting outside the declared task boundary.
- Marking a job cancelled without confirming the runner actually stopped.
- Deleting artifacts the job had already published as its output.
- Skipping the final consistency check after cleanup.
- Reporting success without checking the resulting state.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- State-of-agent-security reports list incomplete cleanup after failed agent runs among operational risks. ([public signal](https://www.gravitee.io/state-of-ai-agent-security))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Compensating Actions](../04-action-execution/compensating-actions.md)
- [Background Job Submission](../04-action-execution/background-job-submission.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
