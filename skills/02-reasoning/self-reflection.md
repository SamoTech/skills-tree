# Self-Reflection

**Category:** `reasoning`  
**Skill Level:** `intermediate`  
**Stability:** `stable`
**Added:** 2025-03

### Description

Evaluate and critique the agent's own outputs before finalizing them, checking for errors, gaps, or improvements.

### Example

```python
prompt = f"""
You produced the following answer:
{answer}

Critique it: Is it accurate? Complete? Are there any errors?
Then provide an improved version.
"""
```

### Frameworks

- Reflexion (Shinn et al. 2023)
- Constitutional AI (Anthropic)
- LangChain self-critique chains

### Related Skills

- [Self-Correction](self-correction.md)
- [Critic Agent](../09-agentic-patterns/critic-agent.md)
