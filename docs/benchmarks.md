# Benchmarks

All benchmarks in Skills Tree are reproducible: they include methodology, datasets, and test scripts.

## Available Benchmarks

### Reasoning

| Benchmark | Dataset | Winner | Margin | Link |
|---|---|---|---|---|
| ReAct vs LATS | HotpotQA | LATS | +8.3% accuracy | [View](../benchmarks/reasoning/react-vs-lats.md) |

### Memory & Retrieval

| Benchmark | Dataset | Winner | Margin | Link |
|---|---|---|---|---|
| RAG retrieval strategies | Custom | HyDE | +12% recall | [View](../benchmarks/memory/rag-retrieval-strategies.md) |
| Memory injection methods | Custom | Top-K semantic | Best cost/quality | [View](../benchmarks/memory/injection-strategies.md) |

### Tool Use

| Benchmark | Dataset | Winner | Margin | Link |
|---|---|---|---|---|
| Function calling | ToolBench | Claude 3.7 | +6% accuracy | [View](../benchmarks/tool-use/function-calling-comparison.md) |

## Reproducing a Benchmark

```bash
git clone https://github.com/SamoTech/skills-tree.git
cd skills-tree
pip install -r requirements.txt
python benchmarks/reasoning/react-vs-lats.py
```

## Contributing Benchmarks

Benchmarks are among the highest-value contributions. To add one:

1. Create `benchmarks/{category}/{name}.md` following the existing format
2. Include: dataset, methodology, results table, reproduction script
3. Open a PR with title format: `benchmark: [skill-a] vs [skill-b]`

See [contributing guide](contributing.md) for full details.
