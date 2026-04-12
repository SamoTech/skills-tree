# Constitutional AI

**Category:** `agentic-patterns`
**Skill Level:** `advanced`
**Stability:** `stable`

### Description

Agent revises its own output by checking it against a set of principles (a "constitution"). For each principle, the agent critiques and rewrites the output until all principles are satisfied.

### Example

```
Initial response: [potentially harmful advice]

Principle 1: "Do not provide instructions that could harm people."
Critique: "My response could be misused to harm others."
Revision: [safer, helpful alternative]

Principle 2: "Be honest and acknowledge uncertainty."
Critique: "I stated this as fact without citing sources."
Revision: [adds uncertainty qualifier]

Final response: [safe, honest, helpful]
```

### Related Skills

- [Reflection](reflection.md)
- [Critic Agent](critic-agent.md)
- [Debate Pattern](debate-pattern.md)
