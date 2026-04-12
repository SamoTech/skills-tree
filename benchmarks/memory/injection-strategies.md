---
title: Memory Injection Strategies Benchmark
type: benchmark
category: memory
dataset: MemGPT PersonaChat subset (300 conversations)
models: [claude-opus-4-5]
updated: 2026-04
---

# Memory Injection Strategies — Benchmark

## Summary

| Strategy | Recall@5 | Avg Tokens Injected | Cost/1k turns | Setup |
|---|---|---|---|---|
| **Top-K Semantic** | 84.2% | 620 | $0.62 | Medium |
| **Full History** | 91.1% | 4,800 | $4.80 | Low |
| **Top-K BM25** | 71.3% | 580 | $0.58 | Low |
| **Recency-only** | 63.7% | 600 | $0.60 | Low |
| **No memory** | 31.2% | 0 | $0.20 | None |

**Verdict:** Top-K Semantic is the best cost/quality tradeoff. Full history wins on recall but costs 8x more — viable only for short conversations (< 20 turns).

## Related

- [`skills/03-memory/memory-injection.md`](../../skills/03-memory/memory-injection.md)
- [`blueprints/rag-stack.md`](../../blueprints/rag-stack.md)
