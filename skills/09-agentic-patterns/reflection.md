---
title: "Reflection / Reflexion"
category: 09-agentic-patterns
level: advanced
stability: stable
description: "Apply reflection / reflexion in AI agent workflows."
added: "2025-03"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-09-agentic-patterns-reflection.json)

# Reflection / Reflexion

**Category:** `agentic-patterns`
**Skill Level:** `advanced`
**Stability:** `stable`
**Added:** 2025-03

### Description

After producing an output the agent critiques its own work, identifies errors, and iteratively improves until a quality threshold is met.

### Example

```
Attempt 1: Write a function to reverse a linked list.
→ Output: [code with bug]

Reflection: The function doesn't handle the edge case of a single node.
→ Fix: Add `if not head or not head.next: return head`

Attempt 2: [corrected code] ✓ passes all tests
```

### Frameworks

- LangGraph self-loop with critique node
- Reflexion (Shinn et al., 2023)
- OpenAI `o1` internal self-critique

### Related Skills

- [Critic Agent](critic-agent.md)
- [Chain of Thought](cot.md)
- [Constitutional AI](constitutional-ai.md)
