# Benchmarks

Benchmark pages describe methodology, datasets, and reproduction material where available. A published result is **current reproducible evidence only when a version-matched run artifact is recorded**. Older result tables and example scripts without a matching run artifact remain historical evidence and must not be treated as current performance or adoption claims.

## Available Benchmarks

### Reasoning

| Benchmark | Dataset | Winner | Margin | Link |
|---|---|---|---|---|
| ReAct vs LATS | HotpotQA | LATS | +8.3 points accuracy | [View](https://github.com/SamoTech/skills-tree/blob/main/benchmarks/reasoning/react-vs-lats.md) |

### Memory & Retrieval

| Benchmark | Dataset | Winner | Margin | Link |
|---|---|---|---|---|
| RAG retrieval strategies | HotpotQA + NaturalQuestions | HyDE | +12.9 points recall | [View](https://github.com/SamoTech/skills-tree/blob/main/benchmarks/memory/rag-retrieval-strategies.md) |
| Memory injection methods | Custom | Top-K semantic | Best cost/quality | [View](https://github.com/SamoTech/skills-tree/blob/main/benchmarks/memory/injection-strategies.md) |

### Tool Use

| Benchmark | Dataset | Winner | Margin | Link |
|---|---|---|---|---|
| Function calling | 200 hand-crafted tasks (5 tool categories) | Claude Opus 4.5 | Top single-call score 95.0 | [View](https://github.com/SamoTech/skills-tree/blob/main/benchmarks/tool-use/function-calling-comparison.md) |

## Reproducing a Benchmark

The example below demonstrates the repository's reproduction convention; it does not establish that every historical result on this page can be reproduced today.

```bash
git clone https://github.com/SamoTech/skills-tree.git
cd skills-tree
pip install -r requirements.txt
```

The historical scorecard pages document their datasets, methodology, and result tables; there is currently **no committed per-benchmark runner script** for them. The CAP capability contracts are the committed, CI-executed evaluation assets — see [EVALUATION-PROTOCOL.md](https://github.com/SamoTech/skills-tree/blob/main/benchmarks/EVALUATION-PROTOCOL.md).

## Contributing Benchmarks

Benchmarks are among the highest-value contributions. To add one:

1. Create `benchmarks/{category}/{name}.md` following the existing format
2. Include: dataset, methodology, results table, reproduction script
3. Open a PR with title format: `benchmark: [skill-a] vs [skill-b]`

See [contributing guide](contributing.md) for full details.
