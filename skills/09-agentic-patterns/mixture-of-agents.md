# Mixture of Agents (MoA)

**Category:** `agentic-patterns`
**Skill Level:** `advanced`
**Stability:** `experimental`

### Description

Multiple LLM agents independently generate responses; an aggregator model combines their outputs into a final, higher-quality answer. Exploits the diversity of different model families.

### Example

```
Query: "Explain quantum entanglement simply"

Agent 1 (GPT-4o):    "Imagine two coins always landing opposite..."
Agent 2 (Claude 3):  "Entanglement links particles so measuring one..."
Agent 3 (Gemini):    "Like a magic pair of dice that always match..."

Aggregator: synthesizes all three → best combined explanation
```

### Related Skills

- [Debate Pattern](debate-pattern.md)
- [Subagent Delegation](subagent-delegation.md)
- [Critic Agent](critic-agent.md)
