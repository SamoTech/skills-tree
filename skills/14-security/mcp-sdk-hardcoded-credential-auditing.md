---
title: "Mcp Sdk Hardcoded Credential Auditing"
category: 14-security
level: advanced
stability: experimental
description: "Audit agent and MCP SDK code and images for hardcoded credentials before deployment or import."
added: "2026-10"
version: v1
related: [secret-scanning, dependency-integrity-verification]
tags: [credentials, auditing, supply-chain, mcp]
---
# Mcp Sdk Hardcoded Credential Auditing

## Description
Audit agent and MCP SDK code and images for hardcoded credentials before deployment or import. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- A team imports an MCP SDK or agent package and must prove it contains no hardcoded credentials before use.
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
3. Scan the artifact source and images for credential patterns, verify every candidate finding with context, and record pass or fail verdicts with the pattern evidence per file.
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
def audit_hardcoded_credentials(files, patterns):
    findings = []
    for name, content in files.items():
        for label, pattern in patterns.items():
            if pattern in content and "example" not in content.split(pattern)[0][-30:]:
                findings.append({"file": name, "kind": label})
    return {"verdict": "FAIL" if findings else "PASS", "findings": findings}
files = {"sdk.py": "TOKEN = "live_abc123"", "docs.py": "TOKEN = "example_token""}
patterns = {"api_token": "live_"}
result = audit_hardcoded_credentials(files, patterns)
assert result["verdict"] == "FAIL" and result["findings"] == [{"file": "sdk.py", "kind": "api_token"}]
```

## Failure Modes
- Scan patterns cover only API keys and miss connection strings and private keys.
- Example or test fixtures are flagged and the audit drowns in false positives.
- Findings are reported without file and context evidence and cannot be verified.
- Container image layers are skipped and credentials baked into base images pass the audit.
- A passing static scan is treated as proof of safety and dynamic checks are skipped.

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- The HaiND VulnCheck batch reporting documents a 9.4-severity hardcoded credential in the agent and MCP SDK ecosystem, defining the audit this skill performs (al-ice.ai, dated October 2026) ([public signal](https://al-ice.ai/posts/2026/10/haind-vulncheck-day-two-22-agent-mcp-cves-october-2026/))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Secret Scanning](../14-security/secret-scanning.md)
- [Dependency Integrity Verification](../14-security/dependency-integrity-verification.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-10` | Initial evidence-backed contract. |
