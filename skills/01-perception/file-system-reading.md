---
title: "File System Reading"
category: 01-perception
level: basic
stability: stable
description: "Apply file system reading in AI agent workflows."
added: "2025-03"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-01-perception-file-system-reading.json)

# File System Reading

**Category:** `perception`  
**Skill Level:** `basic`  
**Stability:** `stable`  
**Added:** 2025-03  
**Last Updated:** 2026-04

---

## Description

Traverse, list, filter, and read files from a local or remote file system. Includes directory tree enumeration, glob pattern matching, metadata extraction (size, timestamps, permissions), and selective content reading for large codebases or data directories. Agents use this skill to build inventories, locate relevant files, and ingest content into their context.

---

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `root` | `string` | ✅ | Root directory path |
| `pattern` | `string` | ❌ | Glob pattern, e.g. `**/*.py` (default: `**/*`) |
| `max_files` | `int` | ❌ | Cap on files returned (default: 50) |
| `include_content` | `bool` | ❌ | Read file contents for small files (default: true) |

---

## Outputs

| Output | Type | Description |
|---|---|---|
| `tree` | `list` | `[{path, size, preview}]` |
| `summary` | `string` | Natural-language description of the directory |
| `total_files` | `int` | Count of matched files |

---

## Example

```python
import anthropic
from pathlib import Path

client = anthropic.Anthropic()

def summarize_directory(root: str, pattern: str = "**/*.py") -> str:
    """Build a directory inventory and summarize the codebase purpose."""
    root_path = Path(root)
    files = list(root_path.glob(pattern))

    inventory = []
    for f in files[:50]:  # cap at 50 files
        rel = f.relative_to(root_path)
        size = f.stat().st_size
        preview = ""
        if size < 4096:
            try:
                preview = f.read_text(encoding="utf-8")[:300]
            except Exception:
                preview = "<binary or unreadable>"
        inventory.append(f"### {rel} ({size} bytes)\n{preview}")

    tree_text = "\n".join(inventory)

    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1024,
        messages=[{
            "role": "user",
            "content": (
                f"File inventory of `{root}`:\n\n"
                f"{tree_text}\n\n"
                "Summarize: What does this project do? What are the main modules?"
            )
        }]
    )
    return response.content[0].text

print(summarize_directory("./my_project"))
```

---

## Frameworks & Models

| Framework / Model | Implementation | Since |
|---|---|---|
| Claude claude-opus-4-5 | Direct text prompt with inventory | 2024-06 |
| LangChain | `DirectoryLoader` | v0.1 |
| LangGraph | Tool node using `pathlib` | v0.1 |

---

## Notes

- Use `pathlib.Path.glob()` for cross-platform recursive matching
- Always cap the number of files to avoid context overflow
- For remote filesystems, use SFTP or cloud SDK to list/read before passing to the model
- Binary files should be skipped or handled separately

---

## Related Skills

- [Document Parsing](document-parsing.md) — extracting content from specific file types
- [Code Reading](code-reading.md) — deeper analysis of source files
- [Structured Data Reading](structured-data-reading.md) — parsing config/data files

---

## Changelog

| Date | Change |
|---|---|
| `2026-04` | Expanded from stub: full description, I/O table, directory summarizer example |
| `2025-03` | Initial stub entry |
