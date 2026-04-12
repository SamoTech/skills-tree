# Debate Pattern

**Category:** `agentic-patterns`
**Skill Level:** `advanced`
**Stability:** `experimental`
**Added:** 2025-03

### Description

Two or more agents argue for opposing positions on a question. A judge agent (or majority vote) evaluates the arguments and selects the most convincing conclusion.

### Example

```
Question: "Is microservices architecture always better than monoliths?"

Agent A (Pro-microservices):  "Scalability, independent deployments..."
Agent B (Pro-monolith):       "Lower complexity for small teams..."
Agent A rebuttal: "..."
Agent B rebuttal: "..."

Judge: Agent B's argument is more nuanced for the given context.
Verdict: "Monolith preferred for early-stage startups."
```

### Related Skills

- [Mixture of Agents](mixture-of-agents.md)
- [Critic Agent](critic-agent.md)
- [Constitutional AI](constitutional-ai.md)
