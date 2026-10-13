---
title: "Code Freeze Management"
category: 05-code
level: advanced
stability: experimental
description: "Manage code freeze windows with explicit exception criteria, recorded approvals, and an auditable list of frozen paths."
added: "2026-10"
version: v1
related: [cicd-generation, semantic-version-management, git-operations]
tags: [release, process, governance]
---

# Code Freeze Management

## Description
Manage code freeze windows with explicit exception criteria, recorded approvals, and an auditable list of frozen paths. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- a release freeze is active and change requests must be evaluated against declared criteria.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for code freeze management work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the code freeze management steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def freeze_decision(change, freeze, approvals):
    if change["risk"] == "critical" and not approvals:
        return "needs-approval"
    if change["path"] in freeze["frozen_paths"] and change["risk"] != "critical":
        return "deferred"
    return "allowed"

freeze = {"frozen_paths": ["payments/"]}
assert freeze_decision({"path": "docs/", "risk": "low"}, freeze, []) == "allowed"
assert freeze_decision({"path": "payments/x", "risk": "low"}, freeze, []) == "deferred"
```

## Failure Modes
- Freezing verbally with no written path list.
- Granting exceptions without recording who approved.
- Letting critical fixes in with no second reviewer.
- No unfreeze checklist when the window ends.
- Freezing code but not configuration drift.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Release freezes and exception governance are recurring 2026 delivery topics in public engineering discussion; this is a dated signal, not an adoption metric.

## Related
- cicd-generation.md
- semantic-version-management.md
- git-operations.md
