# Benchmarks

> **Quantitative skill comparisons** — real numbers, real trade-offs, so you can choose the right skill for your use case.

Benchmarks are the "scorecards" of the Skills Tree. We test competing approaches against each other on real datasets and publish the results here so you don't have to.

---

## What Makes a Benchmark

A Benchmark must:

- Compare **2+ competing approaches** to the same capability
- Use a **named public dataset** or clearly described custom test set
- Report **at least 2 metrics** (accuracy, cost, latency, recall, etc.)
- Be **reproducible** — include code or a clear methodology
- State **what was tested** and **what was not** (scope limits)

---

## Available Benchmarks

| Benchmark | Category | Winner | Link |
|---|---|---|---|
| ReAct vs LATS | Reasoning / Agentic | LATS (+8.3%) | [→](reasoning/react-vs-lats.md) |
| RAG Retrieval Strategies | Memory | HyDE (+12% recall) | [→](memory/rag-retrieval-strategies.md) |
| Memory Injection Methods | Memory | Top-K Semantic | [→](memory/injection-strategies.md) |
| Code Gen: Claude vs GPT-4o | Code | Claude 3.7 (+6%) | [→](code/model-comparison.md) |

---

## Contribute a Benchmark

```bash
cp meta/benchmark-template.md benchmarks/category/skill-a-vs-skill-b.md
# PR title: benchmark: [skill-a] vs [skill-b] on [dataset]
```

**Quality bar:** Numbers must be reproducible. If you can't share the dataset, describe it precisely enough for others to replicate.
