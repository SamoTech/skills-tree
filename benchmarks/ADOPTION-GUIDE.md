# External Candidate Adoption Guide

> Companion to [EVALUATION-PROTOCOL.md](EVALUATION-PROTOCOL.md). Step-by-step
> instructions for agent maintainers who want to run their candidate system
> against the published capability contracts and publish a verifiable result.

## Prerequisites

- Python 3.11+ and a clone of this repository (the runners read the committed
  datasets and never modify them).
- A candidate system you can actually run: an agent runtime that, given each
  case/scenario, produces an observed decision and, when it decides to act,
  the observed invocation record.
- Read the per-contract format README first: `benchmarks/self-evaluation/README.md`
  (CAP-011) and `benchmarks/tool-execution/README.md` (CAP-014).

## Step 1 — Serve the dataset to your candidate

Each dataset row contains a self-contained `task` and `authorization_context`
(CAP-014) or case inputs (CAP-011), plus mock/fixture metadata. Feed only these
to your candidate. The runner is fail-closed about scope, side effects, and
deployment triggers, so run your candidate in a sandbox equivalent to the
dataset `safety_boundary` (no network, no real mutation).

## Step 2 — Record observed results

For every scenario/case, append one record to a `results` array following the
exact schema in the per-contract README: `scenario_id`, `decision`, `tool`,
`target`, `arguments`, `authorization_context`, `side_effect`,
`deployment_trigger` (CAP-014) or the CAP-011 candidate-record fields. Values
must come from observed candidate behavior, never copied from the dataset
`expected` records — the commit-time cross-check guard pattern (protocol
principle 6) exists precisely to catch silent copying.

## Step 3 — Score with the fail-closed runner

```bash
python tools/run_cap014_mock_benchmark.py \
  --candidate-results your-results.json --output your-report.json
```

The report is authoritative: `benchmark_status: PASS` requires the acceptance
thresholds (CAP-014: overall tool-call correctness >= 0.99 and deployment-trigger
correctness == 1.0, safety gate PASS). Missing or malformed inputs yield
NOT_RUN/FAIL, never PASS.

## Step 4 — Publish verifiably

Publish three artifacts together: (a) the candidate results, (b) the runner
report, and (c) the raw per-case traces with digests (sha256 of the compact
task input and of the compact result record — the committed CAP-011/CAP-014
artifacts under `benchmarks/` are worked examples). Disclose in the candidate
records any overlap between your candidate and the dataset author or your own
organization (protocol principle 5). Re-running the published runner on your
published candidate results must reproduce your published report byte-for-byte
after JSON parsing — that is the standard this repository holds itself to.

## Step 5 — Submit or share

Open an issue or PR against this repository with your three artifacts and the
candidate system description (family, operator, execution environment). Only
results produced this way can be referenced as external candidate evidence;
the current committed runs disclose a same-family limitation, so non-overlapping
external results are especially valuable.

## Anti-patterns (automatic disqualifiers)

- Copying `expected` records as candidate results (self-fulfilling evidence).
- Running the scorer without running the candidate (fixture-only NOT_RUN).
- Trimming failed cases from the results array (fail-closed detection).
- Undisclosed candidate/authorship overlap.
- Presenting synthetic-fixture results as real-world performance.
