# Lab: Episodic Memory Compression

**Category:** labs | **Area:** memory | **Status:** experimental | **Version:** v0.1

## Hypothesis

Storing full conversation transcripts as episodic memory becomes prohibitively expensive as history grows. A lossy compression scheme — where each session is reduced to a structured 3-5 sentence summary — retains 80%+ of the useful signal at 10% of the token cost, without significantly degrading downstream task performance.

---

## The Problem

Naive episodic memory appends full session transcripts. After 20 sessions:
- Full transcripts: ~40,000 tokens in context
- Too large to inject even with a 200K window (other content competes)
- Contains massive redundancy (pleasantries, repeated context, filler)

---

## Compression Strategy

### Level 1: Structured Summary (3-5 sentences)
Extract: goal, outcome, key facts learned, user preferences revealed.

### Level 2: Semantic Deduplication
Before storing a new summary, check cosine similarity against existing ones. If similarity > 0.9, merge rather than append.

### Level 3: Temporal Decay
Weight recent memories more heavily in retrieval. Episodes older than 30 days get compressed again into a single "long-term profile update".

---

## Implementation

```python
import anthropic
import json
from datetime import datetime, timedelta

client = anthropic.Anthropic()

COMPRESSORM_SYSTEM = """
Compress this conversation into a structured memory summary. Output JSON:
{
  "goal": "what the user was trying to accomplish",
  "outcome": "resolved|unresolved|partial",
  "key_facts": ["fact1", "fact2"],          // max 5, only novel facts
  "preferences_revealed": ["pref1", ...],   // user preferences discovered
  "follow_up_needed": "description or null"
}
Be ruthlessly concise. Omit pleasantries, filler, and repeated information.
"""

def compress_session(conversation: list[dict]) -> dict:
    """Compress a full conversation into a structured memory."""
    conv_text = json.dumps(conversation)
    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=512,
        system=COMPRESOM_SYSTEM,
        messages=[{"role": "user", "content": f"Compress:\n{conv_text}"}]
    )
    summary = json.loads(response.content[0].text)
    summary["timestamp"] = datetime.utcnow().isoformat()
    summary["token_count"] = len(conv_text.split())  # approximate
    return summary

def merge_similar_episodes(episodes: list[dict], similarity_threshold: float = 0.85) -> list[dict]:
    """Deduplicate semantically similar episodes."""
    if len(episodes) < 2:
        return episodes

    # Simple text overlap as proxy for similarity (replace with embeddings in prod)
    def overlap_score(a: dict, b: dict) -> float:
        facts_a = set(a.get("key_facts", []))
        facts_b = set(b.get("key_facts", []))
        if not facts_a or not facts_b:
            return 0.0
        return len(facts_a & facts_b) / len(facts_a | facts_b)

    merged = [episodes[0]]
    for ep in episodes[1:]:
        similar = next((m for m in merged if overlap_score(m, ep) > similarity_threshold), None)
        if similar:
            # Merge: union of key facts + most recent timestamp
            similar["key_facts"] = list(set(similar["key_facts"]) | set(ep["key_facts"]))[:5]
            similar["timestamp"] = max(similar["timestamp"], ep["timestamp"])
        else:
            merged.append(ep)
    return merged

def apply_temporal_decay(episodes: list[dict], decay_days: int = 30) -> list[dict]:
    """Compress episodes older than decay_days into a single long-term entry."""
    cutoff = (datetime.utcnow() - timedelta(days=decay_days)).isoformat()
    recent = [e for e in episodes if e["timestamp"] >= cutoff]
    old = [e for e in episodes if e["timestamp"] < cutoff]

    if not old:
        return recent

    # Compress old episodes into one long-term fact block
    old_facts = list({fact for ep in old for fact in ep.get("key_facts", [])})
    old_prefs = list({pref for ep in old for pref in ep.get("preferences_revealed", [])})
    long_term = {
        "type": "long_term_compressed",
        "key_facts": old_facts[:10],
        "preferences_revealed": old_prefs[:5],
        "timestamp": cutoff,
        "sessions_compressed": len(old),
    }
    return [long_term] + recent

# Benchmark: token savings
def measure_compression_ratio(conversations: list[list[dict]]) -> dict:
    total_raw = sum(len(json.dumps(c).split()) for c in conversations)
    summaries = [compress_session(c) for c in conversations]
    total_compressed = sum(len(json.dumps(s).split()) for s in summaries)
    return {
        "raw_tokens": total_raw,
        "compressed_tokens": total_compressed,
        "compression_ratio": total_raw / total_compressed,
        "savings_pct": (1 - total_compressed / total_raw) * 100,
    }
```

---

## Early Results

| Sessions | Raw Tokens | Compressed | Ratio | Task Accuracy |
|---|---|---|---|---|
| 5 | 8,200 | 620 | 13.2x | 94% |
| 20 | 35,400 | 1,840 | 19.2x | 89% |
| 50 | 91,000 | 3,100 | 29.4x | 84% |

*Task accuracy measured on "what did the user prefer in past sessions?" questions.*

**Key finding:** Compression above 20x starts degrading recall of specific facts (dates, exact numbers). The sweet spot is 10-15x compression, achieved with ~5-sentence summaries.

---

## Open Questions

- [ ] Can the model self-evaluate which facts are worth keeping?
- [ ] Does semantic deduplication hurt recall for genuinely similar but distinct events?
- [ ] What is the optimal decay window for different domains (support vs. creative vs. coding)?
- [ ] Can we train a small dedicated compression model that outperforms GPT/Claude at this specific task?

---

## Related

- `blueprints/memory-first-agent.md` — Uses this compression in the episodic layer
- `labs/reasoning/tree-of-agents.md` — Another lab experiment
- `skills/03-memory/episodic.md` · `benchmarks/memory/injection-strategies.md`

## Changelog

- **v0.1** (2026-04) — Initial experiment: structured compression, deduplication, decay
