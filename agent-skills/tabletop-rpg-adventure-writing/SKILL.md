---
name: tabletop-rpg-adventure-writing
description: Write structured tabletop RPG adventures with scene beats, stat blocks, secrets, and branching encounter outcomes.
metadata:
  source: skills/13-creative/tabletop-rpg-adventure-writing.md
  category: 13-creative
  version: "v1"
---
# Tabletop Rpg Adventure Writing

## Description
Write structured tabletop RPG adventures with scene beats, stat blocks, secrets, and branching encounter outcomes. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- A task requires tabletop rpg adventure writing before downstream steps can proceed safely.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for tabletop rpg adventure writing. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the tabletop rpg adventure writing steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def scene(title, choices):
    return {"title": title, "choices": choices}
s = scene("Tavern", ["fight", "talk"])
assert len(s["choices"]) == 2
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
Tabletop RPG adventure generation is a recurring creative-agent request with structure requirements. These are dated public signals, not adoption metrics.

## Related
- interactive-fiction-writing.md
- game-mechanic-design.md
- dialogue-writing.md
