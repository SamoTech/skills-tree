---
title: "File Write"
category: 04-action-execution
level: basic
stability: stable
description: "Atomically write text or bytes to a file on disk — with directory creation, encoding control, and crash-safe rename semantics."
added: "2025-03"
version: v3
tags: [filesystem, io, atomic, action]
updated: "2026-04"
code_blocks:
  - id: "example-atomic-write"
    type: executable
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-04-action-execution-file-write.json)

# File Write

## Description

Writes content to a file on the local filesystem. The naive one-liner (`open(p, "w").write(x)`) is fine for scratch scripts, but agents that write configs, caches, or user data **need atomic writes** — a partial write must never overwrite the previous good file. This skill is the safe version every action-executing agent should standardize on.

## When to Use

- Any agent that mutates files a user (or another process) reads concurrently.
- Writing JSON / YAML state that must never be observed half-written.
- Producing artifacts (reports, logs) you want to deliver atomically.

## Inputs / Outputs

| Field | Type | Description |
|---|---|---|
| `path` | `str \| Path` | Destination file path |
| `content` | `str \| bytes` | Payload |
| `encoding` | `str` | Default `utf-8` (ignored for bytes) |
| `mode` | `Literal["overwrite","exclusive","append"]` | Write semantics |
| `make_parents` | `bool` | Create missing directories |
| → `path` | `Path` | Final path written |
| → `bytes_written` | `int` | Length of payload |

## Runnable Example

```python
# Standard library only.
from __future__ import annotations
import json
import os
import tempfile
from pathlib import Path

def write_file(
    path: str | Path,
    content: str | bytes,
    *,
    encoding: str = "utf-8",
    mode: str = "overwrite",      # overwrite | exclusive | append
    make_parents: bool = True,
) -> dict:
    p = Path(path)
    if make_parents:
        p.parent.mkdir(parents=True, exist_ok=True)

    is_bytes = isinstance(content, bytes)
    payload: bytes = content if is_bytes else content.encode(encoding)

    if mode == "exclusive" and p.exists():
        raise FileExistsError(p)

    if mode == "append":
        with open(p, "ab") as f:
            f.write(payload)
        return {"path": p, "bytes_written": len(payload)}

    # Atomic overwrite via temp file in the same directory + os.replace.
    # os.replace is POSIX `rename(2)` and Windows `MoveFileEx`-with-replace,
    # both atomic on the same filesystem.
    fd, tmp = tempfile.mkstemp(prefix=p.name + ".", dir=p.parent)
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(payload)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, p)
    except BaseException:
        try: os.unlink(tmp)
        except FileNotFoundError: pass
        raise
    return {"path": p, "bytes_written": len(payload)}

if __name__ == "__main__":
    state = {"version": 2, "skills": 359}
    info = write_file("./out/state.json", json.dumps(state, indent=2))
    print(info)  # {'path': PosixPath('out/state.json'), 'bytes_written': 32}
```

## Failure Modes

| Failure | Cause | Mitigation |
|---|---|---|
| Half-written file readable by another process | Naive `open(..., "w")` truncates first | Use the atomic temp+`os.replace` pattern above |
| `os.replace` fails across mount points | Temp file on different filesystem | Always create the temp file in the same parent directory |
| Lost data after crash | Buffer not flushed to disk | `f.flush() + os.fsync(fileno)` before rename |
| Permission denied late | Process lacks write on target dir | Check `os.access(parent, os.W_OK)` before generating content |
| Encoding mismatch on Windows | Default cp1252 codec | Always pass `encoding="utf-8"` explicitly |
| Race with another writer | Two agents overwrite each other | Add an advisory lock (`fcntl.flock` / `portalocker`) when concurrency exists |

## Frameworks & Models

| Helper | Provides |
|---|---|
| `pathlib.Path.write_text` | One-shot, NOT atomic |
| `atomic-write` (PyPI) | The pattern above as a lib |
| `filelock` | Cross-process locking |

## Related Skills

- [File Append](file-append.md)
- [File Delete](file-delete.md)
- [Shell Command Execution](shell-command.md)
- [File Read](../01-perception/file-reading.md)

## Changelog

| Date | Version | Change |
|---|---|---|
| 2025-03 | v1 | Initial entry |
| 2026-04 | v3 | Atomic write pattern, failure modes, exclusive/append modes |
