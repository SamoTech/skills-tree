---
title: "Git Diff Reading"
category: 01-perception
level: intermediate
stability: stable
description: "Apply git diff reading in AI agent workflows."
added: "2025-03"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-01-perception-git-diff-reading.json)

# Git Diff Reading
Category: perception | Level: intermediate | Stability: stable | Version: v1

## Description
Parse unified diff output into structured change objects — added/removed lines, file paths, hunks.

## Inputs
- `diff_text`: unified diff string (from `git diff`)

## Outputs
- List of file changes: `{path, added_lines, removed_lines, hunks}`

## Example
```python
import unidiff
patch = unidiff.PatchSet.from_string(diff_text)
for pf in patch:
    print(f"{pf.path}: +{pf.added} -{pf.removed}")
    for hunk in pf:
        for line in hunk:
            if line.is_added: print(f"  + {line.value}", end="")
```

## Frameworks
| Framework | Method |
|---|---|
| Python | `unidiff`, `whatthepatch` |
| LangChain | Custom loader |
| GitHub API | `/repos/{owner}/{repo}/pulls/{n}/files` |

## Failure Modes
- Binary file diffs contain no line data
- Rename detection may list file twice

## Related
- `code-reading.md` · `file-system-reading.md`

## Changelog
- v1 (2026-04): Initial entry
