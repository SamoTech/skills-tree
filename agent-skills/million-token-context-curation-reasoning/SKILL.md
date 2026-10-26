---
name: million-token-context-curation-reasoning
description: Reason about what belongs in a million-token context window using measured relevance and budget floors rather than maximum-fill habits.
metadata:
  source: skills/03-memory/million-token-context-curation-reasoning.md
  category: 03-memory
  version: "v1"
---

# Million Token Context Curation Reasoning

## Description
Reason about what belongs in a million-token context window using measured relevance and budget floors rather than maximum-fill habits. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- An operator needs this capability to proceed safely and verifiably.
- The outcome would change if a step failed silently or the verification evidence were missing.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | the declared input set, policy thresholds, and explicit acceptance criteria. |
| Outputs | A structured record with the decision, rejected alternatives, and the verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Score candidate context blocks by task relevance and staleness, allocate them against an explicit token budget with a reserve, and record what was excluded and why.
4. Compare the actual outcome against the acceptance criteria and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Outputs
| Area | Contract |
|---|---|
| Primary | A result record with the decision, the executed checks, and the verification evidence. |
| Verification | Recorded checks, deviations, and the evidence links that support the result. |
| Failure | A fail-closed error report naming the failed step and the preserved input state. |

## Runnable Example
```python
def curate_context(blocks, budget, reserve):
    usable = budget - reserve
    chosen, spent = [], 0
    for b in sorted(blocks, key=lambda x: -x["relevance"]):
        if spent + b["tokens"] <= usable:
            chosen.append(b["id"]); spent += b["tokens"]
    return {"chosen": chosen, "spent": spent, "reserve_kept": budget - spent >= reserve}

blocks = [{"id":"a","relevance":0.9,"tokens":400},
          {"id":"b","relevance":0.5,"tokens":900},
          {"id":"c","relevance":0.7,"tokens":300}]
out = curate_context(blocks, budget=1000, reserve=200)
assert out["chosen"] == ["a", "c"] and out["reserve_kept"] is True
```

## Failure Modes
- The window is filled to the token maximum and latency cost scales past the value of the last blocks.
- Low-relevance historical blocks crowd out fresh task-critical records.
- Excluded blocks are not recorded so the curation decision cannot be audited or replayed.
- A reserve is declared but not enforced and overflow is truncated at an arbitrary boundary.
- Relevance scores are computed once and reused after the task definition changes.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- Kimi K3.1 Pro shipped with a 1M-token context as part of the strongest open-weight release measured to date (llmreference.com, dated October 23, 2026) ([public signal](https://www.llmreference.com/changelog/2026-10))
- The October dispatch tracks multiple 256K-384K context releases in the same week, making explicit context curation a recurring routing concern (llmreference.com, dated October 2026) ([public signal](https://www.llmreference.com/changelog/2026-10))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Context Window Budget Planning](../03-memory/context-window-budget-planning.md)
- [Long Context Curation](../03-memory/long-context-curation.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
