---
title: "Agent Framework Selection Comparison"
category: 09-agentic-patterns
level: advanced
stability: experimental
description: "Compare agent frameworks for a concrete workload by scoring recorded capability criteria instead of benchmarketing or brand loyalty."
added: "2026-11"
version: v1
related: [framework-modularization-refactoring-planning, modular-agent-architecture-migration]
tags: [frameworks, comparison, selection]
---

# Agent Framework Selection Comparison

## Description
Compare agent frameworks for a concrete workload by scoring recorded capability criteria instead of benchmarketing or brand loyalty. The comparison is bounded by the workload's declared criteria and reproducible spike evidence rather than general rankings.

## When to Use
- A team must choose between orchestration frameworks for a real workload.
- Criteria must come from the workload, not vendor marketing.
- The result must be reproducible from recorded spike evidence.

## Inputs
| Area | Contract |
|---|---|
| Inputs | The workload definition, the candidate framework list, and the weighted criteria. |
| Outputs | A scored comparison with per-criterion evidence and a justified selection. |
| Safety | Fail closed by refusing selections whose criteria were never tested. |

## Procedure
1. Define the workload and its hard constraints.
2. Derive weighted criteria from the workload's actual requirements.
3. Run the same representative spike on each candidate framework.
4. Score each criterion from the spike evidence, not documentation claims.
5. Mark untested criteria as unknown instead of guessing.
6. Emit the scored comparison and the selection with its evidence links.

## Outputs
| Area | Contract |
|---|---|
| Primary | A scored framework comparison with per-criterion spike evidence. |
| Verification | The spike artifacts that reproduce every score. |
| Failure | An unknown marker for criteria that were never tested. |

## Runnable Example
```python
def compare(frameworks, criteria, weights, spikes):
    scores = {}
    for f in frameworks:
        total, unknown = 0.0, []
        for c in criteria:
            ev = spikes.get((f, c))
            if ev is None:
                unknown.append(c)
                continue
            total += weights[c] * ev
        scores[f] = {"score": round(total, 2), "unknown": unknown}
    best = max(scores, key=lambda f: scores[f]["score"])
    return {"scores": scores, "selection": best}

crit = ["stateful", "human_approval"]
w = {"stateful": 0.6, "human_approval": 0.4}
spikes = {("fw1", "stateful"): 1.0, ("fw1", "human_approval"): 1.0,
          ("fw2", "stateful"): 0.5, ("fw2", "human_approval"): 0.0}
r = compare(["fw1", "fw2"], crit, w, spikes)
assert r["selection"] == "fw1" and r["scores"]["fw2"]["score"] == 0.3
```

## Failure Modes
- Criteria are copied from a generic ranking instead of the workload.
- Documentation claims are scored as if they were spike evidence.
- Untested criteria are guessed to complete the table.
- Weights are adjusted after scoring to favor a preferred framework.
- Spike artifacts are discarded, making the comparison unreproducible.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- Comparisons of frameworks like LangGraph, LangChain, and CrewAI continue to emerge, aiding selection of the right agent framework for projects (AI Agents Directory Daily Brief, November 7, 2026) ([public signal](https://aiagentsdirectory.com/news/ai-agents-directory-daily-brief-november-7-2026))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Framework Modularization Refactoring Planning](framework-modularization-refactoring-planning.md)
- [Modular Agent Architecture Migration](modular-agent-architecture-migration.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |
