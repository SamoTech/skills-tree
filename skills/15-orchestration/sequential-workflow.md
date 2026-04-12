**Category:** Orchestration
**Skill Level:** `advanced`
**Stability:** stable
**Added:** 2026-04

### Description
Orchestrates a deterministic pipeline of agent steps where each step receives the output of the previous one as input. Manages state passing, step validation, error propagation, and result accumulation.

### Example
```python
from typing import Any, Callable

Step = tuple[str, Callable[[dict], dict]]

def run_pipeline(initial_state: dict, steps: list[Step]) -> dict:
    state = initial_state.copy()
    for step_name, fn in steps:
        print(f"Running step: {step_name}")
        result = fn(state)
        state.update(result)
        state["__last_step"] = step_name
    return state

pipeline = [
    ("fetch",    lambda s: {"raw": f"data for {s['query']}"}),
    ("parse",    lambda s: {"parsed": s["raw"].upper()}),
    ("summarise",lambda s: {"summary": s["parsed"][:20] + "..."}),
]

result = run_pipeline({"query": "AI agents"}, pipeline)
print(result["summary"])
```

### Related Skills
- [Conditional Branching](conditional-branching.md)
- [Retry Backoff](retry-backoff.md)
- [Logging & Observability](logging-observability.md)
