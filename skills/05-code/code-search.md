---
title: "Code Search"
category: 05-code
level: basic
stability: stable
version: v2
description: "Locate relevant code by explicit symbol, behavior, dependency, or file criteria and verify matches before editing."
added: "2026-09"
related: [git-diff-reading, code-review, debugging]
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-05-code-code-search.json)

# Code Search

**Category:** `code`
**Skill Level:** `basic`
**Stability:** `stable`
**Added:** 2026-09

### Description

Locate relevant code by explicit symbol, behavior, dependency, or file criteria and verify matches before editing. The skill is evidence-first: inspect actual state before acting, preserve existing contracts, and verify the result before reporting completion.

### Inputs / Outputs

| Direction | Field | Type | Contract |
|---|---|---|---|
| Input | criteria | object | Explicit symbols, strings, paths, or dependency names to locate |
| Input | scope | list of string | Roots to search and exclusions; declare them before searching |
| Output | matches | list of object | file:line with a snippet and the reason it matches |
| Output | coverage | object | What was searched, with what tooling, and what was skipped |

### Procedure
1. Turn the information need into explicit criteria: symbols, literals, paths, or dependency names.
2. Choose tooling (ripgrep, symbol index, dependency graph) and search the declared scope.
3. Record each match with file, line, snippet, and why it matches.
4. Read the surrounding context to confirm relevance before editing anything.
5. Report gaps: what the search could not cover and what that means for confidence.

### Example

```python
files = ['src/api.py', 'src/models/user.py', 'tests/test_api.py']
criteria = 'api'
matches = [f for f in files if criteria in f]
assert matches == ['src/api.py', 'tests/test_api.py']
print(matches)
```

### Related Skills

- [Git Diff Reading](../01-perception/git-diff-reading.md) - scope searches to a change set
- [Code Review](code-review.md) - verified matches feed review findings
- [Debugging](debugging.md) - search is the first step of isolation

## Failure Modes

- Searching an undeclared scope and reporting the result as complete.
- Treating a textual match as behavioral relevance without reading context.
- Editing based on an unverified match.
- Hiding skipped files or exclusions from the coverage report.

## Changelog
- v2 (2026-11): Structural modernization; added the input/output contract table, a deterministic example, an execution procedure, and corpus-verified related links (replaced the non-corpus code-reading.md link with git-diff-reading).
- v1 (2026-09): Initial entry.

## Evidence

- https://agentskills.io/specification

Evidence status: implementation guidance only; no benchmark claim is made without reproducible evidence.
