---
title: "Website Localization Verification"
category: 11-web
level: advanced
stability: experimental
description: "Verify localized versions of a site with locale negotiation, layout integrity, and untranslated-string detection across target locales."
added: "2026-10"
version: v1
related: [web-accessibility-auditing, page-diff-monitoring, dom-inspection]
tags: [localization, i18n, qa]
---

# Website Localization Verification

## Description
Verify localized versions of a site with locale negotiation, layout integrity, and untranslated-string detection across target locales. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- a multilingual site release must be verified per locale before launch.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for website localization verification work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the website localization verification steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def check_locales(pages, locales):
    missing = {loc: [p for p in pages if loc not in p['locales']] for loc in locales}
    return all(not v for v in missing.values()), missing

pages = [{'name': 'home', 'locales': ['en', 'fr']}]
ok, missing = check_locales(pages, ['en', 'fr', 'de'])
assert not ok and missing['de'] == ['home']
```

## Failure Modes
- Verifying only the default locale.
- Missing untranslated strings that leak the source language.
- Ignoring layout breakage from longer localized strings.
- Testing locale paths that real negotiation never serves.
- Not recording which locale-version pair was verified.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Localization verification appears in 2026 site-quality request lists; this is a dated signal, not an adoption metric.

## Related
- web-accessibility-auditing.md
- page-diff-monitoring.md
- dom-inspection.md
