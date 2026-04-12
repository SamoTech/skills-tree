**Category:** Orchestration
**Skill Level:** Intermediate
**Stability:** stable
**Added:** 2025-03

### Description
Tracks token consumption, API costs, and time budgets across an agent run. Raises warnings when approaching limits and gracefully terminates or truncates tasks that would exceed the budget, returning partial results where possible.

### Example
```python
import anthropic
from dataclasses import dataclass

client = anthropic.Anthropic()

@dataclass
class Budget:
    max_tokens: int
    max_cost_usd: float
    used_tokens: int = 0
    used_cost_usd: float = 0.0

    COST_PER_1K_INPUT  = 0.000015  # claude-opus-4-5 input
    COST_PER_1K_OUTPUT = 0.000075  # claude-opus-4-5 output

    def charge(self, input_tokens: int, output_tokens: int) -> None:
        cost = (input_tokens / 1000 * self.COST_PER_1K_INPUT +
                output_tokens / 1000 * self.COST_PER_1K_OUTPUT)
        self.used_tokens  += input_tokens + output_tokens
        self.used_cost_usd += cost

    def check(self) -> None:
        if self.used_tokens > self.max_tokens:
            raise RuntimeError(f"Token budget exceeded: {self.used_tokens}/{self.max_tokens}")
        if self.used_cost_usd > self.max_cost_usd:
            raise RuntimeError(f"Cost budget exceeded: ${self.used_cost_usd:.4f}/${self.max_cost_usd}")

bud = Budget(max_tokens=50_000, max_cost_usd=0.50)

for step in ["research", "write", "review"]:
    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=512,
        messages=[{"role": "user", "content": f"Do the {step} step for a blog post on AI agents."}]
    )
    bud.charge(response.usage.input_tokens, response.usage.output_tokens)
    bud.check()
    print(f"[{step}] Tokens used so far: {bud.used_tokens} | Cost: ${bud.used_cost_usd:.4f}")
```

### Related Skills
- [Logging and Observability](logging-observability.md)
- [Task Queue Management](task-queue.md)
- [Retry with Backoff](retry-backoff.md)
