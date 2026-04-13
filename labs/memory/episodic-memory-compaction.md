---
id: lab-memory-compaction
title: Episodic Memory Compaction
category: memory
status: experimental
stability: alpha
author: OssamaHashim
updated: 2026-04-13
tags: [memory, compaction, summarization, episodic, labs]
readiness: Alpha — promising but not validated at scale
---

# Lab: Episodic Memory Compaction

> **⚗️ Experimental (Alpha)** — Addresses a core long-context agent problem. Early prototype; needs real-world validation.

## What Is It?

As agents run for many turns, their context window fills up with conversation history. Episodic memory compaction periodically **summarises and compresses** older episodes into a denser representation, freeing context for new interactions while retaining key facts.

## The Problem It Solves

- Context window exhaustion in long-running agents
- Redundant re-reading of irrelevant old turns
- Loss of important facts when simple truncation is used

## Compaction Strategy

```
Full history → [Compaction trigger] → Summarise episodes N-20..N-5
                                    → Keep episodes N-5..N verbatim
                                    → Store summary in episodic_memory[]
                                    → Prepend summary on next turn
```

## Prototype

```python
import anthropic
from dataclasses import dataclass, field

client = anthropic.Anthropic()

@dataclass
class Episode:
    turn: int
    role: str
    content: str

@dataclass
class EpisodicMemory:
    episodes: list[Episode] = field(default_factory=list)
    compacted_summaries: list[str] = field(default_factory=list)
    compaction_threshold: int = 20   # Compact when > N episodes
    keep_recent: int = 5             # Keep last N episodes verbatim

    def add(self, role: str, content: str):
        self.episodes.append(Episode(len(self.episodes), role, content))
        if len(self.episodes) > self.compaction_threshold:
            self._compact()

    def _compact(self):
        to_compact = self.episodes[:-self.keep_recent]
        verbatim = self.episodes[-self.keep_recent:]

        history_text = "\n".join(
            f"{e.role.upper()}: {e.content}" for e in to_compact
        )
        prompt = f"""Summarise the following conversation history into a concise paragraph
capturing all key facts, decisions, and context an agent would need.
Do not omit names, numbers, dates, or explicit commitments.\n\n{history_text}"""

        resp = client.messages.create(
            model="claude-haiku-4-5",
            max_tokens=512,
            messages=[{"role": "user", "content": prompt}]
        )
        summary = resp.content[0].text.strip()
        self.compacted_summaries.append(summary)
        self.episodes = list(verbatim)

    def build_context(self) -> list[dict]:
        """Build the messages list to pass to the model."""
        messages = []
        if self.compacted_summaries:
            combined = "\n\n".join(
                f"[Episode summary {i+1}]: {s}"
                for i, s in enumerate(self.compacted_summaries)
            )
            messages.append({
                "role": "user",
                "content": f"<memory>\n{combined}\n</memory>\n\nContinue from memory above."
            })
            messages.append({"role": "assistant", "content": "Understood, I have the context."})
        for e in self.episodes:
            messages.append({"role": e.role, "content": e.content})
        return messages

# Usage
mem = EpisodicMemory(compaction_threshold=10, keep_recent=3)
mem.add("user", "My name is Alex and I'm building a RAG pipeline.")
mem.add("assistant", "Got it, Alex. What embedding model are you using?")
# ... more turns ...
context = mem.build_context()
print(f"Compacted summaries: {len(mem.compacted_summaries)}")
print(f"Live episodes: {len(mem.episodes)}")
```

## Open Questions

- What facts are most commonly lost during compaction? (needs empirical study)
- Should compaction be triggered by token count rather than turn count?
- Can we use a structured JSON summary instead of free text for higher recall?

## Graduation Criteria

- [ ] Recall benchmark: compare fact retrieval from compacted vs. full history over 50-turn sessions
- [ ] Structured vs. free-text summary comparison
- [ ] Token budget analysis vs. keep_recent tradeoff
- [ ] Validated on ≥2 real agent types (customer support, coding assistant)
