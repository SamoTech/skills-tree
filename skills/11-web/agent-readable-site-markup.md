---
title: "Agent-Readable Site Markup"
category: 11-web
level: advanced
stability: experimental
description: "Add and validate machine-readable markup that helps agents use a site correctly, with explicit permissions and change detection."
added: "2026-10"
version: v1
related: [dom-inspection, api-discovery, web-accessibility-auditing]
tags: [markup, agents, permissions]
---

# Agent-Readable Site Markup

## Description
Add and validate machine-readable markup that helps agents use a site correctly, with explicit permissions and change detection. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- a site must publish machine-readable guidance for consuming agents.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for agent-readable site markup work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the agent-readable site markup steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def validate_markup(blocks):
    invalid = [b for b in blocks if 'allow' not in b or 'path' not in b]
    return len(invalid) == 0, invalid

ok, bad = validate_markup([{'path': '/docs', 'allow': 'read'}])
assert ok and bad == []
```

## Failure Modes
- Publishing markup that contradicts the real site policy.
- Forgetting permissions so every path defaults open.
- No change detection when routes move or disappear.
- Markup that references endpoints which do not resolve.
- Validating syntax but never testing with a consuming agent.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Agent-readable site guidance alongside the MCP 2026-07-28 specification update is a recurring 2026 request; this is a dated signal, not an adoption metric.

## Related
- dom-inspection.md
- api-discovery.md
- web-accessibility-auditing.md
