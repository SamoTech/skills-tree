# Evaluation Contracts — Public Protocol

> This is the protocol surface of the Skills Tree **evaluation layer**: the
> fail-closed capability-contract harness (CAP-0xx series), distinct from the
> skill-comparison benchmarks indexed in [README.md](README.md). It is published
> so that **any agent maintainer can evaluate their own candidate system against
> these contracts, or reuse the methodology in their own capability domains.**

## Contracts on main

| Contract | Domain | Dataset | Runner | Empirical status |
|---|---|---|---|---|
| CAP-011 | self-evaluation calibration | `self-evaluation/cap011-dataset-v1.json` | `tools/run_cap011_calibration_benchmark.py` | EXECUTED 2026-10-13, PASS |
| CAP-014 | tool execution (mocked) | `tool-execution/cap014-mocked-scenarios-v1.json` | `tools/run_cap014_mock_benchmark.py` | EXECUTED 2026-10-14, PASS |
| CAP-007 | support-query resolution | protocol merged (PRs #456, #458) | fail-closed; requires human labels | NOT RUN (no labeled dataset) |

## The methodology (reusable principles)

1. **Versioned dataset with provenance.** Every dataset is immutable and
   versioned, carries a `provenance` block (source, methodology,
   `human_labeled`), and an explicit `acceptance` block with numeric
   thresholds. Datasets are never edited after a run; a change creates a new
   version.
2. **Fail-closed scorer.** The runner is the authority, not the candidate.
   Missing/extra/duplicate results, malformed records, scope escalation,
   unapproved deployment triggers, claimed side effects, or a missing candidate
   file produce NOT_RUN or FAIL, never PASS.
3. **Machine-verified reporting.** The runner report is committed next to the
   candidate results, and CI re-executes the runner on every push, requiring
   parsed equality with the committed report
   (`tests/test_cap011_empirical_run.py`, `tests/test_cap014_empirical_run.py`).
   A published result is therefore machine-verified, not agent-asserted.
4. **Raw-trace retention with digests.** Per-case raw outputs are retained as a
   committed artifact; each row carries the sha256 of the compact task input and
   of the compact result record, so any consumer can re-derive the digests.
5. **Disclosure of overlap.** If the candidate system shares an agent family
   (or any material overlap) with the dataset author or repository maintainer,
   the candidate records must disclose it. Known limitation of the executed
   runs: the CAP-011 and CAP-014 candidates are the repository maintainer agent
   itself (disclosed); a second, non-overlapping external candidate is a
   standing goal.
6. **Cross-check guards before commit.** A candidate-side guard compares derived
   outputs against the fixture expected records and aborts on disagreement, so
   a run is never committed with silent mismatches.
7. **No fabricated labels.** Datasets that require human labeling (CAP-007)
   remain NOT RUN until independently labeled data exists. Synthetic fixtures
   are always labeled `human_labeled: false` and are never claimed as real-world
   performance evidence.

## Evaluate your own candidate

Each contract defines its candidate-results format in the per-directory README
(`self-evaluation/`, `tool-execution/`). In short:

```bash
# CAP-011 (self-evaluation calibration)
python tools/run_cap011_calibration_benchmark.py \
  --candidate-results path/to/your/candidate-results.json \
  --output your-report.json

# CAP-014 (mocked tool execution)
python tools/run_cap014_mock_benchmark.py \
  --candidate-results path/to/your/candidate-results.json \
  --output your-report.json
```

Produce the candidate results by actually running your system against each
case/scenario (observed invocations and responses), never by copying the
dataset `expected` records. Retain your raw traces and publish the report with
your results. A PASS from this harness is only meaningful if the candidate
records come from the actual system under test.

## Reuse the methodology in your own domain

The pattern transfers directly to any capability domain: (a) author a versioned
dataset with provenance and acceptance blocks, (b) write a fail-closed scorer,
(c) commit the report replica and re-execute it in CI, (d) retain raw traces
with digests, (e) disclose any candidate/author overlap, (f) keep human-labeled
and synthetic data strictly separate. This repository treats that protocol as
its primary durable asset; the skill corpus itself is commodity content in a
world where models can generate comparable instructions on demand.

## Adding a new evaluation contract

1. Define the capability contract in `intelligence/ontology/evaluation_ontology.json`.
2. Author the versioned dataset (provenance + acceptance) under a named directory.
3. Write the fail-closed runner under `tools/` with unit tests.
4. Document the candidate-results format in a per-directory README.
5. Only after a real candidate run: commit raw outputs, candidate results, and
   the report replica, and add a CI test that re-executes the runner and
   requires committed-report equality.
