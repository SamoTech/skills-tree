---
title: "Stuck Loop Detection"
category: 09-agentic-patterns
level: advanced
stability: experimental
description: "Detect when an agent repeats the same failing action or state without progress and force a strategy change instead of another retry."
added: "2026-10"
version: v1
related: [agent-halt-conditions, agent-failure-taxonomy, reflection]
tags: [loops, retries, observability]
---

# Stuck Loop Detection

## Description
Detect when an agent repeats the same failing action or state without progress and force a strategy change instead of another retry. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- an autonomous run shows repeated failures and must decide between retry and escalate.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for stuck loop detection work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the stuck loop detection steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def detect_stuck(signatures, window=3):
    if len(signatures) < window:
        return False
    return len(set(signatures[-window:])) == 1

print(not detect_stuck(['a', 'b', 'a']))
print(detect_stuck(['a', 'a', 'a']))
```

## Failure Modes
- Retrying an identical failing action with identical inputs.
- Counting retries without comparing state signatures.
- Escalating without recording what was already tried.
- Flagging productive repetition as a stuck loop.
- Resetting the loop counter on trivial input noise.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Stuck retry loops in autonomous runs are a recurring 2026 agent-observability complaint; this is a dated signal, not an adoption metric.

## Related
- agent-halt-conditions.md
- agent-failure-taxonomy.md
- reflection.md
