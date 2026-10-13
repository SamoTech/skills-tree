---
title: "Cookie Consent Automation"
category: 11-web
level: advanced
stability: experimental
description: "Automate cookie consent dialogs with recorded per-site consent intent and verification that the chosen state actually applied."
added: "2026-10"
version: v1
related: [popup-dialog-handling, cookie-management, iframe-handling]
tags: [consent, cookies, gdpr]
---

# Cookie Consent Automation

## Description
Automate cookie consent dialogs with recorded per-site consent intent and verification that the chosen state actually applied. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- automation must pass consent dialogs with a recorded intent per site.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for cookie consent automation work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the cookie consent automation steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def consent_intent(site, preference):
    allowed = {'accept', 'reject', 'essential-only'}
    if preference not in allowed:
        raise ValueError('unknown consent preference')
    return {'site': site, 'preference': preference}

c = consent_intent('example.org', 'essential-only')
assert c['preference'] == 'essential-only'
```

## Failure Modes
- Clicking away the dialog without recording which choice was made.
- Assuming the clicked choice took effect without verification.
- Missing consent iframes and shadow-root dialogs.
- Applying one global preference where the task needs per-site intent.
- Ignoring the consent record when auditing what was accepted.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Consent-dialog automation with recorded intent recurs in 2026 web-automation requests; this is a dated signal, not an adoption metric.

## Related
- popup-dialog-handling.md
- cookie-management.md
- iframe-handling.md
