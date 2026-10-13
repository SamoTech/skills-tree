---
title: "Kubernetes API Interaction"
category: 07-tool-use
level: advanced
stability: experimental
description: "Interact with the Kubernetes API through declared resource contracts, field validation, and dry-run server-side checks before applying changes."
added: "2026-10"
version: v1
related: [custom-api-wrapper, api-version-pinning, tool-output-validation]
tags: [kubernetes, api, platform]
---

# Kubernetes API Interaction

## Description
Interact with the Kubernetes API through declared resource contracts, field validation, and dry-run server-side checks before applying changes. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- an agent must read or modify cluster resources through the API safely.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for kubernetes api interaction work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the kubernetes api interaction steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def dry_run(diff, dangerous):
    blocked = [k for k in diff if k in dangerous]
    return "reject" if blocked else "apply"

dangerous = {"delete", "force"}
assert dry_run({"scale"}, dangerous) == "apply"
assert dry_run({"delete"}, dangerous) == "reject"
```

## Failure Modes
- Applying without a server-side dry run.
- Editing live specs without recording the previous state.
- Trusting local state over the API server version.
- Deleting by name without a namespace check.
- No least-scope credential review for the agent.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Agent-driven cluster operations are a growing 2026 platform-automation theme in public coverage; this is a dated signal, not an adoption metric.

## Related
- custom-api-wrapper.md
- api-version-pinning.md
- tool-output-validation.md
