---
name: ai-film-marketing-copywriting
description: Write marketing copy for an AI-generated film that discloses its AI origin while selling the story on its own merits.
metadata:
  source: skills/13-creative/ai-film-marketing-copywriting.md
  category: 13-creative
  version: "v1"
---

# AI Film Marketing Copywriting

## Description
Write marketing copy for an AI-generated film that discloses its AI origin while selling the story on its own merits. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

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
3. Draft one origin-disclosure line and one story hook, verify every factual claim about the film against the production record, and test that removing the disclosure does not leave any misleading implication.
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
def copy(title, disclosure, hook):
    if "AI" not in disclosure and "artificial intelligence" not in disclosure:
        raise ValueError("missing AI-origin disclosure")
    return title + ". " + disclosure + " " + hook

out = copy("Launch", "Made with AI-generated visuals.", "A family says goodbye in orbit.")
assert "AI" in out and "orbit" in out
```

## Failure Modes
- The copy sells the film while hiding the AI origin and audiences discover it from reviews.
- AI origin is disclosed in fine print only and the headline implies live-action footage.
- Factual claims about awards or box office are invented to match the campaign tone.
- The disclosure is so dominant that the story never gets a hook and interest collapses.
- Campaign variants drift and some channels drop the disclosure entirely.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- AFP reports China's first AI film reached cinemas, creating a real marketed class of AI-generated films (afp.com, dated October 23, 2026) ([public signal](https://www.afp.com/en/chinas-first-ai-film-hits-cinemas-ticket-sales-lag))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Release Trailer Script Writing](../13-creative/release-trailer-script-writing.md)
- [Social Media Post](../13-creative/social-media-post.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
