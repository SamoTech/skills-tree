---
title: "Browser Network Interception"
category: 11-web
level: advanced
stability: experimental
description: "Observe and selectively stub browser network traffic during automation with request matching rules and recorded evidence of what was intercepted."
added: "2026-10"
version: v1
related: [js-execution, http-header-analysis, headless-browser-configuration]
tags: [network, interception, testing]
---

# Browser Network Interception

## Description
Observe and selectively stub browser network traffic during automation with request matching rules and recorded evidence of what was intercepted. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- a browser flow depends on observing or controlling its network requests.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for browser network interception work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the browser network interception steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def match_rules(url, rules):
    hits = [r for r in rules if url.startswith(r['prefix'])]
    return hits[0]['action'] if hits else 'pass'

rules = [{'prefix': 'https://cdn.example.net/', 'action': 'stub'}]
assert match_rules('https://cdn.example.net/app.js', rules) == 'stub'
assert match_rules('https://example.org/', rules) == 'pass'
```

## Failure Modes
- Intercepting live traffic without recording what was stubbed.
- Stub rules that accidentally match production hosts.
- Intercepting but never asserting the page still behaves.
- Leaving interception active outside the test context.
- Missing that a request bypassed interception via another origin.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Network interception and stubbing for deterministic agent tests is a recurring 2026 request; this is a dated signal, not an adoption metric.

## Related
- js-execution.md
- http-header-analysis.md
- headless-browser-configuration.md
