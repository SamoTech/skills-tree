---
name: evidence-verification
description: Verify meaningful repository changes with direct implementation, test, CI, and documentation evidence.
metadata:
  source: skills/15-orchestration/evidence-verification.md
  category: 15-orchestration
---

# Evidence Verification

## Description

Verify completion claims against direct repository, test, CI, security, and documentation evidence. Separate verified facts from assumptions and unresolved risks.

1. Identify the claim being verified and its strongest evidence source.
2. Inspect the actual changed implementation.
3. Execute or inspect required validation gates.
4. Verify the resulting main commit and relevant CI runs.
5. Check security implications and documentation synchronization.
6. Report verified facts separately from unresolved risks and assumptions.
7. Use the precise completion states defined by AGENTS.md.

## Runnable example

```bash
git show --stat --oneline HEAD
python -m pytest -q
git status --short
```

## Inputs / outputs / failure modes

| Input | Output | Failure mode |
|---|---|---|
| Changed files | Scope evidence | Claimed change is not present |
| Tests | Behavioral evidence | Tests are missing or failing |
| CI checks | Repository-level evidence | Required check is pending/failing |
| Security scans | Risk evidence | Security result is absent |
| Documentation | State continuity | Docs still describe old behavior |

## Related

- `repository-state-load.md`
- `documentation-drift-resolution.md`
- `execution-handoff.md`

## Evidence

- AGENTS.md
- AI_CONSTITUTION.md
- meta/AGENT_HANDOFF_PROTOCOL.md
- GitHub commit, PR, and Actions evidence
