# Multi-Agent Mesh Blueprint

**Category:** blueprints | **Stability:** stable | **Version:** v1

## What This Solves

Some tasks are too broad for a single agent. A multi-agent mesh assigns N specialist agents to parallel sub-tasks, collects results, and merges them through an orchestrator — reducing latency and improving quality through specialization.

**Use when:**
- A task can be decomposed into independent parallel sub-problems
- Different sub-tasks benefit from different system prompts / tool access
- You need cross-validation (agents checking each other)

---

## Architecture

```
                    ┌───────────────┐
         Goal       │  Orchestrator  │
       ──────────►  │  Decomposes &  │
                    │  Routes Tasks  │
                    └─────┬────────┘
                         │
           ┌──────────┼──────────┐
           │          │           │
           ▼          ▼           ▼
    ┌────────┐  ┌────────┐  ┌────────┐
    │ Agent A │  │ Agent B │  │ Agent C │
    │Specialist│  │Specialist│  │Specialist│
    └────────┘  └────────┘  └────────┘
           │          │           │
           └─────────┴──────────┘
                    │
           ┌───────┴───────┐
           │   Result Merger  │
           │  Conflict Resolve│
           └───────────────┘
                    │
                  Output
```

---

## Full Implementation

```python
import anthropic
import asyncio
import json
from dataclasses import dataclass
from typing import Callable

client = anthropic.Anthropic()

@dataclass
class Agent:
    name: str
    system_prompt: str
    tools: list = None

ORCHESTRATOR_SYSTEM = """
You are a task orchestrator. Given a complex goal, decompose it into N independent
sub-tasks that can run in parallel. Output JSON:
{
  "tasks": [
    {"agent": "agent_name", "task": "specific task description"},
    ...
  ],
  "merge_strategy": "concat|vote|synthesize"
}
"""

MERGER_SYSTEM = """
You receive outputs from N specialist agents. Merge them into a single coherent
response. Resolve conflicts by preferring the more specific/evidence-based answer.
"""

DEFAULT_AGENTS = [
    Agent("researcher", "You are a research specialist. Find facts, cite sources."),
    Agent("analyst", "You are a data analyst. Identify patterns and insights."),
    Agent("writer", "You are a technical writer. Structure and clarify information."),
]

def orchestrate(goal: str, agents: list[Agent]) -> dict:
    """Decompose goal into per-agent tasks."""
    agent_names = [a.name for a in agents]
    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1024,
        system=ORCHESTRATOR_SYSTEM,
        messages=[{
            "role": "user",
            "content": f"Goal: {goal}\nAvailable agents: {agent_names}"
        }]
    )
    return json.loads(response.content[0].text)

def run_agent(agent: Agent, task: str) -> str:
    """Run a single specialist agent on its task."""
    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=2048,
        system=agent.system_prompt,
        messages=[{"role": "user", "content": task}]
    )
    return response.content[0].text

def merge_results(goal: str, results: list[dict]) -> str:
    """Merge all agent outputs into a final answer."""
    results_text = "\n\n".join([f"**{r['agent']}**:\n{r['output']}" for r in results])
    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=4096,
        system=MERGER_SYSTEM,
        messages=[{
            "role": "user",
            "content": f"Original goal: {goal}\n\nAgent outputs:\n{results_text}"
        }]
    )
    return response.content[0].text

def run_mesh(goal: str, agents: list[Agent] = None) -> str:
    """Full multi-agent mesh pipeline."""
    agents = agents or DEFAULT_AGENTS
    agent_map = {a.name: a for a in agents}

    # 1. Orchestrate
    plan = orchestrate(goal, agents)
    print(f"Plan: {plan['tasks']}")

    # 2. Run in parallel (using threads for simplicity)
    import concurrent.futures
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(agents)) as executor:
        futures = {
            executor.submit(run_agent, agent_map[t["agent"]], t["task"]): t["agent"]
            for t in plan["tasks"]
            if t["agent"] in agent_map
        }
        for future, agent_name in futures.items():
            output = future.result()
            results.append({"agent": agent_name, "output": output})
            print(f"[{agent_name}] done")

    # 3. Merge
    return merge_results(goal, results)

# Usage
if __name__ == "__main__":
    answer = run_mesh("Write a comprehensive analysis of LLM agent memory architectures")
    print(answer)
```

---

## Variants

| Variant | When to Use |
|---|---|
| **Parallel mesh** (above) | Independent sub-tasks, maximize speed |
| **Sequential chain** | Each agent depends on the previous output |
| **Debate mesh** | Two agents argue opposing views, third adjudicates |
| **Voting mesh** | N agents answer same question, majority wins |

```python
# Debate variant
def debate_mesh(question: str) -> str:
    pro = run_agent(Agent("pro", "Argue strongly FOR the position."), question)
    con = run_agent(Agent("con", "Argue strongly AGAINST the position."), question)
    judge = run_agent(Agent("judge", "Evaluate both sides and give a balanced verdict."),
                     f"FOR:\n{pro}\n\nAGAINST:\n{con}\n\nQuestion: {question}")
    return judge
```

---

## Failure Modes

| Failure | Mitigation |
|---|---|
| Agent produces incompatible output format | Give each agent an output schema in system prompt |
| Orchestrator assigns task to wrong specialist | Include agent capabilities in the orchestration prompt |
| Merger invents info not in agent outputs | Instruct merger to only synthesize, never invent |
| One agent is slow and blocks everything | Set per-agent timeout, use partial results if one fails |

---

## Related

- `blueprints/multi-agent-workflow.md` — Linear orchestration variant
- `systems/research-agent.md` — Research agent using a simplified mesh
- `skills/15-orchestration/multi-agent.md` · `skills/15-orchestration/consensus.md`

## Changelog

- **v1** (2026-04) — Initial blueprint: parallel mesh, debate variant, merger
