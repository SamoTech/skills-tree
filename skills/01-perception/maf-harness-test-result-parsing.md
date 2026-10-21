---
title: "Maf Harness Test Result Parsing"
category: 01-perception
level: advanced
stability: experimental
description: "Parse Microsoft Agent Framework harness result artifacts so pass, fail, and flaky outcomes are read deterministically."
added: "2026-10"
version: v1
related: [agent-trace-span-parsing, agent-eval-report-parsing]
tags: [microsoft-agent-framework, harness, parsing, testing]
---
# Maf Harness Test Result Parsing

## Description
Parse Microsoft Agent Framework harness result artifacts so pass, fail, and flaky outcomes are read deterministically. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A Microsoft Agent Framework harness run has produced result artifacts and the outcomes must be extracted before reporting.
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
3. Parse the harness result artifact, extract case identifiers, statuses, and failure messages, and reject artifacts whose schema version is unsupported.
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
def parse_harness_results(artifact):
    if artifact.get("schema") != "maf-harness/1":
        raise ValueError("unsupported harness artifact schema")
    cases = artifact.get("cases", [])
    if not cases:
        raise ValueError("harness artifact has no cases")
    return {"passed": sum(1 for c in cases if c["status"] == "passed"), "total": len(cases)}
art = {"schema": "maf-harness/1", "cases": [{"id": "t1", "status": "passed"}, {"id": "t2", "status": "failed"}]}
assert parse_harness_results(art) == {"passed": 1, "total": 2}
```

## Failure Modes
- Harness artifacts are parsed without checking the declared schema version.
- Flaky cases are counted as passed on their last attempt and hide real instability.
- Failure messages are dropped and downstream triage cannot reproduce the failing case.
- Artifact contents are logged in full and leak prompt fixtures or credentials into shared logs.
- An empty case list is treated as a successful run instead of a fail-closed error.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- Microsoft documents the Microsoft Agent Framework harness release for running and evaluating agent workloads (devblogs.microsoft.com, dated July 23, 2026) ([public signal](https://devblogs.microsoft.com/agent-framework/the-microsoft-agent-framework-harness-is-now-released/))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Agent Trace Span Parsing](../01-perception/agent-trace-span-parsing.md)
- [Agent Eval Report Parsing](../01-perception/agent-eval-report-parsing.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
