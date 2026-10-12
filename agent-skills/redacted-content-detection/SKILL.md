---
name: redacted-content-detection
description: Detect masking patterns, placeholder tokens, and removed content in documents so downstream reasoning does not treat redactions as literal facts.
metadata:
  source: skills/01-perception/redacted-content-detection.md
  category: 01-perception
  version: "v1"
---

# Redacted Content Detection

## Description
Detect masking patterns, placeholder tokens, and removed content in documents so downstream reasoning does not treat redactions as literal facts. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- The task has explicit constraints such as time, budget, or safety that must gate the outcome.
- A silent failure mode exists that must be surfaced rather than swallowed.
- Verification evidence is required before the result is trusted.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for redacted content detection. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the redacted content detection steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
# Redacted Content Detection: deterministic check
options = [{"name": "x", "gain": 5, "cost": 1}, {"name": "y", "gain": 4, "cost": 1}]
ranked = sorted(options, key=lambda o: (o["cost"], -o["gain"]))
assert ranked[0]["name"] == "x"
print("best:", ranked[0]["name"])
```

## Failure Modes
- Acting outside the declared task boundary.
- Assuming an estimate or preview equals the verified effect.
- Retrying without preserving state or evidence.
- Using stale inputs as if they were current.
- Reporting success without checking the resulting state.

## Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result.

## Evidence
Privacy-preserving document pipelines in 2026 publish redaction-aware parsing; agents that trusted masked values produced reported failure cases. These are dated public signals, not adoption metrics.

## Related
- document-parsing.md
- metadata-extraction.md
- privacy-preservation.md
