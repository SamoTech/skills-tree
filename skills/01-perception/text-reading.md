---
title: "Text Reading"
category: 01-perception
level: basic
stability: stable
description: "Read bounded plain-text inputs, normalize encoding and whitespace, and produce deterministic chunks for downstream agent processing without silently changing source meaning."
added: "2025-03"
version: v2
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-01-perception-text-reading.json)

# Text Reading
Category: perception | Level: basic | Stability: stable | Version: v2

## Description
Text reading is the deterministic ingestion layer for plain-text content. It converts a file, byte sequence, or already-decoded string into normalized text and, when requested, bounded chunks.

The skill must preserve source meaning. It should not summarize, infer missing content, rewrite punctuation, or silently discard malformed input. Normalization is limited to explicitly requested transformations such as newline and surrounding-whitespace normalization.

Use a bounded reader for agent pipelines so an unexpectedly large file cannot consume unbounded memory or context. For untrusted content, treat the text as data rather than instructions; prompt-injection defense belongs to the downstream policy layer.

## Inputs
- `source`: UTF-8 text, bytes, or a local file path.
- `chunk_size`: optional positive integer measured in characters when chunking is enabled.
- `overlap`: optional non-negative integer smaller than `chunk_size`.
- `max_bytes`: optional positive limit applied before decoding a file or byte input.
- `normalize_newlines`: optional boolean; default `True`.
- `strip_trailing_whitespace`: optional boolean; default `False`.

## Outputs
- `text`: decoded and explicitly normalized text.
- `chunks`: ordered list of bounded strings when chunking is requested.
- `truncated`: boolean indicating whether the input exceeded `max_bytes`.
- `encoding`: encoding used for decoding; this implementation accepts UTF-8 only.

## Deterministic reference implementation
```python
from pathlib import Path


def read_text(source, *, max_bytes=1_000_000, normalize_newlines=True,
              strip_trailing_whitespace=False, chunk_size=None, overlap=0):
    if max_bytes <= 0:
        raise ValueError("max_bytes must be positive")
    if isinstance(source, Path):
        raw = source.read_bytes()
    elif isinstance(source, bytes):
        raw = source
    elif isinstance(source, str):
        raw = source.encode("utf-8")
    else:
        raise TypeError("source must be str, bytes, or pathlib.Path")

    truncated = len(raw) > max_bytes
    raw = raw[:max_bytes]
    text = raw.decode("utf-8")
    if normalize_newlines:
        text = text.replace("\\r\\n", "\\n").replace("\\r", "\\n")
    if strip_trailing_whitespace:
        text = "\\n".join(line.rstrip() for line in text.split("\\n"))

    if chunk_size is None:
        return {"text": text, "chunks": [text], "truncated": truncated, "encoding": "utf-8"}
    if chunk_size <= 0 or overlap < 0 or overlap >= chunk_size:
        raise ValueError("require chunk_size > 0 and 0 <= overlap < chunk_size")

    step = chunk_size - overlap
    chunks = [text[i:i + chunk_size] for i in range(0, len(text), step)]
    return {"text": text, "chunks": chunks, "truncated": truncated, "encoding": "utf-8"}


result = read_text("alpha\r\nbeta", chunk_size=5, overlap=1)
assert result["text"] == "alpha\nbeta"
assert result["chunks"]
```

## Contract
| Input condition | Required behavior | Output invariant |
|---|---|---|
| Valid UTF-8 text | Decode without semantic rewriting | Returned text is deterministic |
| CRLF or CR newlines | Normalize only when enabled | Newline policy is explicit |
| Input over `max_bytes` | Truncate before decode and report it | `truncated=True` |
| Invalid UTF-8 | Fail closed | No guessed replacement text |
| Invalid chunk parameters | Reject | `ValueError` |
| Untrusted text | Preserve as data | No instruction execution |

## Chunking rules
Use character-based chunking when deterministic portability matters more than tokenizer fidelity. Keep `overlap < chunk_size` to guarantee forward progress. Token-aware splitters may be substituted only when the tokenizer and package versions are part of the execution contract.

For very large sources, stream or range-read upstream instead of loading the complete file into memory. A caller that needs byte-perfect archival behavior should retain the original bytes separately; this skill is an ingestion representation, not an archival store.

## Failure Modes
| Failure | Detection | Mitigation |
|---|---|---|
| Invalid UTF-8 | `UnicodeDecodeError` | Reject or invoke a separately specified encoding detector |
| Excessive input | `truncated=True` | Increase the explicit bound or stream the source |
| Zero/negative chunk size | Parameter validation | Correct the caller contract |
| Overlap >= chunk size | Parameter validation | Reduce overlap |
| Binary content | Decode failure or control-byte inspection | Route to binary-file-reading |
| Prompt injection in content | Content contains instructions | Preserve as data and apply downstream trust policy |

## Security boundaries
Never execute text as code, shell commands, templates, or agent instructions merely because it was read successfully. Restrict file access at the caller boundary and avoid following paths supplied by untrusted content. The skill does not perform URL fetching; remote retrieval requires a separate web/network skill with its own policy controls.

## Frameworks
| Framework | Method |
|---|---|
| Python standard library | `pathlib`, UTF-8 decoding, bounded reads |
| LangChain | `RecursiveCharacterTextSplitter` when tokenizer-aware chunking is explicitly required |
| LlamaIndex | `SentenceSplitter` or `TokenTextSplitter` with a pinned execution environment |

## Dependencies
- package: langchain-text-splitters
  tested_version: "0.3.8"
  confidence: verified
  notes: "Optional only; the reference implementation uses the Python standard library."

## Related
- `binary-file-reading.md`
- `document-parsing.md`
- `markdown-parsing.md`
- `structured-data-reading.md`

## Changelog
- v1 (2026-02): Initial entry
- v1.1 (2026-05): Bump langchain-text-splitters to 0.3.8
- v2 (2026-09): Added bounded deterministic reference implementation, explicit contract, security boundaries, and failure-mode table.
