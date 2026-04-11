# 🔒 Security Policy

## Supported Versions

Skills Tree is a documentation repository. There is no executable code deployed in production.
However, we take security seriously for the following surfaces:

| Surface | Supported |
|---|---|
| `docs/index.html` (GitHub Pages viewer) | ✅ Active |
| GitHub Actions workflows (`.github/workflows/`) | ✅ Active |
| Skill file content (code examples) | ✅ Reviewed |
| `meta/` and `skills/` markdown files | ✅ Reviewed |

---

## Reporting a Vulnerability

If you discover a security issue in this repository — including but not limited to:

- **XSS or injection vulnerabilities** in the `docs/index.html` viewer
- **Malicious code examples** embedded in skill files
- **Supply-chain risks** in GitHub Actions workflows
- **Exposed secrets or credentials** accidentally committed
- **Prompt injection payloads** embedded in skill descriptions

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
