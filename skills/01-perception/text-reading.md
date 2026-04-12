# Text Reading

**Category:** `perception`  
**Skill Level:** `basic`  
**Stability:** `stable`  
**Added:** 2025-03  
**Version:** v2

---

## Description

Read, chunk, and pre-process raw text inputs for downstream tasks. Covers encoding detection, normalisation, sentence boundary detection, and token-aware chunking — the foundation for every text-based agent pipeline.

---

## Core Operations

| Operation | Tool | Notes |
|---|---|---|
| Encoding detection | `chardet` / `charset-normalizer` | Always detect before decode |
| Normalisation | `unicodedata.normalize('NFC', text)` | Collapse composed/decomposed chars |
| Sentence splitting | `nltk.sent_tokenize` / `spacy` | Language-aware |
| Token counting | `tiktoken` | Match target model's tokenizer |
| Chunking | LangChain `RecursiveCharacterTextSplitter` | Respects sentence boundaries |
| Language detection | `langdetect` / `lingua` | Route multilingual text |

---

## Implementation

### Encoding-safe read

```python
import chardet

def safe_read(path: str) -> str:
    raw = open(path, "rb").read()
    enc = chardet.detect(raw)["encoding"] or "utf-8"
    return raw.decode(enc, errors="replace")
```

### Token-aware chunking

```python
from langchain_text_splitters import RecursiveCharacterTextSplitter
import tiktoken

def chunk_text(text: str, model: str = "gpt-4o",
               chunk_tokens: int = 512, overlap: int = 64) -> list[str]:
    enc = tiktoken.encoding_for_model(model)
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_tokens,
        chunk_overlap=overlap,
        length_function=lambda t: len(enc.encode(t)),
        separators=["\n\n", "\n", ". ", " ", ""]
    )
    return splitter.split_text(text)
```

### Normalisation pipeline

```python
import unicodedata, re

def normalize(text: str) -> str:
    text = unicodedata.normalize("NFC", text)   # Unicode normalise
    text = re.sub(r"\r\n|\r", "\n", text)       # Unify line endings
    text = re.sub(r"[ \t]+", " ", text)          # Collapse whitespace
    text = re.sub(r"\n{3,}", "\n\n", text)      # Max 2 blank lines
    return text.strip()
```

---

## Chunking Strategy Guide

| Use Case | Strategy | Chunk Size |
|---|---|---|
| RAG retrieval | Recursive character | 256–512 tokens, 10% overlap |
| Summarisation | Sentence-level | 1000–2000 tokens, 0 overlap |
| Code files | By function/class | Variable, keep function intact |
| Tabular data | By row batches | 50–200 rows |

---

## Related Skills

- [Document Parsing](document-parsing.md)
- [PDF Parsing](pdf-parsing.md)
- [Structured Data Reading](structured-data-reading.md)
