---
name: file-append
description: Append text or bytes to a file with explicit encoding, newline, locking, and error semantics.
metadata:
  source: skills/04-action-execution/file-append.md
  category: 04-action-execution
---

# File Append

## Description

Append content to an existing file without replacing prior content. Define encoding and newline behavior and consider locking when multiple processes can write concurrently.

## When to Use

- Appending audit records or logs.
- Adding generated entries to a text file.
- Updating append-only artifacts where replacement is not appropriate.

## Inputs / outputs / failure modes

| Input | Output | Failure mode |
|---|---|---|
| Path | Updated file | Permission error |
| Content | Appended bytes | Encoding error |
| Encoding/newline | Deterministic text | Format drift |
| Lock policy | Serialized write | Concurrent writers |

## Runnable example

```python
from pathlib import Path

def append_text(path, text, encoding="utf-8"):
    with Path(path).open("a", encoding=encoding, newline="") as handle:
        handle.write(text)
    return Path(path)

print(append_text("audit.log", "approved\n"))
```

## Failure modes

- Appending unbounded data without rotation.
- Concurrent writers interleaving records.
- Mixing incompatible encodings.
- Treating an append-only file as tamper-proof evidence.

## Related

- file-write.md
- ../01-perception/file-system-reading.md
- assertion.md

## Evidence

- AI_CONSTITUTION.md
- AGENTS.md
- Repository security and validation workflows
