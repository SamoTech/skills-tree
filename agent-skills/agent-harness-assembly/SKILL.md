---
name: agent-harness-assembly
description: "Assemble the agent harness: model access, tools, memory, permissions, evaluation hooks, and observability in one runtime."
metadata:
  source: skills/09-agentic-patterns/agent-harness-assembly.md
  category: 09-agentic-patterns
  version: "v1"
---

# Agent Harness Assembly

## Description
Assemble the agent harness: model access, tools, memory, permissions, evaluation hooks, and observability in one runtime. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- A task requires agent harness assembly before downstream steps can proceed safely.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for agent harness assembly. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the agent harness assembly steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def assemble(parts, required):
    missing = [r for r in required if r not in parts]
    if missing:
        raise ValueError("missing: %s" % missing)
    return "harness-ready"
assert assemble(["model", "tools", "memory", "evals", "observability"], ["model", "tools", "evals"]) == "harness-ready"
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
Harness engineering is an active 2026 ecosystem topic covering tools, evals, memory, and permissions assembly. These are dated public signals, not adoption metrics.

## Related
- progressive-skill-loading.md
- tool-inventory-cataloging.md
- meta-cognition.md
