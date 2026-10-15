---
name: generative-engine-optimization-auditing
description: "Audit pages for answer-engine readiness: factual density, citations, freshness, and machine-readable structure."
metadata:
  source: skills/11-web/generative-engine-optimization-auditing.md
  category: 11-web
  version: "v1"
---

# Generative Engine Optimization Auditing

## Description
Audit pages for answer-engine readiness: factual density, citations, freshness, and machine-readable structure. The procedure is constrained by explicit inputs and acceptance criteria rather than best-effort judgment alone.

## When to Use
- A task requires generative engine optimization auditing before downstream steps can proceed safely.
- Ambiguity or missing evidence would change the outcome.
- The result must be recorded with reasons and evidence for later verification.

## Inputs / Outputs
| Area | Contract |
|---|---|
| Inputs | Task context, candidate inputs, and explicit acceptance criteria for generative engine optimization auditing. |
| Outputs | A decision or artifact with recorded reasons, rejected alternatives, and verification evidence. |
| Safety | Failures must fail closed and be reported with evidence rather than retried silently. |

## Procedure
1. Define the goal, the constraints, and the boundary of what this procedure may change.
2. Inventory the available inputs and flag gaps or ambiguities that block progress.
3. Execute the generative engine optimization auditing steps in a bounded, checkpointed way.
4. Compare the actual outcome against the expected outcome and record deviations.
5. On failure, apply the declared fallback path, and never widen permissions to recover.
6. Emit a structured result with evidence and provenance for downstream consumers.

## Runnable Example
```python
def audit_page(facts, citations, min_facts):
    return len(facts) >= min_facts and len(citations) >= min_facts
assert audit_page(["a", "b"], ["u1", "u2"], 2) is True
assert audit_page(["a"], ["u1"], 2) is False
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
Generative-engine optimization audits are requested as answer engines become a 2026 discovery channel. These are dated public signals, not adoption metrics.

## Related
- web-search.md
- html-reading.md
- search-federation-tooling.md
