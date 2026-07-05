---
title: "Git Diff Reading"
category: 01-perception
level: intermediate
stability: stable
description: "Enable AI agents to parse unified diff output from git operations into structured change objects for code review, changelog generation, and impact analysis."
added: "2025-03"
version: "v2"
last_updated: "2026-07"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-01-perception-git-diff-reading.json)

# Git Diff Reading

**Category:** `01-perception`
**Skill Level:** `intermediate`
**Stability:** `stable`
**Version:** `v2`
**Added:** `2025-03`
**Last Updated:** `2026-07`

---

## Description

Git Diff Reading enables an agent to parse unified diff text — produced by `git diff`, `git show`, or patch files — into structured change objects that enumerate added lines, removed lines, and modified file paths. It is the perception layer for code review agents, PR summarizers, changelog generators, and security scanners. The skill handles multi-file diffs, binary file markers, and renamed/moved file detection.

---

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `diff_text` | `string` | ✅ | Raw unified diff string (output of `git diff` or patch file contents) |
| `context_lines` | `int` | ❌ | Number of context lines to retain per hunk (default: 3) |
| `include_binary` | `bool` | ❌ | Whether to include binary file change markers (default: false) |
| `filter_paths` | `list[string]` | ❌ | Only return changes for files matching these path prefixes |

---

## Outputs

| Output | Type | Description |
|---|---|---|
| `files` | `list[dict]` | Per-file change objects |
| `files[].path` | `string` | File path (new path for renames) |
| `files[].old_path` | `string` | Previous path (only for renames/moves) |
| `files[].status` | `string` | `added` \| `deleted` \| `modified` \| `renamed` \| `binary` |
| `files[].additions` | `int` | Number of added lines |
| `files[].deletions` | `int` | Number of deleted lines |
| `files[].hunks` | `list[dict]` | Individual change hunks with line ranges and diff content |
| `summary` | `dict` | `{total_files, total_additions, total_deletions}` |

---

## Example

```python
import unidiff

def parse_git_diff(diff_text: str, filter_paths: list = None) -> dict:
    patch_set = unidiff.PatchSet(diff_text)
    files = []
    for patched_file in patch_set:
        path = patched_file.path
        if filter_paths and not any(path.startswith(p) for p in filter_paths):
            continue
        files.append({
            "path": path,
            "status": "added" if patched_file.is_added_file else
                      "deleted" if patched_file.is_removed_file else "modified",
            "additions": patched_file.added,
            "deletions": patched_file.removed,
            "hunks": [{"section": str(h.section_header),
                       "lines": [str(l) for l in h]} for h in patched_file],
        })
    total_add = sum(f["additions"] for f in files)
    total_del = sum(f["deletions"] for f in files)
    return {"files": files, "summary": {"total_files": len(files),
                                         "total_additions": total_add,
                                         "total_deletions": total_del}}

import subprocess
diff_text = subprocess.check_output(["git", "diff", "HEAD~1"], text=True)
result = parse_git_diff(diff_text)
print(result["summary"])
# → {"total_files": 4, "total_additions": 87, "total_deletions": 23}
```

```python
# Extended — generate a natural language PR summary
def summarize_diff(diff_text: str) -> str:
    parsed = parse_git_diff(diff_text)
    lines = [f"Changed {parsed['summary']['total_files']} files: "
             f"+{parsed['summary']['total_additions']} -{parsed['summary']['total_deletions']}"]
    for f in parsed["files"]:
        lines.append(f"  [{f['status'].upper()}] {f['path']} (+{f['additions']}/-{f['deletions']})")
    return "\n".join(lines)

print(summarize_diff(diff_text))
```

---

## Frameworks & Models

| Framework / Model | Implementation | Since |
|---|---|---|
| Python `unidiff` | `PatchSet(diff_text)` — parses unified diff into Python objects | v1 |
| Python `whatthepatch` | Lightweight unified diff parser | v1 |
| `gitpython` | `repo.git.diff()` to generate and parse diffs programmatically | v1 |
| GitHub REST API | `GET /repos/{owner}/{repo}/pulls/{pull_number}/files` | v1 |
| LangChain `GitLoader` | Loads git history as documents for LLM context | v0.1 |
| GPT-4o | Reads raw diff text natively; excellent code review quality | 2024-05 |
| Claude 3.7 Sonnet | Strong at summarizing and critiquing diffs | 2025-01 |
| Gemini 2.0 Flash | Good for quick diff summaries, weaker on security analysis | 2024-12 |

---

## Model Comparison

| Capability | GPT-4o | Claude 3.7 Sonnet | Gemini 2.0 Flash | Notes |
|---|---|---|---|---|
| Diff comprehension | 5 | 5 | 4 | Both top models excel at reading diffs |
| Security issue detection | 5 | 4 | 3 | GPT-4o slightly stronger on vuln detection |
| Changelog generation | 4 | 5 | 4 | Claude produces more natural changelogs |
| Instruction following | 5 | 5 | 4 | |
| Large diff handling | 3 | 4 | 3 | All struggle beyond ~4000 changed lines |

---

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Context window overflow | Large diffs (1000+ changed files) exceed LLM context | Chunk by file; summarize each file independently |
| Binary file noise | Binary diffs produce garbled output | Filter with `include_binary=false`; report as `[binary file changed]` |
| Hunk header misparse | Non-standard diff generators produce malformed headers | Validate with `unidiff`; fall back to line-by-line grep |
| Rename detection gap | Moves not detected as renames without `--find-renames` flag | Always run `git diff --find-renames` |
| Encoding issues | Files with mixed encodings produce parse errors | Force UTF-8 with `errors='replace'` |

---

## Prompt Patterns

### Pattern 1 — PR Summary
```
Read the following git diff and produce a concise pull request summary.
Include: what changed, why it likely changed, and any risks.

Diff:
{diff_text}
```

### Pattern 2 — Security Review
```
Analyze this git diff for security issues:
{diff_text}

Flag any:
- Hardcoded secrets or credentials
- SQL injection or XSS vulnerabilities introduced
- Insecure dependency additions
- Removed security checks or validation

Return as JSON: [{"file": "...", "line": N, "issue": "...", "severity": "high|medium|low"}]
```

### Pattern 3 — Changelog Entry
```
Given this git diff between {old_version} and {new_version}:
{diff_text}

Generate a changelog entry in Keep a Changelog format:
### Added
### Changed
### Fixed
### Removed
```

---

## Notes

- Always pass `--unified=0` to `git diff` when you only need changed lines without context; use `--unified=3` for code review tasks.
- For GitHub PRs, the REST API returns per-file diffs limited to 300 lines each — use pagination for large PRs.
- Diffs from binary files, submodules, and mode changes produce non-standard output — handle each case explicitly.
- Token cost: a 500-line diff ≈ 2,000–3,000 tokens; budget accordingly for multi-file reviews.

---

## Related Skills

- [Code Reading](./code-reading.md) — deeper semantic analysis of individual files
- [File System Reading](./file-system-reading.md) — enumerate changed files before diffing
- [API Response Parsing](./api-response-parsing.md) — GitHub/GitLab APIs return diff data as JSON

---

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-04` | v1 | Initial entry |
| `2026-07` | v2 | Added typed I/O tables, extended examples, full frameworks table, model comparison, prompt patterns, detailed failure modes |
