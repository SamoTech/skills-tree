---
title: Self-Healing Agent
category: blueprints
version: v1
stability: stable
---

# Self-Healing Agent

> Agent architecture with built-in error detection, exponential-backoff retry, action rollback, and automatic replanning — so transient failures never stop a long-running task.

## When to Use

- Long-running autonomous agents (30+ steps) where manual intervention is impractical
- Pipelines hitting rate-limited or flaky external APIs
- Tasks where partial completion is worse than full rollback

## Architecture

```
  Agent executes action
           │
    ┌──────┴──────┐
  success         error
    │               │
  next step    Error Classifier
               │         │
           transient   fatal
               │         │
         Retry w/     Rollback
         backoff    last checkpoint
               │         │
           success   Re-planner
               │         │
             next step  new plan
                   │
            Checkpoint saved
```

## Implementation

```python
import anthropic
import time
import copy
from typing import Callable, Any

client = anthropic.Anthropic()

ERROR_CLASSIFIER_SYSTEM = """
Classify this error as transient or fatal.
Transient: network timeout, rate limit (429), lock contention, service unavailable (503).
Fatal: auth failure (401/403), invalid input, resource not found (404), schema mismatch.
Output JSON: {"type": "transient|fatal", "retry_after_s": 0, "reason": "..."}
"""

REPLANNER_SYSTEM = """
A step in the agent plan failed fatally. Given the original plan and the failure,
produce a revised plan that avoids the failed step or substitutes an alternative approach.
Output JSON: {"revised_steps": ["step1", "step2", ...]}
"""

def classify_error(error: str) -> dict:
    import json
    resp = client.messages.create(
        model="claude-opus-4-5", max_tokens=256, system=ERROR_CLASSIFIER_SYSTEM,
        messages=[{"role": "user", "content": f"Error: {error}"}]
    )
    return json.loads(resp.content[0].text)

def replan(original_plan: list, failed_step: str, error: str) -> list:
    import json
    resp = client.messages.create(
        model="claude-opus-4-5", max_tokens=512, system=REPLANNER_SYSTEM,
        messages=[{"role": "user", "content": (
            f"Plan: {original_plan}\nFailed step: {failed_step}\nError: {error}"
        )}]
    )
    return json.loads(resp.content[0].text)["revised_steps"]

def execute_with_healing(steps: list, executor: Callable, max_retries: int = 4) -> list:
    checkpoints = []
    plan = list(steps)
    results = []

    for i, step in enumerate(plan):
        last_checkpoint = copy.deepcopy(results)
        for attempt in range(max_retries):
            try:
                result = executor(step)
                results.append({"step": step, "result": result, "attempt": attempt + 1})
                checkpoints.append(copy.deepcopy(results))
                break
            except Exception as e:
                err_str = str(e)
                classification = classify_error(err_str)

                if classification["type"] == "fatal":
                    # Roll back to last checkpoint, replan remaining
                    results = last_checkpoint
                    remaining = plan[i:]
                    new_steps = replan(remaining, step, err_str)
                    plan = plan[:i] + new_steps
                    break  # restart with new plan

                # Transient: exponential backoff
                wait = classification.get("retry_after_s", 0) or (2 ** attempt)
                time.sleep(min(wait, 60))
        else:
            raise RuntimeError(f"Step '{step}' failed after {max_retries} attempts")

    return results
```

## Retry Policy

| Attempt | Wait |
|---|---|
| 1 | 2s |
| 2 | 4s |
| 3 | 8s |
| 4 | 16s (or `retry_after_s` from error classifier) |

## Failure Modes

| Failure | Fix |
|---|---|
| Replan loop (keeps failing) | Max replan attempts (3); escalate to human after |
| Rollback loses important side effects | Use saga pattern: track compensating actions per step |
| Error classifier wrong | Add explicit status-code checks before LLM classification |

## Related

- `blueprints/human-in-the-loop.md`
- `skills/02-reasoning/self-correction.md`
- `skills/15-orchestration/retry.md`

## Changelog

- `v1` (2026-04) — Initial with exponential backoff, error classification, checkpoint rollback, replanning
