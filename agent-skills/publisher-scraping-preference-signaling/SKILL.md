---
name: publisher-scraping-preference-signaling
description: Publish machine-readable scraping and training preferences, such as a shared robots.txt token, and verify that crawlers honor them.
metadata:
  source: skills/11-web/publisher-scraping-preference-signaling.md
  category: 11-web
  version: "v1"
---

# Publisher Scraping Preference Signaling

## Description
Publish machine-readable scraping and training preferences, such as a shared robots.txt token, and verify that crawlers honor them. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A publisher wants a single, verifiable way to opt out of AI training collection across multiple AI companies.
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
3. Declare the preference in the published machine-readable policy, verify each major crawler’s observed behavior against the declaration, and record violations with timestamps and evidence.
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
def honored(declared, observed):
    return observed == declared
assert honored(True, True) is True
assert honored(True, False) is False
```

## Failure Modes
- The token is typoed and silently declares the opposite intent.
- The preference is declared once and crawler behavior is never verified.
- Violations are observed but not recorded with evidence.
- Different pages on the site emit conflicting signals.
- Per-crawler exceptions are granted without documentation.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- the announcement of October 30, 2026 by Google, Microsoft, OpenAI, and Anthropic to honor a shared robots.txt token letting publishers opt out of AI training data collection with a single entry (SaaSSentinel news coverage, dated October 30, 2026) ([public signal](https://saassentinel.com/news/google-microsoft-openai-and-anthropic-back-single-robots-txt-token-for-ai-training-opt-out))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Agent Blocking Site Response](agent-blocking-site-response.md)
- [Government Portal Agent Access Hardening](government-portal-agent-access-hardening.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
