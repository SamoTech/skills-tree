---
title: "Text Reading"
category: 01-perception
level: basic
stability: stable
description: "Read and pre-process plain text inputs for AI agent consumption."
added: "2025-03"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-01-perception-text-reading.json)

# Text Reading
Category: perception | Level: basic | Stability: stable | Version: v1

## Description
Load, chunk, and normalize plain text documents or strings for downstream agent tasks. Handles encoding detection, whitespace normalization, and optional splitting via LangChain text splitters.

## Inputs
- `source`: file path, URL, or raw string
- `chunk_size`: optional int (tokens or characters per chunk)
- `overlap`: optional int (overlap between consecutive chunks)

## Outputs
- List of text chunks as strings

## Example
```python
from langchain_text_splitters import RecursiveCharacterTextSplitter
def read_and_chunk(text, chunk_size=1000, overlap=100):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=overlap
    )
    return splitter.split_text(text)
```

## Frameworks
| Framework | Method |
|---|---|
| LangChain | `RecursiveCharacterTextSplitter`, `CharacterTextSplitter` |
| LlamaIndex | `SentenceSplitter`, `TokenTextSplitter` |
| Python | `tiktoken` for token-aware splitting |

## Dependencies
- package: langchain-text-splitters
  tested_version: "0.3.8"
  confidence: verified
  notes: "Patched GHSA-fv5p-p927-qmxr (prompt injection via malicious document content). Use langchain-text-splitters>=0.3.8."

## Failure Modes
- Binary or non-UTF-8 files cause decode errors — use `errors='replace'`
- Very large files should be streamed, not loaded into memory at once

## Related
- `document-parsing.md` · `markdown-parsing.md` · `structured-data-reading.md`

## Changelog
- v1 (2026-02): Initial entry
- v1.1 (2026-05): Bump langchain-text-splitters to 0.3.8 (CVE patch)
