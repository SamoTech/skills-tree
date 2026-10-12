---
name: archive-extraction
description: Extract files from zip, tar, and compressed archives safely, with path-traversal defense, decompression-bomb limits, and integrity verification before any extracted byte is used.
metadata:
  source: skills/04-action-execution/archive-extraction.md
  category: 04-action-execution
  version: "v1"
---

# Archive Extraction

Category: Action Execution | Level: basic | Stability: experimental | Version: v1

## Description

Extracting an archive means executing a promise made by untrusted bytes: a manifest of names, sizes, and attributes that the extractor must not believe. This skill covers detecting the real format, bounding the total decompressed size, rejecting traversal paths, and extracting into a staging area so nothing extracted is used before validation completes.

## When to Use

Use when ingesting bundles, backups, datasets, or dependency archives into a working environment.

Do not extract untrusted archives into privileged paths, and do not treat extension names as format evidence.

## Inputs

| Input | Type | Required | Description |
|---|---|---|---|
| `archive_path` | `path` | Yes | The archive file on disk |
| `destination` | `path` | Yes | Staging directory for extraction |
| `max_total_size` | `int` | No | Decompression-bomb ceiling (default 1 GiB) |

## Procedure

1. Detect the format from magic bytes (PK\x03\x04, ustar, gzip, xz), never from the file extension.
2. Read the entry manifest; reject the archive if declared total size exceeds the ceiling.
3. Validate every entry name: reject absolute paths, `..` segments, and non-materializable entries such as device nodes.
4. Verify checksums when the archive provides them (CRC, or sidecar signature files).
5. Extract into the staging directory with permissions normalized; do not execute or import anything during extraction.
6. Move validated files into the destination only after every entry passed.

## Outputs

| Output | Type | Description |
|---|---|---|
| `extracted_files` | `list` | Validated paths now in the destination |
| `skipped_entries` | `list` | Rejected entries with reasons |
| `integrity_report` | `object` | Format, counts, sizes, checksum results |

## Runnable Example

```python
def safe_entry_name(name):
    parts = [p for p in name.split("/") if p not in ("", ".", "..")]
    return "/".join(parts) if parts and not name.startswith("/") else None

def check_manifest(entries, max_total_size=1073741824):
    total = 0
    for entry in entries:
        if safe_entry_name(entry["name"]) is None:
            return {"ok": False, "reason": "traversal", "entry": entry["name"]}
        total += entry.get("size", 0)
        if total > max_total_size:
            return {"ok": False, "reason": "bomb", "entry": entry["name"]}
    return {"ok": True, "total": total}

manifest = [{"name": "data/a.csv", "size": 100}, {"name": "../evil.sh", "size": 5}]
print(check_manifest(manifest))
```

## Failure Modes

| Failure Mode | Cause | Mitigation |
|---|---|---|
| Zip bomb | Compressed ratio and total size unchecked | Enforce `max_total_size` on declared sizes |
| Path traversal | Entry names contain `..` or absolute paths | Validate every entry name before writing |
| Extension spoofing | A gzip stream named `.zip` fed to the wrong parser | Detect format from magic bytes |
| Partial success | Extraction stopped mid-archive but reported done | Extract to staging; report skipped entries |
| Overwritten files | Destination already contained same-named files | Stage first, then move with explicit overwrite policy |

## Security and Authority Boundary

Archives are untrusted input with code-execution risk: entries can be executable or symlinks pointing outside the staging tree. Extract with least privilege, never auto-run extracted code, and treat any archive from an unknown source as hostile until validated.

## Evidence

This skill is grounded in dated public implementation references:

1. The patool portable archive utility (https://pypi.org/project/patool/).
2. The Python standard library tarfile documentation, including its extraction-safety notes (https://docs.python.org/3/library/tarfile.html).

Honest boundary: these are implementation references, not adoption or demand evidence; this entry was added under the owner-directed corpus expansion recorded in `meta/memory/DECISIONS.md`, and no demand signal is claimed for it.

## Related Skills

- [Shell Command](shell-command.md) — the execution layer that performs the extraction steps.
- [Batch Processing](batch-processing.md) — the pattern for handling many extracted entries uniformly.

## Changelog

| Date | Version | Change |
|---|---|---|
| `2026-10` | v1 | Initial entry added under the owner-directed corpus expansion |
