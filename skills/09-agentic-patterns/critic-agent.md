![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-09-agentic-patterns-critic-agent.json)

# Critic Agent

**Category:** `agentic-patterns`
**Skill Level:** `advanced`
**Stability:** `stable`
**Added:** 2025-03

### Description

A dedicated secondary agent (or LLM call) that evaluates the primary agent's output against defined criteria and returns structured feedback for revision.

### Example

```python
critic_prompt = """
You are a code reviewer. Evaluate the following function:
{code}

Rate on: correctness (1-5), readability (1-5), edge-case handling (1-5).
Return JSON: {"scores": {...}, "feedback": "..."}
"""
feedback = llm.invoke(critic_prompt.format(code=generated_code))
```

### Related Skills

- [Reflection](reflection.md)
- [Constitutional AI](constitutional-ai.md)
- [Debate Pattern](debate-pattern.md)
