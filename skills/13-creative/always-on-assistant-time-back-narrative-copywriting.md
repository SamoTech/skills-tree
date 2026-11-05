---
title: "Always On Assistant Time Back Narrative Copywriting"
category: 13-creative
level: advanced
stability: experimental
description: "Write positioning copy for always-on assistants around verified time-back outcomes instead of vague capability claims."
added: "2026-11"
version: v1
related: [pitch-deck-narrative, personal-agent-onboarding-copy]
tags: [copywriting, agents, narrative, positioning]
---
# Always On Assistant Time Back Narrative Copywriting

## Description
Write positioning copy for always-on assistants around verified time-back outcomes instead of vague capability claims. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- An always-on assistant needs launch positioning.
- The copy must claim only verifiable outcomes.
- Time-saved claims need a stated measurement basis.

## Inputs
| Area | Contract |
|---|---|
| Inputs | The product responsibilities, the measured outcome data, and the audience. |
| Outputs | Launch copy naming concrete outcomes with their measurement bases. |
| Safety | Fail closed by removing any outcome claim that lacks a stated measurement basis. |

## Procedure
1. List the assistant responsibilities and their measured outcomes.
2. Select the audience and the decisions the copy must support.
3. Draft the narrative around concrete time-back outcomes.
4. Attach the measurement basis to every outcome claim.
5. Strip capability claims that no outcome data supports.
6. Emit the copy with a claim-to-evidence mapping for review.

## Outputs
| Area | Contract |
|---|---|
| Primary | Launch copy naming concrete outcomes with their measurement bases. |
| Verification | The claim-to-evidence mapping that reproduces every retained claim. |
| Failure | A fail-closed revision report naming the unsupported claims. |

## Runnable Example
```python
def review(claims, evidence):
    keep, drop = [], []
    for c in claims:
        (keep if c["outcome"] in evidence else drop).append(c)
    return {"keep": keep, "drop": drop}
ev = {"hours-saved-weekly": "panel-study"}
cs = [{"id": "c1", "outcome": "hours-saved-weekly"},
      {"id": "c2", "outcome": "reads-your-mind"}]
r = review(cs, ev)
assert [c["id"] for c in r["keep"]] == ["c1"] and [c["id"] for c in r["drop"]] == ["c2"]
```

## Failure Modes
- The copy claims time savings with no stated measurement basis.
- Capability poetry replaces concrete responsibilities.
- Outcome numbers are rounded upward for punch.
- The claim-to-evidence mapping is omitted from review.
- Unsupported claims survive because they sound aspirational.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- OpenAI DevDay 2026 positioned Dots, always-on agents, around giving people more time and attention for what matters (OpenAI DevDay 2026 Recap, dated November 5, 2026) ([public signal](https://openai.com/index/devday-2026-recap/))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Pitch Deck Narrative](pitch-deck-narrative.md)
- [Personal Agent Onboarding Copy](personal-agent-onboarding-copy.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |
