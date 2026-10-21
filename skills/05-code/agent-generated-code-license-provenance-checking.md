---
title: "Agent Generated Code License Provenance Checking"
category: 05-code
level: advanced
stability: experimental
description: "Check license provenance for agent-generated code so downstream obligations are recorded before merge."
added: "2026-10"
version: v1
related: [agent-generated-code-auditing, build-reproducibility-verification]
tags: [licensing, provenance, agents, verification]
---
# Agent Generated Code License Provenance Checking

## Description
Check license provenance for agent-generated code so downstream obligations are recorded before merge. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- An agent produced code that resembles a known open-source implementation and license obligations must be checked before merge.
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
3. Compare the generated code against declared licensed sources, record matched origins and licenses, and block the merge when an obligation is undeclared.
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
def check_license_provenance(matches, allowed):
    violations = [m for m in matches if m["license"] not in allowed]
    return {"merge": not violations, "violations": violations}
matches = [{"file": "util.py", "license": "MIT"}, {"file": "net.go", "license": "GPL-3.0"}]
dec = check_license_provenance(matches, {"MIT", "Apache-2.0"})
assert dec["merge"] is False and len(dec["violations"]) == 1
```

## Failure Modes
- Code is merged without recording which licensed sources the agent drew from.
- License obligations are read from the model's claim rather than the matched source.
- Copyleft detections are downgraded to warnings and obligations are missed.
- The provenance record is written after merge and cannot gate the decision.
- Snippet matching is case-sensitive on license names and valid obligations slip through.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- The October 2026 LangChain newsletter rounds up the agent tooling releases shipped at Interrupt NYC and London (langchain.com, dated October 15, 2026) ([public signal](https://www.langchain.com/blog/october-2026-langchain-newsletter))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Agent Generated Code Auditing](../05-code/agent-generated-code-auditing.md)
- [Build Reproducibility Verification](../05-code/build-reproducibility-verification.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
