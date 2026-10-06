---
title: "Agent Skill Security Audit"
category: 14-security
level: advanced
stability: experimental
description: "Audit an agent skill and its bundled resources before installation or execution, checking declared behavior, permissions, credential access, network egress, obfuscation, and sandbox requirements."
added: "2026-10"
updated: "2026-10"
version: v1
related: [sandboxed-execution, secret-scanning, permission-checking, input-sanitization, audit-logging]
---

# Agent Skill Security Audit

## Description

An agent skill is executable trust-boundary content when it contains instructions, scripts, hooks, references, or tool permissions. Audit the complete skill package before installation or execution rather than trusting its description or publisher metadata.

The audit is primarily static and compares declared behavior with the actual SKILL.md instructions and every bundled executable/resource file. Check for unexpected permission grants, credential reads, network egress, obfuscated content, hidden behavior, unsafe hooks, and mismatch between advertised and observable behavior.

Dynamic analysis is optional and must run only in an isolated sandbox with synthetic or no credentials, bounded resources, controlled network access, and explicit teardown. An audit result is evidence for a trust decision; it is not a guarantee that a skill is benign.

## Inputs / Outputs

| Input | Type | Required | Description |
|---|---|---:|---|
| skill_root | path | yes | Root directory containing the skill manifest and bundled resources |
| declared_permissions | list | no | Permissions/tools explicitly declared by the skill or host metadata |
| runtime_policy | object | no | Sandbox, filesystem, network, credential, and execution constraints |
| audit_mode | enum | yes | static or sandboxed |

Output is a structured audit record containing findings, evidence locations, severity, confidence, declared-vs-observed deltas, sandbox requirements, and a disposition such as allow, review, or deny.

## Audit Procedure

1. Parse frontmatter and record declared name, purpose, permissions, compatibility, and provenance.
2. Inventory SKILL.md, scripts, hooks, binaries, configuration, references, and generated files under the skill root.
3. Compare advertised behavior with actual instructions and executable content.
4. Identify credential and sensitive-file access, including environment variables, SSH material, cloud credentials, token stores, and unrelated user data.
5. Identify network destinations and egress mechanisms. Treat undeclared network access as a finding requiring review.
6. Inspect for shell/process execution, package installation, dynamic code loading, obfuscation, encoded payloads, persistence, or attempts to hide behavior from the user.
7. Compare declared tool permissions with the minimum permissions required by observed behavior.
8. Record exact evidence locations and never treat absence of a detected pattern as proof of safety.
9. If dynamic analysis is required, run only in an isolated sandbox with synthetic credentials, bounded resources, controlled egress, and no access to the auditor real environment.
10. Produce a fail-closed disposition when high-confidence critical behavior is incompatible with the declared purpose or execution policy.

## Runnable Example

```python
from pathlib import Path
import re

SENSITIVE_PATHS = (".env", ".ssh", ".aws", ".config/gcloud")

def audit_skill(root: Path) -> list[dict]:
    findings = []
    for path in sorted(p for p in root.rglob("*") if p.is_file()):
        rel = path.relative_to(root).as_posix()
        text = path.read_text(errors="replace") if path.suffix in {".md", ".py", ".sh", ".json", ".yaml", ".yml"} else ""
        if any(token in rel for token in SENSITIVE_PATHS):
            findings.append({"rule": "sensitive-path", "severity": "high", "path": rel})
        if re.search(r"(curl|wget|requests\\.(get|post)|urllib\\.request)", text, re.I):
            findings.append({"rule": "network-egress", "severity": "medium", "path": rel})
    return findings

print(audit_skill(Path("./skill-under-review")))
```

This example is a bounded static signal detector, not a malware detector. Production audits need language-aware analysis, archive/binary handling, symlink controls, policy evaluation, and reproducible evidence capture.

## Failure Modes

| Failure | Cause | Mitigation |
|---|---|---|
| Trusting metadata | Description differs from bundled behavior | Audit executable/resource contents and record declared-vs-observed deltas |
| Credential exposure | Skill reads real secrets or credential stores | Deny or isolate access; use synthetic credentials for dynamic testing |
| Hidden egress | Network access is not declared or constrained | Default to no network and allow only policy-approved destinations |
| Permission overreach | Skill requests tools broader than its purpose | Apply least privilege and require explicit review for elevated permissions |
| Obfuscation | Encoded/dynamic content hides behavior | Flag for manual/static analysis and preserve exact evidence location |
| Sandbox escape | Dynamic test reaches the host | Use a maintained isolated runtime with resource, filesystem, and network controls |
| False negative | Static checks miss behavior | Treat audit output as evidence, not a safety guarantee; use layered controls |
| False positive | Benign implementation matches a heuristic | Record confidence and require contextual review rather than automatic condemnation |

## Design Rules

1. Treat every third-party skill package as untrusted input until its behavior is reviewed.
2. Audit the complete package, not only SKILL.md frontmatter.
3. Preserve provenance and exact evidence locations for every finding.
4. Compare declared permissions and behavior against the least-privilege execution policy.
5. Default dynamic analysis to synthetic/no credentials, bounded resources, and restricted network access.
6. Never claim that a static scan proves a skill is safe.
7. Keep audit evidence separate from authorization; a passing audit does not itself grant permission to execute a skill.
8. Prefer deterministic checks for path, permission, secret, network, and package-integrity findings where practical.

## References

- OWASP Secure Agent Playbook issue #21: https://github.com/OWASP/secure-agent-playbook/issues/21
- 2026 research on detecting malicious agent skills: https://arxiv.org/abs/2602.06547
- Skills Tree Sandboxed Execution: sandboxed-execution.md
- Skills Tree Secret Scanning: secret-scanning.md

Evidence status: the cited sources support the audit problem and defensive methodology. This skill does not claim complete malware detection, compliance certification, or universal safety.

## Related Skills

- [Sandboxed Execution](sandboxed-execution.md)
- [Secret Scanning](secret-scanning.md)
- [Permission Checking](permission-checking.md)
- [Input Sanitization](input-sanitization.md)
- [Audit Logging](audit-logging.md)

## Changelog

| Date | Version | Change |
|---|---|---|
| 2026-10 | v1 | Added demand-driven contract for pre-installation and pre-execution agent-skill security auditing |
