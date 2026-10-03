---
title: "Security Scanning"
category: 05-code
level: advanced
stability: stable
version: v2
added: "2025-03"
updated: "2026-10-03"
description: "Detect source vulnerabilities, dependency advisories, and exposed secrets with separate scanners and enforce explicit severity thresholds in CI."
---

# Security Scanning

## Purpose

Security scanning is a layered verification step. Source analysis, dependency analysis, and secret detection have different coverage boundaries. A clean result from one scanner is not proof that an application is secure.

## Inputs / Outputs

| Item | Type | Required | Notes |
|---|---|---:|---|
| Source tree | filesystem | yes | Code and configuration |
| Dependency manifest/lockfile | file | recommended | Enables dependency analysis |
| Secret policy | config | recommended | Defines exclusions and fixtures |
| Severity threshold | policy | yes | Explicit build-failure boundary |
| Findings | structured records | yes | Scanner, rule, path, severity, evidence |
| Gate result | pass/fail | yes | Derived from policy |

## Runnable Example

```bash
set -euo pipefail
bandit -r src -ll -f json -o bandit.json
python - <<'PY'
import json
from pathlib import Path
report = json.loads(Path("bandit.json").read_text())
high = [x for x in report.get("results", []) if x.get("issue_severity") == "HIGH"]
print(f"bandit_high={len(high)}")
if high:
    raise SystemExit("security gate failed")
PY
```

## Operating Rules

- Preserve raw scanner reports before normalization.
- Define failure thresholds in repository policy, not prose.
- Use scoped, expiring exceptions instead of silently suppressing findings.
- Redact secrets from CI logs and reports.
- Scan resolved dependency graphs when lockfiles are available.

## Failure Modes

| Failure | Cause | Mitigation |
|---|---|---|
| False negative | Scanner coverage gap | Use complementary scanners and review high-risk changes |
| False positive | Rule matches safe code | Preserve evidence and use scoped exceptions |
| Secret leakage | Raw output exposes secret material | Redact before publication |
| Dependency blind spot | Only direct dependencies scanned | Scan the resolved graph |
| Gate bypass | Result is advisory only | Make policy threshold a CI exit condition |

## Evidence

- Bandit: https://bandit.readthedocs.io/
- npm audit: https://docs.npmjs.com/cli/commands/npm-audit
- OWASP SAMM: https://owaspsamm.org/

Evidence status: references support the scanning guidance. No complete-coverage or security-certification claim is made.

## Related Skills

- secret-scanning
- dependency-management
- code-review
- secure-coding

## Changelog

| Version | Date | Change |
|---|---|---|
| v1 | 2025-03 | Initial entry |
| v2 | 2026-10 | Added layered scanning, explicit gate contract, and failure boundaries |
