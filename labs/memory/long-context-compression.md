# Lab: Long-Context Compression Strategies

**Category:** `memory`  
**Type:** `lab`  
**Status:** In Progress  
**Version:** v1  
**Added:** 2026-04

---

## Motivation

As agent conversations grow, context windows fill up. Naive truncation loses critical information. This lab experiments with 4 compression strategies to find the best accuracy-vs-token tradeoff for long-running agent sessions.

---

## Strategies Tested

| Strategy | Mechanism | Compression Ratio |
|---|---|---|
| **Truncation** | Drop oldest messages | 1:N (hard cutoff) |
| **Summarisation** | LLM summarises old messages | 4:1 to 8:1 |
| **Selective retention** | LLM marks "important" messages | 3:1 to 6:1 |
| **Hierarchical memory** | Recent = full, older = summary, oldest = key facts | 6:1 to 12:1 |

---

## Experiment Setup

- **Task:** Multi-step research task requiring recall of information from turn 1–5 when answering at turn 20+
- **Baseline:** Full context (no compression)
- **Metric:** Answer accuracy on 50 reference questions requiring long-range recall
- **Models:** Claude Sonnet 4.5, GPT-4o
- **Conversation length:** 20 turns, ~25K tokens before compression

---

## Implementation

```python
from anthropic import Anthropic

client = Anthropic()

def summarise_old_messages(messages: list, keep_recent: int = 6) -> list:
    """Summarise messages[:-keep_recent] into a single system message."""
    if len(messages) <= keep_recent:
        return messages

    old = messages[:-keep_recent]
    recent = messages[-keep_recent:]

    summary_resp = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=512,
        messages=[{
            "role": "user",
            "content": (
                "Summarise the following conversation history into a concise "
                "paragraph. Preserve: decisions made, facts established, "
                "open questions. Discard: small talk, repeated content.\n\n"
                + "\n".join(f"{m['role']}: {m['content']}" for m in old)
            )
        }]
    )

    summary_msg = {
        "role": "user",
        "content": f"[CONVERSATION SUMMARY — earlier turns]:\n{summary_resp.content[0].text}"
    }
    return [summary_msg] + recent


def hierarchical_compress(messages: list) -> list:
    """Recent 4 full → next 8 summarised → rest as key facts."""
    if len(messages) <= 12:
        return messages
    very_old = messages[:-12]
    mid = messages[-12:-4]
    recent = messages[-4:]

    facts = client.messages.create(
        model="claude-haiku-4-5", max_tokens=256,
        messages=[{"role": "user", "content":
            "Extract 5–10 key facts from this history as bullet points:\n"
            + "\n".join(f"{m['role']}: {m['content']}" for m in very_old)}]
    ).content[0].text

    summary = client.messages.create(
        model="claude-haiku-4-5", max_tokens=512,
        messages=[{"role": "user", "content":
            "Summarise:\n"
            + "\n".join(f"{m['role']}: {m['content']}" for m in mid)}]
    ).content[0].text

    return [
        {"role": "user", "content": f"[KEY FACTS from early conversation]:\n{facts}"},
        {"role": "user", "content": f"[SUMMARY of middle conversation]:\n{summary}"},
    ] + recent
```

---

## Preliminary Results

| Strategy | Recall Accuracy | Token Reduction | Cost vs. Baseline |
|---|---|---|---|
| Truncation | 51% | 75% | -75% |
| Summarisation | 74% | 72% | -68% (+ Haiku cost) |
| Selective retention | 79% | 65% | -62% (+ Haiku cost) |
| Hierarchical | **83%** | 78% | -70% (+ 2× Haiku) |
| Full context (baseline) | 91% | 0% | baseline |

---

## Next Steps

- [ ] Test with `mem0` external memory integration
- [ ] Compare vector-search retrieval vs. summarisation at 50-turn conversations
- [ ] Evaluate on domain-specific tasks (code agent, research agent)
- [ ] Measure latency overhead of compression step

---

## Related

- [Skill: Memory Injection](../../skills/03-memory/memory-injection.md)
- [Lab: Tree of Agents](../reasoning/tree-of-agents.md)
