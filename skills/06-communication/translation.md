---
title: "Translation"
category: 06-communication
level: basic
stability: stable
description: "Apply translation in AI agent workflows."
added: "2025-03"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-06-communication-translation.json)

# Translation

**Category:** `communication`  
**Skill Level:** `basic`  
**Stability:** `stable`
**Added:** 2025-03

### Description

Translate text between any two languages with high accuracy, preserving tone and context.

### Example

```python
prompt = "Translate the following English text to Arabic:\n" + text
result = llm.invoke(prompt)
```

### Frameworks

- Any multilingual LLM
- DeepL API
- Google Translate API

### Related Skills

- [Multilingual Output](multilingual-output.md)
- [Paraphrasing](paraphrasing.md)
