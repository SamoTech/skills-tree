# Skill activation evidence

Bounded benchmark for Issue #357: measure whether the expected skill is selected and invoked in real agent sessions.

## Capture paths

| Path | When to use |
|------|-------------|
| [HERMES-TRACE-CAPTURE.md](HERMES-TRACE-CAPTURE.md) | You run Hermes with the observer plugin |
| [MANUAL-TRACE-CAPTURE.md](MANUAL-TRACE-CAPTURE.md) | **No Hermes** — any agent; operator records observed selection/execution |

## Evaluate

```bash
python tools/run_skill_activation_benchmark.py \
  --dataset benchmarks/activation/skill-activation-v1.json \
  --observations path/to/observations.json \
  --output skill-activation-benchmark-result.json
```

Empty or partial corpora are valid. Do not manufacture events.
