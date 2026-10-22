---
name: agent-import-code-injection-prevention
description: Prevent code injection through imported agent artifacts by quarantining and validating imports before execution.
metadata:
  source: skills/14-security/agent-import-code-injection-prevention.md
  category: 14-security
  version: "v1"
---

# Agent Import Code Injection Prevention

## Description
Prevent code injection through imported agent artifacts by quarantining and validating imports before execution. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- An agent runtime imports external agent code and must prevent the import path from executing injected code.
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
3. Quarantine imported artifacts, scan for import-time execution paths, validate the declared entry points against the manifest, and fail closed on any undeclared executable behavior.
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
def validate_import(manifest, artifact):
    for entry in artifact["entry_points"]:
        if entry not in manifest["declared_entry_points"]:
            return {"verdict": "REJECT", "reason": "undeclared entry point: " + entry}
    for pattern in artifact.get("import_time_calls", []):
        if pattern in {"exec", "eval", "system"}:
            return {"verdict": "REJECT", "reason": "import-time execution: " + pattern}
    return {"verdict": "ACCEPT"}
manifest = {"declared_entry_points": {"run_task"}}
assert validate_import(manifest, {"entry_points": ["run_task"], "import_time_calls": []})["verdict"] == "ACCEPT"
assert validate_import(manifest, {"entry_points": ["run_task"], "import_time_calls": ["eval"]})["verdict"] == "REJECT"
```

## Failure Modes
- Imported artifacts are executed directly and import-time hooks run before validation.
- Entry points are validated by name only and a declared name executes undeclared behavior.
- Quarantine is skipped for packages from a known registry and trust replaces validation.
- Injection findings are logged but the artifact runs anyway to keep the workflow moving.
- The manifest is authored by the artifact itself and validation is circular.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- The AWS security bulletin for the Bedrock AgentCore Starter Toolkit records import-agent code-injection as a live CVE class that import paths must prevent (aws.amazon.com, dated October 2026) ([public signal](https://aws.amazon.com/security/security-bulletins/2026-127-aws/))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Input Sanitization](../14-security/input-sanitization.md)
- [Sandboxed Execution](../14-security/sandboxed-execution.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
