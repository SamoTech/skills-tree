**Category:** Security & Safety
**Skill Level:** Intermediate
**Stability:** stable
**Added:** 2025-03

### Description
Records all agent actions — tool calls, file writes, API requests, decisions — to a structured, append-only log. Enables post-hoc auditing, debugging, and compliance. Supports JSON Lines, OpenTelemetry, and syslog formats.

### Example
```python
import json, time, uuid
from pathlib import Path
from functools import wraps

LOG_FILE = Path("/var/log/agent/audit.jsonl")
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

def audit_log(action: str, details: dict, agent_id: str = "agent-001") -> None:
    entry = {
        "timestamp": time.time(),
        "event_id": str(uuid.uuid4()),
        "agent_id": agent_id,
        "action": action,
        **details,
    }
    with LOG_FILE.open("a") as f:
        f.write(json.dumps(entry) + "\n")

def audited(action_name: str):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            audit_log(f"{action_name}:start", {"args": str(args[:2])})
            try:
                result = func(*args, **kwargs)
                audit_log(f"{action_name}:success", {"result_type": type(result).__name__})
                return result
            except Exception as e:
                audit_log(f"{action_name}:error", {"error": str(e)})
                raise
        return wrapper
    return decorator

@audited("file_write")
def write_report(path: str, content: str) -> None:
    Path(path).write_text(content)
```

### Related Skills
- [Permission Checking](permission-checking.md)
- [Logging and Observability](../15-orchestration/logging-observability.md)
- [Rollback / Undo](rollback-undo.md)
