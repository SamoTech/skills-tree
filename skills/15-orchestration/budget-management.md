**Category:** Orchestration
**Skill Level:** `advanced`
**Stability:** stable
**Added:** 2026-04

### Description
Tracks and enforces token, cost, time, and API-call budgets across a multi-agent workflow. Allocates quotas per sub-agent, triggers warnings at thresholds, and halts or degrades execution when limits are reached.

### Example
```python
from dataclasses import dataclass, field

@dataclass
class Budget:
    max_tokens: int
    max_cost_usd: float
    used_tokens: int = 0
    used_cost: float = 0.0

    def charge(self, tokens: int, cost_usd: float):
        self.used_tokens += tokens
        self.used_cost += cost_usd
        if self.used_tokens > self.max_tokens:
            raise RuntimeError(f"Token budget exceeded: {self.used_tokens}/{self.max_tokens}")
        if self.used_cost > self.max_cost_usd:
            raise RuntimeError(f"Cost budget exceeded: ${self.used_cost:.4f}")

    @property
    def remaining_tokens(self):
        return self.max_tokens - self.used_tokens

b = Budget(max_tokens=10000, max_cost_usd=0.50)
b.charge(4000, 0.12)
print(f"Remaining tokens: {b.remaining_tokens}")
```

### Related Skills
- [Rate Limiting](../14-security/rate-limiting.md)
- [Logging & Observability](logging-observability.md)
