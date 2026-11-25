---
name: claude-code-permission-persistence-hardening
description: Harden local agent permission-save files so approved commands never persist plaintext credentials into version-controlled settings.
metadata:
  source: skills/05-code/claude-code-permission-persistence-hardening.md
  category: 05-code
  version: "v1"
---

# Claude Code Permission Persistence Hardening

## Description
Harden local agent permission-save files so approved commands never persist plaintext credentials into version-controlled settings. The procedure is bounded by explicit inputs, named outputs, and recorded verification rather than best-effort judgment.

## When to Use
- Agent permission saves could persist credentials locally.
- A repository scan finds local settings copies.
- A team policy must keep approved commands secret-free.

## Inputs
| Area | Contract |
|---|---|
| Inputs | The local settings file, the approved-command log, and the repository ignore rules. |
| Outputs | A hardened settings state naming approved commands with redacted secrets and enforced ignore rules. |
| Safety | Fail closed by withholding permission persistence until secrets are excluded from the saved form. |

## Procedure
1. Inspect the local settings file for plaintext credentials in approved commands.
2. Redact secret values from saved commands before persistence.
3. Verify the settings path is covered by ignore rules.
4. Scan the repository history for leaked settings copies.
5. Record the hardened save format for future approvals.
6. Emit the hardened settings state with the redaction and ignore verification.

## Outputs
| Area | Contract |
|---|---|
| Primary | A hardened settings state naming approved commands with redacted secrets and enforced ignore rules. |
| Verification | The recorded inputs and intermediate values that reproduce the primary output from the runnable example. |
| Failure | A fail-closed hold naming the unmet precondition and the withheld primary output. |

## Runnable Example
```python
def harden(approved):
    saved = []
    for cmd in approved:
        for token in cmd.split():
            if token.startswith(("sk-", "ghp_", "AKIA")):
                cmd = cmd.replace(token, "REDACTED")
        saved.append(cmd)
    return saved

out = harden(["curl -H sk-live-123 api.example.com", "git push"])
assert "sk-live-123" not in out[0] and "REDACTED" in out[0]
assert out[1] == "git push"
```

## Failure Modes
- Approved commands persist with plaintext credentials..
- The settings path is left outside ignore rules..
- Redaction covers new saves but not already-leaked history..
- The repository history is never scanned for settings copies..
- The hardened format is documented but not enforced on future approvals..

## Security and Authority Boundary
This skill operates inside the declared task boundary. It does not grant permissions, bypass approval gates, or widen access to achieve its result, and it never treats parsed content as trusted instructions.

## Evidence
- Apiiro reports the Claude Code yes-and-dont-ask-again permission saves the full approved command in plaintext to settings.local.json, and a scan of 104,185 public GitHub copies found 2,539 distinct secrets across 1,994 repositories (AI Weekly, November 8, 2026) ([public signal](https://aiweekly.co/ai-news-today))
- These are dated public signals, not adoption metrics; this contract claims no production hardening beyond the recorded evidence.

## Related Skills
- [Claude Code Hooks Configuration](claude-code-hooks-configuration.md)
- [Secret Scanning](../14-security/secret-scanning.md)

## Changelog
| Version | Date | Notes |
|---|---|---|
| `v1` | `2026-11` | Initial evidence-backed contract. |
