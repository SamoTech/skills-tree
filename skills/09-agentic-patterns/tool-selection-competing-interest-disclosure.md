---
title: "Tool Selection Competing Interest Disclosure"
category: 09-agentic-patterns
level: advanced
stability: experimental
description: "Disclose competing interests, such as toolmaker overlap with a recommended tool, whenever an agent or author recommends one tool over a comparable alternative."
added: "2026-11"
version: v1
related: [full-run-lifecycle-hook-instrumentation, piped-permission-prompt-delegation]
tags: [disclosure, tool-selection, bias, agentic-patterns]
---
# Tool Selection Competing Interest Disclosure

## Description
Disclose competing interests, such as toolmaker overlap with a recommended tool, whenever an agent or author recommends one tool over a comparable alternative. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- An agent or content author recommends a tool while operating a competing product and the reader cannot weigh the recommendation without the overlap disclosed.
- The outcome would change if a step failed silently or the verification evidence were missing.
- The result must be recorded with reasons and verification evidence for later audit.

## Inputs
| Area | Contract |
|---|---|
| Inputs | the recommendation, the author's affiliation registry, and the disclosure standard. |
| Outputs | A structured record with the decision, rejected alternatives, and the verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Look up the recommending party in the affiliation registry before publishing a comparison.
2. Identify overlaps between the recommender's products and any tool in the comparison set.
3. State each overlap explicitly in the recommendation alongside the ranking basis.
4. Separate measured claims from preference and mark which claims carry evidence links.
5. On a discovered but undisclosed overlap, block publication and record the finding.
6. Emit a structured result with the disclosure text, overlaps, and evidence links.

## Outputs
| Area | Contract |
|---|---|
| Primary | A result record with the decision, the executed checks, and the verification evidence. |
| Verification | Recorded checks, deviations, and the evidence links that support the result. |
| Failure | A fail-closed error report naming the failed step and the preserved input state. |

## Runnable Example
```python
def disclosure_text(author_products, compared_tools):
    overlap = sorted(set(author_products) & set(compared_tools))
    if overlap:
        return {"blocked": False, "text": "we operate a competing product: " + ", ".join(overlap)}
    return {"blocked": False, "text": "no competing interest"}
mine = ["munder-difflin"]
tools = ["orkas", "munder-difflin", "prospero"]
d = disclosure_text(mine, tools)
assert "orkas" not in d["text"] and "munder-difflin" in d["text"]
```

## Failure Modes
- A ranking omits that the author sells a competing product in the same list.
- Measured claims and personal preference are blended so neither can be checked.
- The overlap is disclosed in a linked page the reader is unlikely to open.
- Undisclosed overlaps are discovered after publication and never corrected.
- The disclosure names the overlap but not the ranking basis, hiding the conflict's effect.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- the Munder Difflin agent-tools daily noting that the Orkas desktop agent team competes with Munder Difflin so the mention should be weighed accordingly (Munder Difflin agent-tools daily, dated November 1, 2026) ([public signal](https://munderdiffl.in/blog/agent-tools-today-2026-11-01/))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Full Run Lifecycle Hook Instrumentation](full-run-lifecycle-hook-instrumentation.md)
- [Piped Permission Prompt Delegation](piped-permission-prompt-delegation.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |
