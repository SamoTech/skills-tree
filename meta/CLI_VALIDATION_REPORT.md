# CLI Validation Report

Sprint: **C-12.75** | Scenarios: 20 | Source: `evaluation/cli_scenarios.json`

---

## How to Run

```bash
pip install -e .[dev]
python - <<'EOF'
import json, subprocess, time

with open("evaluation/cli_scenarios.json") as f:
    scenarios = json.load(f)

passed, failed, crashed = 0, 0, 0
total_ms = 0

for s in scenarios:
    t0 = time.perf_counter()
    try:
        r = subprocess.run(
            s["command"], shell=True, capture_output=True, text=True, timeout=15
        )
        ms = (time.perf_counter() - t0) * 1000
        total_ms += ms
        exit_ok = r.returncode == s["expected_exit_code"]
        status = "PASS" if exit_ok else "FAIL"
        if exit_ok: passed += 1
        else: failed += 1
        print(f"  {s['id']} [{status}] {s['description'][:50]:<50s}  {ms:6.0f}ms")
    except subprocess.TimeoutExpired:
        crashed += 1
        print(f"  {s['id']} [CRASH] TIMEOUT after 15s")

print(f"\nResults: {passed}/20 passed | {failed} failed | {crashed} crashed")
print(f"Average: {total_ms/len(scenarios):.0f}ms per scenario")
EOF
```

---

## Scenario Inventory

| ID | Category | Description | Expected Exit |
|---|---|---|---|
| S01 | recommend | Basic recommend, default experience | 0 |
| S02 | recommend | All flags: experience + time-budget | 0 |
| S03 | recommend | Beginner experience | 0 |
| S04 | recommend | Advanced experience | 0 |
| S05 | recommend | Table output format | 0 |
| S06 | recommend | Pretty output format | 0 |
| S07 | error_handling | Unknown goal — graceful fail | 1 |
| S08 | recommend | Short flags (-g, -e) | 0 |
| S09 | blueprint | Coding Agent | 0 |
| S10 | blueprint | RAG Assistant | 0 |
| S11 | blueprint | Multi-Agent Systems | 0 |
| S12 | error_handling | Unknown goal blueprint — graceful fail | 1 |
| S13 | goals | List goals JSON | 0 |
| S14 | goals | List goals table | 0 |
| S15 | skills | List skills JSON | 0 |
| S16 | skills | List skills table | 0 |
| S17 | validate | Full stack no-goal | 0 |
| S18 | validate | Full stack with goal | 0 |
| S19 | meta | --help | 0 |
| S20 | recommend | All flags + low budget | 0 |

---

## Expected Results

| Metric | Target | Threshold |
|---|---|---|
| Pass rate | 20/20 (100%) | ≥ 18/20 (90%) |
| Average execution time | < 500 ms | < 2000 ms |
| Crashes (timeout/exception) | 0 | ≤ 1 |
| Malformed JSON output | 0 | 0 |

See CI run artifact `test_results.txt` for actual measured values.
