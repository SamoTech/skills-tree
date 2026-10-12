---
title: "Tool Source Vetting"
category: 07-tool-use
level: advanced
stability: experimental
description: "Vet a third-party tool or package source before installation using published provenance, maintainer history, and code inspection, and record the verdict."
added: "2026-10"
version: v1
related: [agent-skill-security-audit, dependency-integrity-verification, secret-scanning]
tags: [tool, source, vetting, tool]
---

# Tool Source Vetting

## Description
Vet a third-party tool or package source before installation using published provenance, maintainer history, and code inspection, and record the verdict. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- Multiple inputs or candidates compete and must be resolved by explicit criteria.
- A wrong intermediate result would propagate into consequential actions.
- The task repeats and benefits from a deterministic procedure.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for tool source vetting. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the tool source vetting steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
# Tool Source Vetting: deterministic check
seen = {}
conflicts = []
for item in [{"k": "a", "v": 1}, {"k": "a", "v": 2}, {"k": "b", "v": 3}]:
    if item["k"] in seen and seen[item["k"]] != item["v"]:
        conflicts.append(item["k"])
    seen[item["k"]] = item["v"]
assert conflicts == ["a"]
print("conflicts:", conflicts)
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
Agent supply-chain security is a 2026 concern; MCP tool poisoning and rug-pull attacks are documented public threats. These are dated public signals, not adoption metrics.

## Related
- agent-skill-security-audit.md
- dependency-integrity-verification.md
- secret-scanning.md
