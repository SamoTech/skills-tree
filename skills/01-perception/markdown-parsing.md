---
title: "Markdown Parsing"
category: 01-perception
level: intermediate
stability: stable
description: "Apply markdown parsing in AI agent workflows."
added: "2025-03"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-01-perception-markdown-parsing.json)

# Markdown Parsing
Category: perception | Level: basic | Stability: stable | Version: v1

## Description
Parse Markdown documents into structured AST or HTML, extracting headings, code blocks, links, and metadata.

## Inputs
- `text`: raw Markdown string
- `extract`: list of element types to return

## Outputs
- Structured dict with sections, code blocks, links, frontmatter

## Example
```python
import mistune, yaml
def parse_md(text):
    if text.startswith("---"):
        _, fm, body = text.split("---", 2)
        meta = yaml.safe_load(fm)
    else:
        meta, body = {}, text
    md = mistune.create_markdown(renderer=mistune.AstRenderer())
    return {"meta": meta, "ast": md(body)}
```

## Frameworks
| Framework | Method |
|---|---|
| Python | `mistune`, `markdown-it-py` |
| LlamaIndex | `MarkdownReader` |
| LangChain | `UnstructuredMarkdownLoader` |

## Failure Modes
- Non-standard frontmatter delimiters
- Nested code blocks with backtick collisions

## Related
- `document-parsing.md` · `text-reading.md`

## Changelog
- v1 (2026-04): Initial entry
