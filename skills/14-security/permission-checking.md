![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-14-security-permission-checking.json)

**Category:** Security
**Skill Level:** `advanced`
**Stability:** stable
**Added:** 2026-04

### Description
Enforces role-based or capability-based access control before executing any tool call or resource access. Evaluates the requesting agent's identity, granted scopes, and the target resource's required permissions.

### Example
```python
from functools import wraps
from typing import Callable

ACL = {
    "agent-admin": {"read", "write", "delete"},
    "agent-worker": {"read", "write"},
    "agent-readonly": {"read"},
}

def require_permission(action: str):
    def decorator(fn: Callable):
        @wraps(fn)
        def wrapper(agent_id: str, *args, **kwargs):
            perms = ACL.get(agent_id, set())
            if action not in perms:
                raise PermissionError(f"{agent_id} lacks '{action}' permission")
            return fn(agent_id, *args, **kwargs)
        return wrapper
    return decorator

@require_permission("delete")
def delete_record(agent_id: str, record_id: str):
    return f"Deleted {record_id}"

try:
    print(delete_record("agent-worker", "order-42"))
except PermissionError as e:
    print(e)
```

### Related Skills
- [Input Sanitization](input-sanitization.md)
- [Audit Logging](audit-logging.md)
- [Human In Loop](human-in-loop.md)
