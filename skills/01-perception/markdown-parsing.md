---
title: "Markdown Parsing"
category: 01-perception
level: intermediate
stability: stable
version: v2
added: "2025-03"
updated: "2026-09"
description: "Parse Markdown deterministically into bounded structural records such as headings, fenced code blocks, links, and frontmatter without executing embedded content."
related:
  - document-parsing
  - text-reading
  - structured-data-reading
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-01-perception-markdown-parsing.json)

# Markdown Parsing
Category: perception | Level: intermediate | Stability: stable | Version: v2

## Description
Markdown parsing converts a Markdown document into a representation an agent can inspect without treating document content as executable instructions. The safe baseline is structural extraction: headings, fenced code blocks, links, frontmatter, and source locations. Rendering to HTML is a separate transformation and should use an explicitly configured renderer with raw HTML handling understood.

This skill is intentionally bounded. It does not execute code blocks, follow links, fetch remote resources, evaluate embedded HTML, or infer that Markdown text is trustworthy merely because it parsed successfully.

## When to Use
- Extract document structure before summarization or indexing.
- Identify headings and code examples while preserving their source order.
- Collect links for a later, separately authorized retrieval step.
- Read YAML-like frontmatter when the caller explicitly requests it.

Do not use this parser as a security sanitizer, HTML renderer, or arbitrary document execution engine.

## Inputs
- `text`: UTF-8 Markdown source.
- `max_bytes`: optional byte ceiling for bounded processing; default `1_000_000`.
- `extract`: optional set containing `headings`, `code_blocks`, `links`, and `frontmatter`.

## Outputs
A deterministic dictionary containing only requested fields. Each extracted item preserves source order and includes enough location information to trace it back to the original text. Unparseable frontmatter is reported as an error rather than silently discarded.

## Output Contract
| Field | Type | Contract |
|---|---|---|
| `headings` | list | `level`, `text`, and zero-based `line` for ATX headings |
| `code_blocks` | list | `language`, `text`, `start_line`, and `end_line` |
| `links` | list | `text`, `target`, and zero-based `line` |
| `frontmatter` | object/string | Raw YAML-frontmatter body; parsing is optional and must be explicit |
| `errors` | list | Stable error codes for bounded or malformed input |

## Deterministic Reference Implementation
The following implementation uses only the Python standard library. It extracts common Markdown structures and deliberately leaves Markdown semantics that require a full parser out of scope.

```python
from __future__ import annotations

import re

LINK_RE = re.compile(r"\[([^\]]*)\]\(([^)\s]+)(?:\s+[^)]*)?\)")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*#*\s*$")


def parse_markdown(text: str, max_bytes: int = 1_000_000) -> dict:
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    if len(text.encode("utf-8")) > max_bytes:
        return {"headings": [], "code_blocks": [], "links": [], "errors": ["input_too_large"]}

    lines = text.splitlines()
    headings, code_blocks, links, errors = [], [], [], []
    in_fence = False
    fence_marker = ""
    fence_lang = ""
    fence_start = 0
    fence_lines = []

    for number, line in enumerate(lines):
        if line.startswith(("```", "~~~")):
            marker = line[:3]
            if not in_fence:
                in_fence = True
                fence_marker = marker
                fence_lang = line[3:].strip().split()[0] if line[3:].strip() else ""
                fence_start = number
                fence_lines = []
            elif marker == fence_marker:
                code_blocks.append({
                    "language": fence_lang,
                    "text": "\n".join(fence_lines),
                    "start_line": fence_start,
                    "end_line": number,
                })
                in_fence = False
            else:
                fence_lines.append(line)
            continue

        if in_fence:
            fence_lines.append(line)
            continue

        match = HEADING_RE.match(line)
        if match:
            headings.append({"level": len(match.group(1)), "text": match.group(2), "line": number})

        for link in LINK_RE.finditer(line):
            links.append({"text": link.group(1), "target": link.group(2), "line": number})

    if in_fence:
        errors.append("unterminated_code_fence")

    return {
        "headings": headings,
        "code_blocks": code_blocks,
        "links": links,
        "errors": errors,
    }
```

## Validation Rules
1. Reject non-string input before parsing.
2. Apply the byte limit before processing lines.
3. Preserve source order for every extracted structure.
4. Never execute fenced code, HTML, URLs, or frontmatter values.
5. Report an unterminated fenced block instead of silently treating its contents as ordinary prose.
6. Treat extracted URLs as data; retrieval requires a separate authorization boundary.
7. A successful parse means only that the selected structural extraction completed; it does not establish document trustworthiness.

## Failure Modes
| Failure | Detection | Safe behavior |
|---|---|---|
| Oversized document | UTF-8 byte count exceeds limit | Return `input_too_large` without partial claims |
| Unterminated fence | Fence remains open at EOF | Preserve no synthetic closing fence; return explicit error |
| Complex Markdown extension | Syntax outside the reference parser | Preserve source text and use a dedicated parser when required |
| Malformed frontmatter | Explicit frontmatter parse fails | Return parse error; do not guess metadata |
| Embedded HTML/script | Raw HTML appears in source | Treat it as untrusted text; never execute it |
| Link target is remote | URL scheme/target is extracted | Return the target only; do not fetch it |

## Security Boundaries
Markdown is untrusted input. Parsing must not execute fenced code, JavaScript, shell commands, template expressions, or embedded HTML. If the downstream system renders Markdown as HTML, it must apply a separate rendering and sanitization policy. Link extraction must never imply network permission.

## Frameworks
| Framework | Method | Use when |
|---|---|---|
| Python standard library | bounded structural parser | deterministic extraction is sufficient |
| `mistune` | AST/rendering | full Markdown grammar is required and dependency is approved |
| `markdown-it-py` | token/AST parsing | CommonMark-style parsing is required |
| LlamaIndex | `MarkdownReader` | document ingestion is already managed by the framework |
| LangChain | `UnstructuredMarkdownLoader` | broader document-loader integration is required |

## Dependencies
The reference implementation has no third-party runtime dependency. Third-party Markdown parsers may be appropriate when full grammar support is required, but their versions and security posture must be verified by the consuming project rather than asserted by this skill.

## Related Skills
- `document-parsing.md` — broader document extraction and normalization.
- `text-reading.md` — bounded text ingestion and encoding handling.
- `structured-data-reading.md` — structured formats that require schema-aware interpretation.

## Provenance
The parser returns source line locations for extracted structures so downstream processing can retain traceability to the original Markdown. It does not assign semantic authority or authorship to document content.

## Changelog
- v1 (2026-04): Initial entry.
- v1.1 (2026-05): Documented third-party parser dependency and security boundary.
- v2 (2026-09): Added bounded deterministic reference implementation, explicit contracts, validation rules, failure modes, provenance, and security boundaries.
