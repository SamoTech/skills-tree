---
title: "Metadata Extraction"
category: 01-perception
level: basic
stability: experimental
description: "Extract embedded metadata — EXIF, document properties, media tags — with provenance, field allowlisting, and sensitive-field redaction before any downstream use."
added: "2026-10"
version: v1
related: ["document-parsing", "pdf-parsing"]
---

# Metadata Extraction

Category: Perception | Level: basic | Stability: experimental | Version: v1

## Description

Metadata is data about data that travels inside the file — camera and location details in images, author and revision history in documents, encoding parameters in media. This skill extracts it as a typed, provenance-carrying record and treats it as sensitive by default: redact or allowlist fields rather than passing everything through.

## When to Use

Use when a workflow needs document properties, image EXIF, or media tags for routing, deduplication, or compliance — and when files leave their origin and embedded metadata must be reviewed before release.

Do not dump all metadata into logs or model context; embedded fields often contain names, coordinates, and hardware identifiers.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `file` | `path` | Yes | The file to inspect |
| `kinds` | `list` | No | Metadata kinds to extract: exif, document, media |
| `allowlist` | `list` | No | Specific fields to return; default is a minimal safe set |

## Procedure

1. Identify the file type before choosing an extractor; the container format determines which metadata blocks exist.
2. Extract only the requested metadata kinds rather than every block the format offers.
3. Apply the allowlist and redact sensitive fields — GPS coordinates, author identity, device serials — before returning values.
4. Record provenance for each field: which block, which tool, and the file digest at extraction time.
5. Report unreadable or truncated metadata blocks as findings rather than as empty metadata.
6. Keep the original file unmodified; extraction is a read-only operation.

## Outputs

| Output | Type | Description |
|---|---|---|
| `metadata` | `map` | Allowlisted fields with their values |
| `provenance` | `map` | Per-field block and tool provenance |
| `findings` | `list` | Unreadable blocks and redacted field names |

## Runnable Example

```python
def allowlist_metadata(raw, allowed):
    kept, redacted = {}, []
    for key, value in raw.items():
        if key in allowed:
            kept[key] = value
        else:
            redacted.append(key)
    return {"metadata": kept, "redacted": sorted(redacted)}

exif = {"DateTime": "2026:09:01 12:00:00", "GPSLatitude": 30.05, "Model": "TestCam-4"}
print(allowlist_metadata(exif, allowed={"DateTime", "Model"}))
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Metadata leakage | Location or identity fields reach logs or models | Allowlist and redact before use |
| Format mismatch | An extractor is applied to the wrong container type | Identify the file type before extracting |
| Truncated blocks | Damaged metadata is parsed as empty | Report unreadable blocks as findings |
| Encoding surprises | Dates and charset-prefixed strings are misread | Normalize with the declared encoding |
| Stale extraction | Fields are cited against a modified file | Record the file digest at extraction time |

## Security and Authority Boundary

Embedded metadata is personal data in most contexts — author names, locations, and device identifiers. Extraction results are sensitive by default; only allowlisted fields leave this skill, and redaction must be reported rather than silent.

## Evidence

This skill is grounded in dated public implementation references:

1. The ExifTool metadata reference (https://exiftool.org/).
2. The Pillow imaging library documentation (https://pillow.readthedocs.io/).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Document Parsing](document-parsing.md) — the content-extraction layer that works alongside embedded properties.
- [PDF Parsing](pdf-parsing.md) — the document format whose metadata blocks this skill reads.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
