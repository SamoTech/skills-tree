---
title: Multi-Agent Mesh
category: blueprints
version: v1
stability: stable
---

# Multi-Agent Mesh

> N specialist agents coordinated by a central orchestrator. Each specialist owns a domain; the orchestrator decomposes tasks, routes sub-tasks, aggregates results, and resolves conflicts.

## When to Use

- Task requires parallel expertise (research + code + legal review simultaneously)
- Individual subtasks exceed a single agent’s context window
- You need fault isolation: one specialist failure shouldn’t kill the whole pipeline

## Architecture

```
         User Request
               │
               ▼
      ┌───────────────┐
      │  Orchestrator  │
      │  (task planner)│
      └─────┬────┬────┘
           │     │      │
     ▼─────┘  ▼       ▼
Specialist A  Specialist B  Specialist C
(Research)   (Code Gen)   (Risk Review)
     │             │           │
     └───────────┴─────────┘
                   │
          Result Aggregator
          (merge + resolve)
                   │
               Final answer
```

## Full Implementation

```python
import anthropic
from concurrent.futures import ThreadPoolExecutor, as_completed

client = anthropic.Anthropic()

SPECIALISTS = {
    "research": "You are a research specialist. Given a sub-task, return a concise factual brief.",
    "code":     "You are a code specialist. Given a sub-task, return working, runnable Python.",
    "risk":     "You are a risk/legal specialist. Identify risks and compliance issues.",
}

ORCHESTRATOR_SYSTEM = """
You decompose tasks. Given a task, output JSON:
{"subtasks": [{"agent": "research|code|risk", "task": "..."}]}
Only JSON, no prose.
"""

AGGREGATOR_SYSTEM = """
You merge specialist outputs into a single coherent response.
Resolve any conflicts by preferring the risk specialist on safety questions.
"""

def call_specialist(agent: str, task: str) -> dict:
    resp = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1024,
        system=SPECIALISTS[agent],
        messages=[{"role": "user", "content": task}]
    )
    return {"agent": agent, "task": task, "result": resp.content[0].text}

def run_mesh(user_task: str) -> str:
    # 1. Orchestrator decomposes
    orch_resp = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=512,
        system=ORCHESTRATOR_SYSTEM,
        messages=[{"role": "user", "content": user_task}]
    )
    import json
    subtasks = json.loads(orch_resp.content[0].text)["subtasks"]

    # 2. Run specialists in parallel
    results = []
    with ThreadPoolExecutor(max_workers=len(subtasks)) as pool:
        futures = {pool.submit(call_specialist, s["agent"], s["task"]): s for s in subtasks}
        for future in as_completed(futures):
            results.append(future.result())

    # 3. Aggregate
    context = "\n\n".join(f"[{r['agent'].upper()}]\n{r['result']}" for r in results)
    agg_resp = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=2048,
        system=AGGREGATOR_SYSTEM,
        messages=[{"role": "user", "content": f"Task: {user_task}\n\nSpecialist outputs:\n{context}"}]
    )
    return agg_resp.content[0].text
```

## Configuration Tips

| Setting | Recommendation |
|---|---|
| Max specialists | 5–7 (beyond that, aggregation degrades) |
| Specialist model | Can use faster/cheaper model per specialist; orchestrator uses most capable |
| Timeout per specialist | 30s; on timeout mark as `{"result": "TIMEOUT"}` and continue |
| Conflict resolution | Risk > Research > Code in safety decisions |

## Failure Modes

| Failure | Fix |
|---|---|
| Orchestrator over-decomposes | Cap subtasks at 7; merge small tasks |
| Specialists contradict each other | Explicit conflict resolution prompt in aggregator |
| One specialist hangs | ThreadPoolExecutor timeout + partial aggregation |

## Related

- `blueprints/multi-agent-workflow.md`
- `systems/research-agent.md`
- `skills/15-orchestration/`

## Changelog

- `v1` (2026-04) — Initial mesh with parallel specialists and conflict-resolving aggregator
