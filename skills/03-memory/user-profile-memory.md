---
title: "User Profile Memory"
category: 03-memory
level: intermediate
stability: stable
tags: [memory, personalization, user-profile, preferences, identity]
description: "Store and retrieve user-specific preferences, history, and attributes to personalize agent behavior consistently across interactions."
added: "2025-03"
---

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-03-memory-user-profile-memory.json)

# User Profile Memory

**Category:** `memory`  
**Skill Level:** `intermediate`  
**Stability:** `stable`  
**Added:** 2025-03

---

## Description

User profile memory gives an agent a stable, queryable model of who it is talking to. Rather than deriving user intent from scratch on every turn, the agent can consult accumulated facts — preferred communication style, domain expertise level, frequently used tools, prior decisions — and tailor its responses accordingly.

The key distinction from general [Cross-Session Persistence](cross-session-persistence.md) is scope: the profile is *about the user as a person*, not about a specific task or session. It answers questions like "Does this user prefer terse or detailed responses?", "What tech stack do they use?", "Have they opted out of suggested actions?"

---

## When to Use

- Personalized assistants where tone, verbosity, and assumption level should adapt per user
- Multi-turn agents that need to avoid asking the same clarifying questions twice
- Any product where "the agent knows me" is a differentiating feature
- B2B tools where user role (e.g. frontend dev vs. DevOps) changes which suggestions are relevant

---

## Data Model

```python
from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class UserProfile:
    user_id: str
    name: Optional[str] = None
    language: str = "en"
    timezone: Optional[str] = None
    expertise_level: str = "intermediate"   # beginner | intermediate | expert
    response_style: str = "balanced"        # terse | balanced | detailed
    tech_stack: list[str] = field(default_factory=list)
    preferences: dict[str, Any] = field(default_factory=dict)
    flags: dict[str, bool] = field(default_factory=dict)  # feature/consent flags
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
```

---

## Implementation Pattern

```python
import json
from pathlib import Path
from datetime import datetime, timezone
from dataclasses import asdict


class UserProfileStore:
    """Simple file-backed user profile store. Swap backend for Redis/Supabase in production."""

    def __init__(self, store_dir: str = ".profiles"):
        self._dir = Path(store_dir)
        self._dir.mkdir(parents=True, exist_ok=True)

    def _path(self, user_id: str) -> Path:
        return self._dir / f"{user_id}.json"

    def load(self, user_id: str) -> UserProfile:
        p = self._path(user_id)
        if p.exists():
            data = json.loads(p.read_text(encoding="utf-8"))
            return UserProfile(**data)
        return UserProfile(user_id=user_id)

    def save(self, profile: UserProfile) -> None:
        profile.updated_at = datetime.now(timezone.utc).isoformat()
        if not profile.created_at:
            profile.created_at = profile.updated_at
        self._path(profile.user_id).write_text(
            json.dumps(asdict(profile), ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def update(self, user_id: str, **kwargs) -> UserProfile:
        """Patch specific fields without overwriting the whole profile."""
        profile = self.load(user_id)
        for key, value in kwargs.items():
            if hasattr(profile, key):
                setattr(profile, key, value)
            else:
                profile.preferences[key] = value
        self.save(profile)
        return profile

    def delete(self, user_id: str) -> None:
        """GDPR forget-me: remove all stored data for this user."""
        self._path(user_id).unlink(missing_ok=True)
```

### Injecting the profile into agent context

```python
store = UserProfileStore()

def build_system_prompt(user_id: str) -> str:
    profile = store.load(user_id)
    return f"""You are a helpful assistant.

User profile:
- Name: {profile.name or 'Unknown'}
- Expertise: {profile.expertise_level}
- Preferred response style: {profile.response_style}
- Tech stack: {', '.join(profile.tech_stack) or 'not specified'}
- Language: {profile.language}

Adjust your tone and depth accordingly. Do not ask for information already recorded above.
"""
```

---

## Profile Update Strategies

Profiles should be updated incrementally as new facts emerge — not only on explicit "remember this" commands.

1. **Explicit updates**: The user says "I prefer concise answers" or "I use Python, not Node". Extract and write directly.
2. **Implicit inference**: After several turns, detect patterns (user always asks for code examples → set `response_style` preference `code_heavy`).
3. **Tool-driven discovery**: If the user runs `git log` in a TypeScript repo, update `tech_stack` automatically.
4. **Conflict resolution**: If a new signal contradicts a stored preference, update with a recency weight — don't silently overwrite without logging the change.

---

## Privacy Considerations

User profiles contain personal data. Design for compliance from the start:

- Implement `delete(user_id)` as a first-class API — every `store.save()` must have a matching `store.delete()`
- Log what was stored and when — provide a `get_audit_trail(user_id)` method
- Never persist raw message content; summarise and extract only structured attributes
- Apply field-level encryption for sensitive attributes (medical, financial) even if the store itself is access-controlled
- Respect `profile.flags["consent_personalization"]` — if `False`, load a blank profile at runtime and discard inferences without writing

---

## Pitfalls

- **Profile staleness**: A "beginner" from 2 years ago may now be an expert. Age preferences and re-confirm periodically.
- **Conflating users**: In shared environments (family device, shared API key), one profile may blend multiple people's preferences. Require explicit `user_id` resolution.
- **Preference over-fitting**: Adapting too aggressively to past patterns can make the agent unhelpful when the user's needs change. Treat the profile as a prior, not a constraint.
- **Asking too many questions to populate the profile**: Build it passively from observed behaviour rather than interrogating the user upfront.

---

## Related Skills

- [Cross-Session Persistence](cross-session-persistence.md)
- [Episodic Memory](episodic-memory.md)
- [User Profile (full)](user-profile.md)
- [Memory Injection](memory-injection.md)
