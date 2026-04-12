**Category:** Orchestration
**Skill Level:** Intermediate
**Stability:** stable
**Added:** 2025-03

### Description
Executes a chain of agent steps in strict order where each step receives the output of the previous one. Implements pipeline composition with typed I/O contracts, error propagation, and optional checkpointing for long-running sequences.

### Example
```python
from dataclasses import dataclass
from typing import Any, Callable

@dataclass
class PipelineStep:
    name: str
    fn: Callable[[Any], Any]

class SequentialPipeline:
    def __init__(self, steps: list[PipelineStep]):
        self.steps = steps

    def run(self, initial_input: Any) -> Any:
        state = initial_input
        for step in self.steps:
            print(f"[{step.name}] Running...")
            state = step.fn(state)
            print(f"[{step.name}] Done.")
        return state

# Define steps
def fetch_data(url: str) -> dict:
    return {"url": url, "rows": 500}  # simulated

def clean_data(raw: dict) -> dict:
    return {**raw, "cleaned": True}

def analyse(clean: dict) -> dict:
    return {**clean, "summary": "Analysis complete"}

pipeline = SequentialPipeline([
    PipelineStep("Fetch",   lambda x: fetch_data(x)),
    PipelineStep("Clean",   clean_data),
    PipelineStep("Analyse", analyse),
])

result = pipeline.run("https://api.example.com/data")
print(result)
```

### Related Skills
- [Parallel Task Execution](parallel-execution.md)
- [Conditional Branching](conditional-branching.md)
- [Retry with Backoff](retry-backoff.md)
