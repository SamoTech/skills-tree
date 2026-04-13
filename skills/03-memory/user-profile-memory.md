---
title: "User Profile Memory"
category: 03-memory
level: intermediate
stability: stable
description: "Apply user profile memory in AI agent workflows."
added: "2025-03"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-03-memory-user-profile-memory.json)

# User Profile Memory

**Category:** `memory`  
**Skill Level:** `intermediate`  
**Stability:** `stable`
**Added:** 2025-03

### Description

Store and retrieve user-specific preferences, history, and attributes to personalize agent behavior across interactions.

### Example

```python
profiles = {}

def update(user_id, key, value):
    profiles.setdefault(user_id, {})[key] = value

def get(user_id):
    return profiles.get(user_id, {})
```

### Related Skills

- [Cross-Session Persistence](cross-session-persistence.md)
- [Episodic Memory](episodic-memory.md)
