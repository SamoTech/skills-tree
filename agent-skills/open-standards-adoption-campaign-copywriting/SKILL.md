---
name: open-standards-adoption-campaign-copywriting
description: Write adoption campaign copy for open agent standards that names the standard, its governance home, and honest maturity state without vendor capture framing.
metadata:
  source: skills/13-creative/open-standards-adoption-campaign-copywriting.md
  category: 13-creative
  version: "v1"
---

# Open Standards Adoption Campaign Copywriting

## Description
Write adoption campaign copy for open agent standards that names the standard, its governance home, and honest maturity state without vendor capture framing. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A communications agent must write a campaign for adopting open agent standards with honest maturity and governance framing.
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
3. Draft the campaign naming each standard and its governance home, state the maturity level honestly, and record the standard body as the authority link before publishing.
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
def campaign_copy(items):
    out = []
    for it in items:
        if not it.get("governance") or not it.get("maturity"):
            raise ValueError("standard entry needs governance home and maturity: " + it["name"])
        out.append(f"{it[chr(110)+chr(97)+chr(109)+chr(101)]} - governed by {it[chr(103)+chr(111)+chr(118)+chr(101)+chr(114)+chr(110)+chr(97)+chr(110)+chr(99)+chr(101)]}, maturity: {it[chr(109)+chr(97)+chr(116)+chr(117)+chr(114)+chr(105)+chr(116)+chr(121)]}")
    return "\n".join(out)
copy = campaign_copy([{"name": "Agent Skills", "governance": "AAIF", "maturity": "newly announced"}, {"name": "OpenSandbox", "governance": "AAIF", "maturity": "newly announced"}])
assert "AAIF" in copy
try:
    campaign_copy([{"name": "x", "governance": "AAIF"}])
    assert False
except ValueError:
    pass
```

## Failure Modes
- The campaign presents a newly announced standard as battle-tested and adopters hit early churn.
- Governance homes are omitted and readers assume the standard is vendor-controlled.
- Maturity states are copied from vendor marketing instead of the standards body announcement.
- Competing proprietary formats are disparaged with unsourced claims and the campaign becomes FUD copy.
- The campaign omits how to participate or give feedback and adoption is one-way marketing.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- The Agentic AI Foundation announcement of four new open projects, including Agent Skills and OpenSandbox, provides the open-standards campaign case this skill writes for. ([public signal](https://www.prnewswire.com/news-releases/agentic-ai-foundation-announces-four-new-projects-agent-skills-open-responses-openenv-and-opensandbox-302916689.html))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Ai Content Disclosure Writing](../13-creative/ai-content-disclosure-writing.md)
- [Public Roadmap Communication Writing](../06-communication/public-roadmap-communication-writing.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
