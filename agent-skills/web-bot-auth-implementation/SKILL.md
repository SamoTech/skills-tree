---
name: web-bot-auth-implementation
description: Implement bot authentication for automated web access including protocol selection, credential scoping, and verified identification headers.
metadata:
  source: skills/11-web/web-bot-auth-implementation.md
  category: 11-web
  version: "v1"
---

# Web Bot Auth Implementation

## Description
Implement bot authentication for automated web access including protocol selection, credential scoping, and verified identification headers. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- automated access to a site requires declared and verified bot identity.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for web bot auth implementation work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the web bot auth implementation steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def identify_headers(agent_name, contact):
    if '@' not in contact:
        raise ValueError('contact must include an email address')
    return {'X-Bot-Contact': contact, 'X-Bot-Name': agent_name}

h = identify_headers('skills-tree-bot', 'ops@example.org')
assert h['X-Bot-Name'] == 'skills-tree-bot'
```

## Failure Modes
- Sending automated traffic with a browser-spoofed identity.
- Using credentials with far wider scope than the task needs.
- Ignoring the declared protocol a site publishes for bots.
- Never verifying that identification headers survive redirects.
- Hard-coding contact or identity per run without recording it.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
2026 web-ecosystem discussions push declared bot identification and authenticated agent access over scraping; this is a dated signal, not an adoption metric.

## Related
- http-header-analysis.md
- url-rate-limiting.md
- robots-txt-parsing.md
