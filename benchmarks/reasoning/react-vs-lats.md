# ReAct vs LATS — Agent Planning Benchmark

**Category:** Reasoning / Agentic Patterns  
**Dataset:** HotpotQA (multi-hop reasoning, 500 questions)  
**Metrics:** Accuracy, avg steps, cost per query, latency  
**Tested:** 2026-04  
**Version:** v1

---

## Summary

| Approach | Accuracy | Avg Steps | Cost/Query | Latency |
|---|---|---|---|---|
| **LATS** | **67.2%** | 8.3 | $0.041 | 18.4s |
| ReAct | 58.9% | 5.1 | $0.018 | 9.2s |
| CoT (baseline) | 44.3% | 1.0 | $0.007 | 2.1s |

**Winner:** LATS on accuracy (+8.3pp over ReAct). ReAct wins on cost (2.3× cheaper) and speed (2× faster).

---

## When to Use Each

| Condition | Use |
|---|---|
| Accuracy is critical, budget flexible | **LATS** |
| Cost or latency constrained | **ReAct** |
| Simple factual Q&A, no multi-hop | **CoT** |
| Interactive / real-time agent | **ReAct** |
| Research / analysis where quality > speed | **LATS** |

---

## Methodology

- Model: `claude-opus-4-5` for both
- HotpotQA 500-question dev split (multi-hop only)
- ReAct: standard observe-think-act loop, max 10 steps
- LATS: 4-branch tree, depth 5, UCT selection, value function = LLM scoring
- Accuracy: exact match on final answer string (lowercased, stripped)
- Cost: Anthropic token pricing as of 2026-04

---

## Key Finding

LATS's tree search finds better intermediate steps on multi-hop questions, but at a significant compute cost. For production systems, a **hybrid approach** works well: ReAct first, fall back to LATS if confidence is low.

```python
def hybrid_plan(question: str, confidence_threshold: float = 0.7) -> str:
    result, confidence = react_agent(question)
    if confidence < confidence_threshold:
        result, _ = lats_agent(question)  # higher quality, higher cost
    return result
```

---

## Related

- [ReAct Skill](../../skills/09-agentic-patterns/react.md)
- [LATS Skill](../../skills/09-agentic-patterns/lats.md)
- [Chain of Thought](../../skills/09-agentic-patterns/chain-of-thought.md)
