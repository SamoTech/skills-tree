**Category:** Security & Safety
**Skill Level:** Intermediate
**Stability:** stable
**Added:** 2025-03

### Description
Verifies that an agent has explicit authorisation before executing sensitive operations (file writes, API calls, database mutations). Implements a declarative permission model with scope-based access control and deny-by-default behaviour.

### Example
```python
from dataclasses import dataclass, field
from typing import Set

@dataclass
class AgentPermissions:
    allowed_scopes: Set[str] = field(default_factory=set)

    def check(self, scope: str) -> None:
        if scope not in self.allowed_scopes:
            raise PermissionError(
                f"Agent attempted '{scope}' without permission. "
                f"Granted scopes: {self.allowed_scopes}"
            )

def send_email(to: str, body: str, perms: AgentPermissions) -> None:
    perms.check("email:send")
    print(f"Email sent to {to}: {body[:40]}...")

def read_file(path: str, perms: AgentPermissions) -> str:
    perms.check("filesystem:read")
    with open(path) as f:
        return f.read()

# Grant only read access — email will be blocked
agent_perms = AgentPermissions(allowed_scopes={"filesystem:read"})
read_file("/tmp/data.txt", agent_perms)        # OK
send_email("a@b.com", "Hello", agent_perms)    # PermissionError
```

### Related Skills
- [Audit Logging](audit-logging.md)
- [Human-in-the-Loop Escalation](human-in-loop.md)
- [Sandboxed Execution](sandboxed-execution.md)
