---
title: "Binary File Reading"
category: 01-perception
level: intermediate
stability: stable
description: "Apply binary file reading in AI agent workflows."
added: "2025-03"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-01-perception-binary-file-reading.json)

# Binary File Reading
Category: perception | Level: advanced | Stability: stable | Version: v1

## Description
Read binary file formats (images, archives, executables) to extract metadata, magic bytes, and embedded content.

## Inputs
- `path`: file path
- `mode`: `metadata` | `extract` | `hex_dump`

## Outputs
- File type, size, embedded strings, metadata

## Example
```python
import magic
from PIL import Image
fpath = "unknown.bin"
ftype = magic.from_file(fpath, mime=True)
print(f"Detected: {ftype}")
if ftype.startswith("image/"):
    img = Image.open(fpath)
    print(img.size, img.format, img._getexif())
```

## Frameworks
| Framework | Method |
|---|---|
| Python | `python-magic`, `Pillow`, `pefile` |
| CLI | `file`, `binwalk`, `strings` |

## Failure Modes
- Corrupted magic bytes cause misidentification
- Nested archives require recursive extraction

## Related
- `file-system-reading.md` · `document-parsing.md`

## Changelog
- v1 (2026-04): Initial entry
