---
title: "Dialogue State Tracking"
category: 03-memory
level: intermediate
stability: experimental
description: "Maintain a compact structured state of slots, intents, and pending confirmations across dialogue turns with update rules and conflict handling rather than re-reading full history."
added: "2026-10"
version: v1
related: [working-memory, short-term-memory, memory-indexing]
tags: [dialogue, state, tracking, memory]
---

# Dialogue State Tracking

## Description
Maintain a compact structured state of slots, intents, and pending confirmations across dialogue turns with update rules and conflict handling rather than re-reading full history. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- A task requires dialogue state tracking before downstream steps can proceed safely.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for dialogue state tracking. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Normalize the task into explicit inputs, constraints, and acceptance criteria.
2. Gather the required evidence and check completeness before proceeding.
3. Apply the dialogue state tracking procedure using the declared criteria only.
4. Record the outcome, rejected alternatives, and the reason for each rejection.
5. Verify the result against the acceptance criteria with an independent check.
6. Report the result with evidence, and escalate explicitly when a criterion cannot be met.

## Runnable Example
```python
# Dialogue State Tracking: deterministic check
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
- Proceeding with dialogue state tracking without the required evidence or inputs.
- Treating an unverified result as verified.
- Silently swallowing errors instead of failing closed with reasons.
- Optimizing the stated metric while violating the stated constraint.
- Losing the audit trail of decisions and rejected alternatives.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Voice and chat agent architectures in 2026 publish state-tracking components; multi-turn management is a recurring production request. These are dated public signals, not adoption metrics.

## Related
- working-memory.md
- short-term-memory.md
- memory-indexing.md
