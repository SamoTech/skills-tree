# Blueprint Name

> 📋 Copy to `blueprints/your-blueprint.md`, fill in every field, delete this block.
> A blueprint is a **production architecture** — not a tutorial. It must be opinionated, runnable, and explicit about cost / failure modes.

**Pattern:** RAG | Multi-Agent | Computer Use | Memory-First | HITL | Self-Healing | Other  
**Skills Used:** [Skill A](../skills/XX/skill-a.md) · [Skill B](../skills/XX/skill-b.md)  
**Complexity:** Basic | Intermediate | Advanced  
**Version:** v1  
**Added:** YYYY-MM

---

## What It Solves

One paragraph: which class of agent system does this architecture target, and what failure mode of naive implementations does it eliminate?

---

## Architecture

```
┌─────────────┐     ┌──────────────┐     ┌────────────┐
│   Client    │ ──▶ │  Orchestrator │ ──▶ │  Skill A   │
└─────────────┘     │   (this BP)   │     └────────────┘
                    └──────┬────────┘
                           ▼
                    ┌────────────┐
                    │  Skill B   │
                    └────────────┘
```

Replace with the real component diagram. Show every external system (vector DB, queue, observability sink) and every skill node.

---

## Technology Choices

| Layer | Choice | Rationale |
|---|---|---|
| Model | `claude-opus-4-5` / `gpt-4o` | Why this model for this layer |
| Vector DB | Qdrant / pgvector / Pinecone | Latency, cost, ops profile |
| Queue / state | Redis / SQLite / Postgres | Persistence guarantees needed |
| Observability | OpenTelemetry / Langfuse / W&B | What you must trace to debug failures |

State **one** primary choice per layer. If you list alternatives, explain when to pick each.

---

## Implementation

```python
# Complete, runnable reference implementation.
# Must import real libraries and call real APIs (or clearly mocked ones).
# Must include error handling, retries, and a way to observe failures.
```

---

## Cost & Latency

| Metric | Value | Notes |
|---|---|---|
| Avg. p50 latency | Xs | End-to-end, single request |
| Avg. p95 latency | Xs | Under expected concurrency |
| Avg. cost per request | $X | Including embeddings + LLM tokens |
| Scaling profile | linear / sub-linear / quadratic | What cost grows with |

---

## Failure Modes

| Failure | Cause | Mitigation |
|---|---|---|
| Retrieval misses | Poor embedding fit | Try HyDE / reranker |
| Tool timeout | Upstream slow | Bounded retry + circuit breaker |
| Hallucinated tool args | Model drift | JSON schema validator + repair loop |

Every blueprint MUST list at least three failure modes — that's the difference between a tutorial and a blueprint.

---

## When NOT to Use This

- List the cases where a simpler design is correct.
- Be honest. Blueprints that can't articulate their non-fit are over-engineered.

---

## Scaling Notes

How does this architecture behave at 10× / 100× traffic? Where does it break first? What's the upgrade path?

---

## Related

- **Skills:** [skill-a](../skills/XX-category/skill-a.md), [skill-b](../skills/XX-category/skill-b.md)
- **Systems:** [system-name](../systems/system-name.md)
- **Blueprints:** [blueprint-name](../blueprints/blueprint-name.md)

---

## Changelog

| Date | Change |
|---|---|
| `YYYY-MM` | v1 initial |
