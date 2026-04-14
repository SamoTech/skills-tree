# Skill Versioning Spec

This document defines the **v1 / v2 / v3** versioning system for every skill in Skills Tree. All new and updated skills must include a `Version:` field in their frontmatter.

---

## Version Definitions

| Version | Label | Requirements | Badge |
|---|---|---|---|
| **v1** | Stub | Description, basic I/O table, no code example | 🟡 Yellow |
| **v2** | Expanded | Everything in v1 + working code example + Failure Modes + Prompt Patterns | 🟠 Orange |
| **v3** | Battle-Tested | Everything in v2 + Model Comparison table (3+ models rated) + verified examples + changelog entries | 🟢 Green |

---

## Frontmatter Field

Add `Version:` to every skill file immediately after `Stability:`:

```markdown
**Category:** `reasoning`  
**Skill Level:** `advanced`  
**Stability:** `stable`  
**Version:** `v2`  
**Added:** `2025-03`  
**Last Updated:** `2026-04`
```

---

## PR Title Convention

When upgrading a skill, use this PR title format:

```
improve: [skill-name] — v1→v2
improve: [skill-name] — v2→v3
```

Examples:
- `improve: causal-reasoning — v1→v2`
- `improve: memory-injection — v2→v3`

This convention is detected by `skill-upgrade-comment.yml` which automatically posts a congratulatory comment and proposes the next upgrade step.

---

## "Battle-Tested" Auto-Badge

Skills that reach **v3** automatically receive the `Battle-Tested` label via CI. The label is applied by `skill-upgrade-comment.yml` when it detects a `v2→v3` upgrade in the PR title.

---

## Upgrade Checklist

### v1 → v2 checklist
- [ ] `Version: v2` set in frontmatter  
- [ ] Working Python code example added (`## Example` section)  
- [ ] `## Failure Modes` section added with at least 3 rows  
- [ ] `## Prompt Patterns` section added with at least 2 patterns  
- [ ] `Last Updated` date updated  

### v2 → v3 checklist
- [ ] `Version: v3` set in frontmatter  
- [ ] `## Model Comparison` table populated for GPT-4o, Claude 3.7 Sonnet, Gemini 2.0 Flash  
- [ ] All example snippets are verified runnable  
- [ ] Changelog entry added with `| YYYY-MM | v3 | ... |`  
- [ ] PR title follows `improve: [skill-name] — v2→v3` convention  

---

## Current Version Distribution

> Updated automatically by CI on each merge. See [LEADERBOARD.md](LEADERBOARD.md) for the live counts.

| Version | Count | % of Total |
|---|---|---|
| v1 (Stub) | — | — |
| v2 (Expanded) | — | — |
| v3 (Battle-Tested) | — | — |

---

## Who Should Upgrade Skills?

Anyone! Pick a skill that's still at v1, run the upgrade checklist, and open a PR. See [CONTRIBUTING.md](../CONTRIBUTING.md) for the full workflow. High-value targets:

- Skills in `01-perception`, `02-reasoning`, and `03-memory` (highest traffic)
- Skills referenced by `/systems` or `/blueprints` files
- Skills with no `Example` section at all
