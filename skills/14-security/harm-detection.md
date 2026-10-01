---
title: "Harm Detection"
category: 14-security
level: advanced
stability: stable
description: "Triage potentially harmful agent inputs and outputs with explicit categories, thresholds, and escalation paths before high-impact actions."
added: "2025-03"
updated: "2026-10"
version: v2
related: [input-sanitization, human-in-loop, privacy-preservation]
---

# Harm Detection

## Description

Harm detection is a safety gate that classifies content or planned actions against an explicitly defined risk policy before an agent acts or responds. It should identify relevant categories, preserve uncertainty, and escalate ambiguous or high-impact cases instead of silently converting a classifier result into authorization.

The detector can combine deterministic rules, specialist classifiers, and human review. It is a risk-control layer, not a universal guarantee that content is safe.

## Inputs / Outputs

| Input | Type | Required | Description |
|---|---|---:|---|
| `text` | string | yes | Content to classify |
| `action` | string | no | Intended agent action if action-aware screening is used |
| `policy` | dict | yes | Categories, thresholds, and escalation behavior |
| `context` | dict | no | Minimal context required for classification |

| Output | Type | Description |
|---|---|---|
| `decision` | string | `allow`, `escalate`, or `block` |
| `categories` | list[str] | Policy categories triggered |
| `confidence` | float | Classifier confidence when available |
| `reason` | string | Safe explanation of the decision |

## Runnable Example

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class SafetyResult:
    decision: str
    categories: list[str]
    confidence: float

def screen(text: str) -> SafetyResult:
    lower = text.casefold()
    categories = []
    if "credential" in lower or "password" in lower:
        categories.append("credential_handling")
    if "self-harm" in lower:
        categories.append("self_harm")
    if categories:
        return SafetyResult("escalate", categories, 0.70)
    return SafetyResult("allow", [], 0.90)

print(screen("Please summarize this public article."))
```

This deterministic example is intentionally conservative and incomplete. Production classifiers require a documented taxonomy, evaluation set, threshold policy, false-positive/false-negative analysis, and an escalation path.

## Failure Modes

| Failure | Cause | Mitigation |
|---|---|---|
| False negative | Classifier misses harmful content | Use layered controls and action-specific authorization |
| False positive | Benign content matches a category | Provide review/escalation rather than silent rejection when appropriate |
| Context loss | Classification sees too little context | Pass only the minimum context required for the policy decision |
| Classifier prompt injection | User content manipulates a classifier | Treat classifier input as untrusted and constrain its output schema |
| Policy drift | Categories or thresholds become outdated | Version the policy and evaluate changes before rollout |
| Over-trust | A classifier result is treated as authorization | Keep safety screening separate from identity/permission checks |

## Design Rules

- Define categories and actions before implementing the classifier.
- Keep `block` and `escalate` semantics explicit.
- Do not expose hidden classifier prompts or sensitive evidence in user-facing messages.
- Log policy decisions without storing unnecessary harmful content.
- Re-test thresholds when models or policies change.
- Use human review for ambiguous high-impact cases.

## References

- NIST AI Risk Management Framework: https://www.nist.gov/itl/ai-risk-management-framework
- NIST AI RMF FAQs: https://www.nist.gov/itl/ai-risk-management-framework/ai-risk-management-framework-faqs

Evidence status: the cited NIST material supports AI risk-management and trustworthiness guidance; this skill does not claim that any classifier is universally accurate.

## Related Skills

- [Input Sanitization](input-sanitization.md)
- [Human In Loop](human-in-loop.md)
- [Permission Checking](permission-checking.md)
