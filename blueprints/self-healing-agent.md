# Self-Healing Agent Blueprint

**Category:** blueprints | **Stability:** stable | **Version:** v1

## What This Solves

Production agents fail. APIs time out, tools return unexpected formats, partial actions leave state inconsistent. This blueprint adds structured error detection, exponential-backoff retry, state rollback, and graceful degradation — so agents recover automatically from the majority of transient failures.

**Use when:**
- Agent runs unsupervised (cron, webhook-triggered)
- Actions have side effects that must be idempotent
- Failure rate > 5% on any single tool

---

## Architecture

```
  Agent Action
       │
       ▼
  ┌──────────────┐
  │ Try Action   │
  └─────┬────────┘
          │
   ┌─────┴─────┐
   │           │
 Success     Failure
   │           │
 Continue    Error Classifier
              │
     ┌───────┴───────┐
     │               │
  Transient        Permanent
  (retry)          (rollback)
     │               │
  Backoff         Restore state
  + Retry         + Alert human
```

---

## Full Implementation

```python
import anthropic
import time
import json
from typing import Callable, Optional, TypeVar
from dataclasses import dataclass, field
from copy import deepcopy

client = anthropic.Anthropic()
T = TypeVar("T")

@dataclass
class AgentState:
    """Snapshot of agent state — must be serializable."""
    step: int
    data: dict
    completed_actions: list[str] = field(default_factory=list)

ERROR_CLASSIFIER_SYSTEM = """
Classify this error and decide the recovery strategy. Output JSON:
{
  "error_type": "transient|permanent|unknown",
  "cause": "brief explanation",
  "strategy": "retry|rollback|skip|alert",
  "retry_delay_seconds": int,
  "max_retries": int
}

Transient: network timeouts, rate limits, 5xx errors, lock contention
Permanent: auth errors, invalid input, resource not found, schema mismatch
"""

def classify_error(error: Exception, context: dict) -> dict:
    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=256,
        system=ERROR_CLASSIFIER_SYSTEM,
        messages=[{"role": "user", "content": f"Error: {str(error)}\nContext: {json.dumps(context)}"}]
    )
    return json.loads(response.content[0].text)

def with_retry(
    fn: Callable[[], T],
    context: dict,
    max_retries: int = 3,
    base_delay: float = 1.0,
) -> T:
    """Execute fn with exponential backoff on transient errors."""
    last_error = None
    for attempt in range(max_retries + 1):
        try:
            return fn()
        except Exception as e:
            last_error = e
            if attempt == max_retries:
                break

            classification = classify_error(e, context)

            if classification["error_type"] == "permanent":
                raise  # Don't retry permanent errors

            delay = base_delay * (2 ** attempt)  # exponential backoff
            delay = min(delay, classification.get("retry_delay_seconds", delay))
            print(f"[Retry {attempt+1}/{max_retries}] {classification['cause']} — waiting {delay:.1f}s")
            time.sleep(delay)

    raise last_error

class SelfHealingAgent:
    def __init__(self):
        self.state = AgentState(step=0, data={})
        self._checkpoints: list[AgentState] = []

    def checkpoint(self):
        """Save current state snapshot."""
        self._checkpoints.append(deepcopy(self.state))

    def rollback(self, steps: int = 1):
        """Restore to N checkpoints ago."""
        if len(self._checkpoints) >= steps:
            self.state = self._checkpoints[-steps]
            print(f"[Rollback] Restored to step {self.state.step}")
        else:
            print("[Rollback] No checkpoint available, resetting to initial state")
            self.state = AgentState(step=0, data={})

    def run_action(self, name: str, action_fn: Callable, max_retries: int = 3):
        """Run an action with checkpoint, retry, and rollback on failure."""
        self.checkpoint()
        context = {"action": name, "step": self.state.step}

        try:
            result = with_retry(action_fn, context, max_retries)
            self.state.completed_actions.append(name)
            self.state.step += 1
            return result
        except Exception as e:
            classification = classify_error(e, context)
            print(f"[FAIL] Action '{name}' failed permanently: {e}")
            print(f"[STRATEGY] {classification['strategy']}")

            if classification["strategy"] == "rollback":
                self.rollback()
            elif classification["strategy"] == "skip":
                print(f"[SKIP] Continuing without '{name}'")
            elif classification["strategy"] == "alert":
                self._alert_human(name, e, classification)
                raise

    def _alert_human(self, action: str, error: Exception, classification: dict):
        print(f"\n🚨 HUMAN ALERT: Action '{action}' requires intervention")
        print(f"   Error: {error}")
        print(f"   Classification: {classification}")

# Usage
if __name__ == "__main__":
    agent = SelfHealingAgent()
    call_count = 0

    def flaky_api_call():
        global call_count
        call_count += 1
        if call_count < 3:
            raise ConnectionError("Upstream timeout")
        return {"data": "success"}

    result = agent.run_action("fetch_data", flaky_api_call, max_retries=3)
    print(f"Final result: {result}")
    print(f"Completed actions: {agent.state.completed_actions}")
```

---

## Idempotency Pattern

```python
# Always check if action was already completed before executing
def idempotent_action(action_id: str, fn: Callable, completed_log: set) -> any:
    if action_id in completed_log:
        print(f"[SKIP] {action_id} already completed")
        return None
    result = fn()
    completed_log.add(action_id)
    return result
```

---

## Failure Modes

| Failure | Mitigation |
|---|---|
| Rollback makes things worse | Only rollback read state, never un-send messages |
| Infinite retry loop | Hard cap at 5 retries with circuit breaker |
| Checkpoint consumes too much memory | Keep only last 3 checkpoints |
| Error classifier hallucination | Add explicit error code allowlist for transient |

---

## Related

- `blueprints/human-in-the-loop.md` — Escalate when self-healing is exhausted
- `skills/15-orchestration/retry.md` · `skills/02-reasoning/self-correction.md`

## Changelog

- **v1** (2026-04) — Initial blueprint: error classification, retry, checkpoint, rollback
