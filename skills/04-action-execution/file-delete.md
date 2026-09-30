---
title: "File Delete"
category: 04-action-execution
level: intermediate
stability: stable
description: "Delete a verified filesystem target only after path validation, scope checks, and any required approval boundary."
added: "2026-09"
related: [file-write, file-system-reading, approval-before-destructive-tools]
---

# File Delete

## Description

Remove a filesystem entry only after resolving the intended path and confirming that the target is within the permitted scope. Destructive deletion must fail closed when path or authorization is ambiguous.

## When to Use

- Removing temporary artifacts.
- Deleting an explicitly identified file or directory.
- Cleaning generated output inside a controlled workspace.

## Inputs / outputs / failure modes

| Input | Output | Failure mode |
|---|---|---|
| Target path | Deletion result | Target missing |
| Allowed root | Scope validation | Path escape |
| Recursive flag | Controlled removal | Accidental directory deletion |
| Approval state | Allowed action | Unauthorized deletion |

## Runnable example

```python
from pathlib import Path

def delete_file(path, allowed_root):
    target = Path(path).resolve()
    root = Path(allowed_root).resolve()
    if target.parent != root:
        raise ValueError("target is outside the allowed root")
    target.unlink()
    return True

delete_file("workspace/output.txt", "workspace")
```

## Failure modes

- Deleting from an untrusted path string.
- Following a symlink outside the permitted workspace.
- Recursive deletion without explicit scope.
- Treating a missing target as proof of successful deletion.

## Related

- file-write.md
- ../01-perception/file-system-reading.md
- ../14-security/approval-before-destructive-tools.md

## Evidence

- AI_CONSTITUTION.md
- AGENTS.md
- Repository security and validation workflows
