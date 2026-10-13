---
name: agent-card-parsing
description: Parse A2A Agent Card JSON documents, validate required fields and capability declarations, and surface malformed or inconsistent cards before they are trusted for routing.
metadata:
  source: skills/01-perception/agent-card-parsing.md
  category: 01-perception
  version: "v1"
---

# Agent Card Parsing

## Description
Parse A2A Agent Card JSON documents, validate required fields and capability declarations, and surface malformed or inconsistent cards before they are trusted for routing. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- peer-agent discovery or routing depends on an Agent Card being well formed before downstream steps can proceed safely.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for agent card parsing work. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the agent card parsing steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def validate_card(card):
    required = ("name", "url", "skills")
    missing = [k for k in required if k not in card]
    if missing:
        raise ValueError("missing fields %s" % missing)
    if not card["skills"]:
        raise ValueError("card declares no skills")
    return "valid"

assert validate_card({"name": "a", "url": "https://x", "skills": ["search"]}) == "valid"
try:
    validate_card({"name": "a", "url": "https://x", "skills": []})
    raise AssertionError("should have raised")
except ValueError:
    print("card validation held")
```

## Failure Modes
- Trusting an unverified or unsigned card.
- Ignoring missing capability fields.
- Treating a stale cached card as current.
- Routing on declared skills that were never tested.
- Accepting duplicate or conflicting cards.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
A2A 1.0 (12 March 2026) made signed Agent Cards the discovery artifact for agent-to-agent interop; this is a dated public protocol signal, not an adoption metric.

## Related
- json-schema-validation.md
- url-dom-inspection.md
- metadata-extraction.md
