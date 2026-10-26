---
title: "Batch Skill Import Execution"
category: 04-action-execution
level: advanced
stability: experimental
description: "Import skill packages into a runtime in batches with per-item verification and a rollback ledger, never trusting metadata blindly."
added: "2026-10"
version: v1
related: [agent-skills-open-standard-package-usage, agent-import-trust-memory]
tags: [skills, import, batch, verification]
---
# Batch Skill Import Execution

## Description
Import skill packages into a runtime in batches with per-item verification and a rollback ledger, never trusting metadata blindly. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- An agent must import a batch of skill packages into a runtime and verify each import instead of trusting the batch as a whole.
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
3. Import each package, validate its manifest against the expected source path and version, and record one ledger row per import with a pass or rollback verdict.
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
def import_batch(packages, expected):
    ledger = []
    for p in packages:
        ok = p["source"] in expected and p["version"] == "v1"
        ledger.append({"name": p["name"], "verdict": "pass" if ok else "rollback"})
    return ledger
l = import_batch([{"name": "a", "source": "skills/02-reasoning/a.md", "version": "v1"}], {"skills/02-reasoning/a.md"})
assert l == [{"name": "a", "verdict": "pass"}]
```

## Failure Modes
- The batch is imported as one unit and one bad package rolls back or poisons the whole set.
- Manifest source paths are not validated and a package is attributed to the wrong skill file.
- Rollback rows are not recorded and failed imports leave orphaned state.
- Package metadata is treated as trusted and an unvetted description becomes runtime guidance.
- Import order is not recorded and a later audit cannot reproduce which package landed first.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- The 2026 agent development tooling overview documents the batch skill-import workflows this procedure executes safely. ([public signal](https://www.agensi.io/learn/ai-agent-development-tools-2026))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Agent Skills Open Standard Package Usage](../07-tool-use/agent-skills-open-standard-package-usage.md)
- [Agent Import Trust Memory](../03-memory/agent-import-trust-memory.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
