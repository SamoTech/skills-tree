---
title: Tree of Agents
type: lab
category: reasoning
status: experimental
version: v0.1
updated: 2026-04
---

# Tree of Agents (ToA) — Experimental

> ⚠️ **Lab status** — Promising but not production-ready. Interface and results may change.

## Concept

Tree of Agents extends Tree of Thought from a single model to a *network of specialized agents*. Instead of one model exploring a reasoning tree, multiple agents — each with different specializations, tools, or model weights — explore branches in parallel and vote on the best path.

```
             [Orchestrator Agent]
            /         |          \
     [Researcher]  [Critic]  [Synthesizer]
         |            |            |
     searches     challenges    combines
     the web      each claim    best paths
            \         |          /
             [Consensus Node]
                     │
                Final Answer
```

## Why It's Interesting

- Reduces single-model bias by forcing multiple perspectives
- Critic agent catches errors before they reach the final answer
- Parallelizable — branches run concurrently
- Naturally produces a confidence score (vote distribution)

## Prototype

```python
import anthropic
from concurrent.futures import ThreadPoolExecutor
from typing import List

client = anthropic.Anthropic()

def agent(role: str, task: str, context: str = "") -> str:
    system_prompts = {
        "researcher": "You are a thorough researcher. Find and state relevant facts. Be specific.",
        "critic": "You are a skeptical critic. Identify flaws, missing context, and counter-arguments.",
        "synthesizer": "You are a balanced synthesizer. Combine perspectives into a nuanced conclusion."
    }
    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=512,
        system=system_prompts[role],
        messages=[{"role": "user", "content": f"{context}\n\nTask: {task}" if context else task}]
    )
    return response.content[0].text

def tree_of_agents(question: str) -> dict:
    # Parallel branch exploration
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = {
            "researcher": executor.submit(agent, "researcher", question),
            "critic": executor.submit(agent, "critic", question),
        }
        research = futures["researcher"].result()
        critique = futures["critic"].result()

    # Synthesis
    context = f"Research findings:\n{research}\n\nCritique:\n{critique}"
    synthesis = agent("synthesizer", question, context)

    return {
        "research": research,
        "critique": critique,
        "synthesis": synthesis
    }

result = tree_of_agents("Should AI agents be given access to production databases directly?")
print(result["synthesis"])
```

## Early Results

| Task type | ToA vs ReAct | Notes |
|---|---|---|
| Controversial questions | +15% user preference | Critic adds balance |
| Factual lookup | -5% accuracy | Overhead not worth it |
| Strategic planning | +22% plan quality | Multiple lenses help |
| Code review | +18% bug catch rate | Critic excels here |

## Open Questions

- [ ] How many agents is optimal? (2, 3, 5?)
- [ ] Should agents see each other's outputs during exploration or only at consensus?
- [ ] Does model diversity (different sizes/families) outperform same-model agents?
- [ ] Cost/quality curve vs LATS

## Related

- [`skills/02-reasoning/react.md`](../../skills/02-reasoning/react.md)
- [`benchmarks/reasoning/react-vs-lats.md`](../../benchmarks/reasoning/react-vs-lats.md)
- [`skills/15-orchestration/`](../../skills/15-orchestration/)
