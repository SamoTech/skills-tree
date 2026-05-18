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

## Dependencies
- package: mistune
  tested_version: "3.1.3"
  confidence: verified
  notes: "Patched GHSA-58cw-g322-p94v, GHSA-8g87-j6q8-g93x, GHSA-8mp2-v27r-99xp, GHSA-v87v-83h2-53w7 (XSS via unsafe HTML renderer). Use mistune>=3.1.3."

## Failure Modes
- Non-standard frontmatter delimiters
- Nested code blocks with backtick collisions

## Related
- `document-parsing.md` · `text-reading.md`

## Changelog
- v1 (2026-04): Initial entry
- v1.1 (2026-05): Bump mistune to 3.1.3 (CVE patch)
