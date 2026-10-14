---
name: agents-md-authoring
description: Author and maintain AGENTS.md files that tell coding agents about build, test, and contribution conventions for a repository.
metadata:
  source: skills/05-code/agents-md-authoring.md
  category: 05-code
  version: "v1"
---
# Agents Md Authoring

## Description
Author and maintain AGENTS.md files that tell coding agents about build, test, and contribution conventions for a repository. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- A task requires agents md authoring before downstream steps can proceed safely.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for agents md authoring. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the agents md authoring steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def agents_md(build_cmd, test_cmd):
    return "# AGENTS.md\n- Build: %s\n- Test: %s" % (build_cmd, test_cmd)
md = agents_md("make", "make test")
assert "make test" in md
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
AGENTS.md is an adopted convention read by major coding agents in 2026; repositories request authoring guidance. These are dated public signals, not adoption metrics.

## Related
- codebase-onboarding.md
- documentation-generation.md
- system-prompt-refactoring.md
