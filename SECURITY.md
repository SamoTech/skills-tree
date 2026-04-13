# \U0001f512 Security Policy

## Supported Versions

Skills Tree is a documentation repository. There is no executable code deployed in production.
However, we take security seriously for the following surfaces:

| Surface | Supported |
|---|---|
| `docs/index.html` (GitHub Pages viewer) | ✅ Active |
| GitHub Actions workflows (`.github/workflows/`) | ✅ Active |
| Skill file content (code examples) | ✅ Reviewed |
| `meta/` and `skills/` markdown files | ✅ Reviewed |
| Dependency Auditor snippet execution (Phase 3) | ✅ Active |

---

## Reporting a Vulnerability

If you discover a security issue in this repository — including but not limited to:

- **XSS or injection vulnerabilities** in the `docs/index.html` viewer
- **Malicious code examples** embedded in skill files
- **Supply-chain risks** in GitHub Actions workflows
- **Exposed secrets or credentials** accidentally committed
- **Prompt injection payloads** embedded in skill descriptions
- **Adversarial snippets** designed to abuse the Dependency Auditor

Please **do not open a public GitHub issue**.

Instead, report it privately:

1. **Email:** Use GitHub's [private vulnerability reporting](https://github.com/SamoTech/skills-tree/security/advisories/new)
2. **Response time:** We aim to acknowledge within **48 hours** and resolve within **7 days** for critical issues
3. **Credit:** Responsible disclosures will be credited in the release notes

---

## Scope

### In Scope

- Any vulnerability in the static GitHub Pages site (`docs/`)
- Malicious or misleading code examples in skill `.md` files
- GitHub Actions workflow vulnerabilities (script injection, token exposure)
- Accidentally committed API keys, tokens, or credentials
- Adversarial snippets targeting the Phase 3 Dependency Auditor execution environment

### Out of Scope

- Issues in third-party frameworks or models *referenced* by skill files (report those upstream)
- Theoretical AI safety concerns in documented skills (open an issue for discussion instead)
- Social engineering attacks

---

## Security Best Practices for Contributors

When contributing skill files:

- ✅ **Never include real API keys, tokens, or passwords** in code examples — always use placeholders like `YOUR_API_KEY`
- ✅ **Use environment variables** for sensitive values in examples: `os.environ['API_KEY']`
- ✅ **Do not demonstrate actual exploits** — describe vulnerabilities conceptually, don't provide working attack code
- ✅ **Flag experimental skills** with `stability: experimental` if they involve risky operations
- ✅ **Include security notes** in skill files that involve privileged actions, file deletion, or network access

---

## Phase 3 Execution Gap — Network Constraints

> This section documents the threat model for the **Dependency Auditor** (`dependency-auditor.yml`),
> which executes Python code snippets from skill files in isolated virtual environments on
> GitHub Actions runners as part of Phase 3 of the Dependency Watchdog pipeline.

### What the Auditor Does

`dependency-auditor.yml` runs on pull requests that touch `skills/**/*.md` files and on a
weekly cron schedule. It:

1. Parses Python code blocks from skill Markdown files
2. Creates an isolated `venv` per skill using `tempfile.TemporaryDirectory()` + `venv.create(clear=True)`
3. Installs the skill's declared `deps` into that venv
4. Executes each snippet via `subprocess.run` with a 30-second timeout
5. Proposes a Yellow → Green badge promotion PR if all snippets pass

### The Network Constraint Risk

**The Risk:**
Since snippets run via `subprocess.run` on a GitHub Actions runner, a malicious snippet
(e.g. a PR disguising crypto mining, data exfiltration, or credential harvesting as a
skill code example) would have **full outbound network access** during execution.

**The Layered Mitigations (in order of current deployment):**

| Layer | Mitigation | Status |
|---|---|---|
| **Primary** | Ephemeral GH Actions runner — discarded after every job. No persistent state survives. | ✅ Active |
| **Secondary** | PR review gate — maintainers review all PRs before the audit workflow triggers on `pull_request`. External PRs do not auto-trigger execution. | ✅ Active |
| **Tertiary** | 30-second subprocess timeout — caps runaway or stalling snippets. | ✅ Active |
| **Escalation path** | Docker `--network=none` container for snippet execution — completely severs outbound network for the execution subprocess. | ⏳ Available if abuse is detected |

**Current Risk Assessment: LOW**

For the current scope — a curated, maintainer-reviewed repository — the ephemeral runner
model is the **primary and sufficient containment strategy**. The runner is discarded after
every job, so even a successful exfiltration attempt finds no persistent secrets, no
long-lived credentials, and no reusable environment.

### Escalation Procedure

If abuse is detected (e.g. a PR attempts network exfiltration from a snippet):

1. **Immediately** close the PR and block the contributor
2. **Report** via the private vulnerability channel above
3. **Enable** Docker `--network=none` execution by updating the `run_snippet()` call in
   `tools/dependency_auditor.py` to wrap the subprocess in:
   ```bash
   docker run --rm --network=none -v /tmp/snippet.py:/snippet.py python:3.11-slim python /snippet.py
   ```
4. **Audit** the Actions runner logs for the affected job to assess blast radius

### Note for Future Community Contributors

If this repository is ever opened to public, unreviewed PRs, the escalation to
Docker `--network=none` execution **must be implemented before** enabling auto-trigger
of the auditor on external PRs. Do not skip this step.

---

## Skill Security Categories

Skills in [`14-security/`](skills/14-security/) specifically cover agent safety patterns:

| Skill | Description |
|---|---|
| [Sandboxed Execution](skills/14-security/sandboxed-execution.md) | Run untrusted code in isolated environments |
| [Secret Scanning](skills/14-security/secret-scanning.md) | Detect credentials in agent outputs |
| [Human-in-the-Loop](skills/14-security/human-in-loop.md) | Require human approval for high-risk actions |
| [Input Sanitization](skills/14-security/input-sanitization.md) | Prevent prompt injection attacks |
| [Permission Checking](skills/14-security/permission-checking.md) | Scope agent capabilities to minimum required |
| [Audit Logging](skills/14-security/audit-logging.md) | Record all agent actions for review |
| [Rollback / Undo](skills/14-security/rollback-undo.md) | Reverse unintended agent actions |
| [Rate Limiting](skills/14-security/rate-limiting.md) | Cap agent tool calls to prevent runaway loops |
| [Harm Detection](skills/14-security/harm-detection.md) | Classify and block harmful outputs |
| [Privacy Preservation](skills/14-security/privacy-preservation.md) | Prevent leakage of PII and sensitive data |

---

## Acknowledgements

Thank you to everyone who responsibly discloses security issues and helps keep the AI agent community safer.

---

*Maintained by [@SamoTech](https://github.com/SamoTech) · Last updated: April 2026*
