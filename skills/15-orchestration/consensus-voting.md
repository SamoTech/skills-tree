![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-15-orchestration-consensus-voting.json)

**Category:** Orchestration
**Skill Level:** Advanced
**Stability:** stable
**Added:** 2025-03

### Description
Collects independent responses from multiple agents on the same question and aggregates them via majority vote, weighted scoring, or LLM meta-evaluation. Improves reliability and reduces hallucination on factual or classification tasks.

### Example
```python
import anthropic
from collections import Counter

client = anthropic.Anthropic()

def agent_vote(question: str, temperature: float) -> str:
    """A single agent vote at a given temperature."""
    msg = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=16,
        temperature=temperature,
        messages=[{"role": "user", "content": f"{question} Answer with ONE word."}]
    )
    return msg.content[0].text.strip().lower()

def consensus_vote(question: str, n_agents: int = 5) -> str:
    """Run N agents and pick the majority answer."""
    temps = [0.0, 0.3, 0.5, 0.7, 1.0][:n_agents]
    votes = [agent_vote(question, t) for t in temps]
    print(f"Votes: {votes}")
    winner, count = Counter(votes).most_common(1)[0]
    return f"{winner} ({count}/{n_agents} votes)"

print(consensus_vote("Is Python interpreted or compiled?"))
```

### Related Skills
- [Mixture of Agents](../09-agentic-patterns/mixture-of-agents.md)
- [Debate Pattern](../09-agentic-patterns/debate-pattern.md)
- [Subagent Spawning](subagent-spawning.md)
