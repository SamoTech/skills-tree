---
title: "Binary File Reading"
category: 01-perception
level: intermediate
stability: stable
description: "Enable AI agents to read binary file formats (images, archives, executables) and extract metadata, magic bytes, and embedded content for downstream processing."
added: "2025-03"
version: "v2"
last_updated: "2026-07"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-01-perception-binary-file-reading.json)

# Binary File Reading

**Category:** `01-perception`
**Skill Level:** `intermediate`
**Stability:** `stable`
**Version:** `v2`
**Added:** `2025-03`
**Last Updated:** `2026-07`

---

## Description

Binary File Reading enables an agent to inspect non-text files by detecting their format via magic bytes, extracting embedded metadata, and producing hex dumps or decoded payloads. It is essential for forensic analysis, media processing pipelines, and any workflow where files arrive in unknown or heterogeneous formats. Agents use this skill before routing files to format-specific processors.

---

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `path` | `string` | ✅ | Absolute or relative path to the binary file |
| `mode` | `string` | ✅ | `metadata` \| `hex_dump` \| `extract` — controls output depth |
| `max_bytes` | `int` | ❌ | Max bytes to read in hex_dump mode (default: 1024) |
| `recursive` | `bool` | ❌ | Recursively unpack nested archives (default: false) |

---

## Outputs

| Output | Type | Description |
|---|---|---|
| `mime_type` | `string` | Detected MIME type (e.g. `image/png`, `application/zip`) |
| `size_bytes` | `int` | File size in bytes |
| `metadata` | `dict` | Format-specific metadata (EXIF, PE headers, ZIP entries, etc.) |
| `hex_preview` | `string` | First N bytes as hex string (only in hex_dump mode) |
| `embedded_files` | `list[dict]` | Extracted sub-files when `mode=extract` |

---

## Example

```python
import magic
from PIL import Image
from PIL.ExifTags import TAGS

def read_binary(path: str, mode: str = "metadata") -> dict:
    mime = magic.from_file(path, mime=True)
    result = {"mime_type": mime, "size_bytes": __import__("os").path.getsize(path)}

    if mode == "metadata" and mime.startswith("image/"):
        img = Image.open(path)
        exif_raw = img._getexif() or {}
        result["metadata"] = {TAGS.get(k, k): v for k, v in exif_raw.items()}

    elif mode == "hex_dump":
        with open(path, "rb") as f:
            result["hex_preview"] = f.read(64).hex()

    return result

print(read_binary("photo.jpg"))
# → {"mime_type": "image/jpeg", "size_bytes": 204800, "metadata": {"Make": "Canon", ...}}
```

```python
# Extended — extract ZIP contents
import zipfile

def extract_zip(path: str) -> list[dict]:
    with zipfile.ZipFile(path) as zf:
        return [{"name": i.filename, "size": i.file_size, "compress_size": i.compress_size}
                for i in zf.infolist()]

print(extract_zip("archive.zip"))
```

---

## Frameworks & Models

| Framework / Model | Implementation | Since |
|---|---|---|
| Python `python-magic` | `magic.from_file(path, mime=True)` — libmagic bindings | v1 |
| Python `Pillow` | `Image.open()` + `_getexif()` for image metadata | v1 |
| Python `pefile` | PE header parsing for Windows executables | v1 |
| Python `zipfile` / `tarfile` | Standard library archive extraction | v1 |
| `binwalk` CLI | Firmware and embedded file extraction | v1 |
| LangChain `UnstructuredFileLoader` | Fallback loader for unknown binary formats | v0.1 |
| GPT-4o | Can interpret hex dumps and metadata dicts natively | 2024-05 |
| Claude 3.7 Sonnet | Strong at structured metadata interpretation | 2025-01 |

---

## Model Comparison

| Capability | GPT-4o | Claude 3.7 Sonnet | Gemini 2.0 Flash | Notes |
|---|---|---|---|---|
| Metadata interpretation | 4 | 5 | 3 | Claude excels at structured dict parsing |
| Hex dump analysis | 4 | 4 | 3 | Both GPT-4o and Claude handle this well |
| Format routing decisions | 5 | 4 | 4 | GPT-4o slightly better at format identification |
| Instruction following | 5 | 5 | 4 | |
| Edge case handling | 4 | 4 | 3 | Corrupted files trip all models |

---

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Wrong MIME detection | Corrupted or spoofed magic bytes | Cross-validate with file extension and content heuristics |
| EXIF read failure | Truncated or non-standard EXIF blocks | Wrap in try/except; fall back to basic stat info |
| Infinite recursion | Self-referencing or deeply nested archives | Set `max_depth` limit (default 3) |
| Memory overflow | Attempting to load large binary into memory | Stream in chunks; use `mmap` for files >100 MB |
| Permission error | File locked or restricted permissions | Check `os.access(path, os.R_OK)` before opening |

---

## Prompt Patterns

### Pattern 1 — Basic Metadata Request
```
Read the binary file at: {file_path}
Detect its MIME type and extract all available metadata.
Return a JSON object with keys: mime_type, size_bytes, metadata.
```

### Pattern 2 — Format Routing
```
Inspect the binary file: {file_path}
Based on its detected format, choose the appropriate extraction tool:
- image/* → extract EXIF
- application/zip → list archive contents
- application/x-executable → extract PE headers
Return: {format, tool_used, extracted_data}
```

### Pattern 3 — Hex Forensics
```
Perform a hex analysis on: {file_path}
Read the first {num_bytes} bytes as hex.
Identify the file signature (magic bytes) and report:
- Detected format
- Known header pattern match
- Any anomalies
```

---

## Notes

- `python-magic` requires `libmagic` system library (`apt install libmagic1` on Debian/Ubuntu).
- On Windows, use `python-magic-bin` instead of `python-magic`.
- EXIF data can contain sensitive GPS coordinates — sanitize before storing or logging.
- Files larger than 500 MB should be streamed, not loaded fully into memory.

---

## Related Skills

- [File System Reading](./file-system-reading.md) — enumerating and stat-ing files before binary inspection
- [Document Parsing](./document-parsing.md) — higher-level parsing once format is identified
- [Image Understanding](./image-understanding.md) — semantic analysis after binary extraction
- [OCR](./ocr.md) — text extraction from image-type binary files

---

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-04` | v1 | Initial entry |
| `2026-07` | v2 | Added typed I/O tables, extended examples, frameworks table, model comparison, prompt patterns, detailed failure modes |
