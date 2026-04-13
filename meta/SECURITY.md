# Security Policy

## Dependency Trust Contract

Skills Tree is documentation infrastructure. Every skill that references executable code
is covered by the **Four-State Dependency Trust Contract**, documented in full in
[`meta/badge-states.md`](badge-states.md).

| Badge | Meaning | User action |
|---|---|---|
| ![unscanned](https://img.shields.io/badge/deps-unscanned-lightgrey?style=flat-square) | Not yet audited | Inspect manually before use |
| ![machine-inferred](https://img.shields.io/badge/deps-machine--inferred-yellow?style=flat-square) | AST-extracted, PyPI-confirmed, not human-run | Verify versions before production use |
| ![verified](https://img.shields.io/badge/deps-verified-22c55e?style=flat-square&color=22c55e) | Human-confirmed, no active CVEs | Safe to copy-paste |
| ![advisory](https://img.shields.io/badge/deps-%E2%9A%A0%EF%B8%8F%20CVE-critical?style=flat-square) | Active CVE in OSV database | Do NOT use in production |

## CVE Response SLA

**Badges are updated within 15 minutes** of a CVE appearing in the
[OSV database](https://osv.dev) for any package in `meta/skills-sbom.cdx.json`.

This is enforced by `.github/workflows/osv-watch.yml` (cron: `*/15 * * * *`).

When a CVE is detected:
1. Affected skill badges transition to `advisory` (red) automatically
2. A GitHub Issue is opened with the full CVE details and affected skill list
3. Maintainers are notified via the issue
4. Resolution requires a human verification PR confirming the skill works with a patched version
5. On merge, the badge returns to `verified` (green)

## Reporting a Vulnerability in a Skill

If you discover a vulnerability in a skill's code snippet (e.g., prompt injection,
excessive tool permissions, secret exposure), please:

1. **Do NOT open a public issue** for unresolved vulnerabilities
2. Email `security@samotech.dev` or use [GitHub Private Vulnerability Reporting](https://github.com/SamoTech/skills-tree/security/advisories/new)
3. Include: the skill file path, the vulnerability type, and a minimal reproduction

We will respond within **48 hours** and publish a CVE advisory + skill patch within **7 days**.

## Security-Sensitive Skill Categories

PRs touching the following categories require **two maintainer approvals** (enforced in `CODEOWNERS`):

- `skills/14-security/` — all security skills
- `skills/07-tool-use/` — all tool-use skills (excessive permissions risk)
- `blueprints/` — production architectures

All skills in these categories must include a `# ⚠️ Scope this to your trust boundary`
comment on any line that grants agent permissions or calls external APIs.

## Snippet Audit Pipeline

Every PR touching skill code blocks is automatically scanned by:

- **`promptfoo`** — prompt injection patterns, PII exposure, excessive agency
- **`gitleaks`** — secrets accidentally committed in example code
- **Custom linter** — flags `eval()`, `exec()`, shell injection patterns,
  unrestricted `**kwargs` forwarding to tool calls

Failed checks block merge until resolved.

## SBOM

The full Software Bill of Materials for all skill dependencies is at
[`meta/skills-sbom.cdx.json`](skills-sbom.cdx.json) in CycloneDX 1.5 format.

Generated nightly by `tools/ast_sweep.py` and scannable with:
```bash
pip install grype
grype sbom:meta/skills-sbom.cdx.json --fail-on critical
```

## Scope

This security policy covers the **documentation and code snippets** in this repository.
It does not cover the security of the AI models, APIs, or frameworks referenced in skills —
those are governed by their respective projects.
