---
title: "Text Reading"
category: 01-perception
level: basic
stability: stable
description: "Read bounded plain-text inputs, normalize encoding and whitespace, and split content deterministically for downstream agent processing without conflating parsing with retrieval or generation."
added: "2025-03"
version: v2
related: [document-parsing, markdown-parsing, structured-data-reading]
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-01-perception-text-reading.json)

# Text Reading
Category: perception | Level: basic | Stability: stable | Version: v2

## Description
Text reading converts a bounded byte or string source into normalized text chunks.
It is a deterministic preprocessing step, not an embedding, retrieval, summarization, or generation step.
The implementation below uses only the Python standard library so its behavior is reproducible.

## Inputs / Outputs
| Input | Type | Contract |
|---|---|---|
| `source` | `str | bytes` | Raw text or UTF-8-compatible bytes; bounded before processing |
| `chunk_size` | `int` | Positive character limit per chunk |
| `overlap` | `int` | `0 <= overlap < chunk_size` |
| `normalize_whitespace` | `bool` | Collapse runs of whitespace when enabled |

| Output | Type | Contract |
|---|---|---|
| `chunks` | `list[str]` | Ordered, non-empty chunks whose lengths respect the requested bound |

## Deterministic Reference Implementation
```python
import re


def read_text(source, chunk_size=1000, overlap=100, normalize_whitespace=True):
    if chunk_size <= 0 or overlap < 0 or overlap >= chunk_size:
        raise ValueError("require chunk_size > 0 and 0 <= overlap < chunk_size")
    if isinstance(source, bytes):
        text = source.decode("utf-8", errors="strict")
    elif isinstance(source, str):
        text = source
    else:
        raise TypeError("source must be str or bytes")
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    if normalize_whitespace:
        text = re.sub(r"[ \t]+", " ", text)
        text = re.sub(r"\n{3,}", "\n\n", text).strip()
    if not text:
        return []
    step = chunk_size - overlap
    return [text[i:i + chunk_size] for i in range(0, len(text), step)]

chunks = read_text("alpha   beta\n\ngamma", chunk_size=10, overlap=2)
assert chunks
assert all(len(chunk) <= 10 for chunk in chunks)
```

## Frameworks
| Framework | Role | Boundary |
|---|---|---|
| Python standard library | Deterministic normalization and chunking | Recommended reference behavior |
| LangChain | `RecursiveCharacterTextSplitter` | Optional downstream splitting; verify installed version separately |
| LlamaIndex | `SentenceSplitter` / `TokenTextSplitter` | Optional downstream splitting; token counts are model-specific |

## Failure Modes
| Cause | Observable result | Mitigation |
|---|---|---|
| Invalid UTF-8 bytes | `UnicodeDecodeError` | Choose an explicit encoding or reject the source |
| Oversized source | Excessive memory use | Enforce a byte/character limit before loading |
| Invalid overlap | `ValueError` | Require `0 <= overlap < chunk_size` |
| Binary content | Nonsensical text | Detect file type upstream and route to binary parsing |
| Whitespace loss | Formatting-sensitive content changes | Disable normalization for code or layout-sensitive text |

## Security Boundaries
Treat document text as untrusted data. Reading must not execute embedded markup, macros, shell commands, or model instructions.
Do not fetch URLs, follow links, or resolve external resources in this skill.
If downstream code sends the text to an LLM, apply prompt-injection defenses separately.

## Validation Rules
- The source type must be `str` or `bytes`.
- Chunk size must be positive and overlap must be smaller than chunk size.
- The reference implementation performs no network I/O.
- The output order is stable for identical inputs and parameters.
- Empty or whitespace-only input returns an empty list.

## Provenance
The reference implementation is intentionally standard-library-only and does not assert framework compatibility beyond the documented method names.
Framework package versions are not pinned here because the core contract does not require them.

## Related
- `document-parsing.md` — broader document extraction
- `markdown-parsing.md` — Markdown-specific structure
- `structured-data-reading.md` — structured records rather than free text

## Changelog
- v1 (2026-02): Initial entry
- v1.1 (2026-05): Dependency note updated for langchain-text-splitters
- v2 (2026-09-20): Added deterministic reference behavior, typed contracts, validation, security boundaries, and failure-mode coverage
