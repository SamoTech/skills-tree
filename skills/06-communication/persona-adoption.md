![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-06-communication-persona-adoption.json)

# Persona Adoption

**Category:** `communication`  
**Skill Level:** `intermediate`  
**Stability:** `stable`
**Added:** 2025-03

### Description

Adopt a defined character, role, or personality consistently throughout an interaction — used for AI assistants, NPCs, and specialized agents.

### Example

```python
system_prompt = '''
You are DevBot, a senior DevOps engineer with 10 years of experience.
You give concise, opinionated advice and prefer shell commands over GUI solutions.
'''
response = llm.invoke([system_prompt, user_message])
```

### Related Skills

- [Tone Adjustment](tone-adjustment.md)
- [Instruction Following](instruction-following.md)
