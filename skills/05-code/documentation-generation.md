---
title: "Documentation Generation"
category: 05-code
level: advanced
stability: stable
version: v2
description: "Generate technical documentation from verified repository behavior, interfaces, configuration, and implementation evidence."
added: "2026-09"
related: [code-explanation, code-review, code-search]
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-05-code-documentation-generation.json)

# Documentation Generation

**Category:** `code`
**Skill Level:** `advanced`
**Stability:** `stable`
**Added:** 2026-09

### Description

Generate technical documentation from verified repository behavior, interfaces, configuration, and implementation evidence. The skill is evidence-first: inspect actual state before acting, preserve existing contracts, and verify the result before reporting completion.

### Inputs / Outputs

| Direction | Field | Type | Contract |
|---|---|---|---|
| Input | sources | object | Code, interfaces, configuration, and tests that define actual behavior |
| Input | scope | string | README, API reference, architecture, runbook, or developer guide |
| Output | documentation | object | Sections accurate to verified behavior, with prerequisites and limits |
| Output | evidence | list of string | File references backing every documented claim |

### Procedure
1. Read the implementation, configuration, and tests that define actual behavior.
2. Document only what is verified; mark inferred or planned behavior explicitly.
3. Include prerequisites, setup steps, and known limits; docs that omit prerequisites fail users.
4. Keep runnable examples synchronized with the code they demonstrate.
5. Cross-check every claim against the repository before publishing.

### Example

```python
claims = {'install': 'pip install skills-tree', 'requires_python': '3.10+'}
assert all(isinstance(v, str) for v in claims.values())
print('each documented claim must carry a repository file reference')
```

### Related Skills

- [Code Explanation](code-explanation.md) - verified behavior traces feed the docs
- [Code Review](code-review.md) - review documentation claims like code changes
- [Code Search](code-search.md) - locate the interfaces being documented

## Failure Modes

- Documenting assumptions as facts.
- Inventing interfaces or capabilities the repository does not have.
- Omitting prerequisites or operational constraints.
- Letting documentation drift after behavior changes.

## Changelog
- v2 (2026-11): Structural modernization; added the input/output contract table, a deterministic example, an execution procedure, and corpus-verified related links.
- v1 (2026-09): Initial entry.

## Evidence

- https://agentskills.io/specification

Evidence status: implementation guidance only; no benchmark claim is made without reproducible evidence.
