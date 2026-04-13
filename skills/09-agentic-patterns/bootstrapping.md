---
title: "Bootstrapping"
category: 09-agentic-patterns
level: advanced
stability: experimental
description: "Apply bootstrapping in AI agent workflows."
added: "2025-03"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-09-agentic-patterns-bootstrapping.json)

# Bootstrapping

**Category:** `agentic-patterns`
**Skill Level:** `advanced`
**Stability:** `experimental`
**Added:** 2025-03

### Description

Agent generates its own training data (question-answer pairs, preference pairs, or demonstrations) to fine-tune itself or a smaller model, iteratively improving capability without human annotation.

### Example

```python
# Generate synthetic Q&A pairs
for topic in topics:
    question = llm.generate(f"Write a hard question about: {topic}")
    answer   = llm.generate(f"Answer this question: {question}")
    dataset.append({"question": question, "answer": answer})

# Fine-tune smaller model on dataset
trainer.train(model=small_model, data=dataset)
```

### Related Skills

- [Self-Play](self-play.md)
- [Constitutional AI](constitutional-ai.md)
- [Reflection](reflection.md)
