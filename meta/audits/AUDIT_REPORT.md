# Skills Tree — Autonomous Engineering Audit

**Audit baseline:** `main` at `7d00d0e034b4ba7edfacc512c2794080f7fb8a62`
**Audit branch:** `agent/production-hardening-20260917`
**Date:** 2026-09-17

## Executive assessment

The repository contains a substantial working recommendation/API/CLI/MCP stack, but the current production boundary is weaker than the project documentation implies. The highest-value issues are correctness and behavioral-test integrity, not a wholesale rewrite.

## Architecture map

```text
Taxonomy (meta/GOAL_TAXONOMY.md)
        |
        v
GoalTaxonomyParser -----> RecommendationEngine <----- SkillsGraph (data/SKILLS_GRAPH.json)
        |                         |
        |                         +---- EvidenceDeriver <----- benchmarks/INDEX.json
        |                         +---- SkillScorer
        |                         +---- ExplanationEngine
        |                         +---- learning-path traversal
        v                         v
     API routes --------------> BlueprintGenerator
        ^                         |
        |                         v
      MCP tools               Blueprint JSON
        ^
        |
      CLI (currently via FastAPI TestClient)
```

## Runtime flow findings

1. `api/dependencies.py` constructs cached taxonomy, graph, recommendation engine, calibrator, and blueprint generator instances.
2. `POST /recommend` calls the real `RecommendationEngine`, then applies a separate calibration pass before building API summaries.
3. `POST /blueprint` calls the recommendation engine and then `BlueprintGenerator`.
4. MCP currently delegates to the API layer through an in-process `TestClient`.
5. CLI also delegates to the API layer through an in-process `TestClient`.

## P0/P1/P2/P3 findings

| ID | Severity | Finding | Evidence | Impact |
|---|---|---|---|---|
| AUD-001 | P1 | Parent-goal resolution does not reliably consume the Level-4 sub-goal skill lists. | Taxonomy stores detailed mappings under `#### Gxx.y` sections, while the original parser primarily scans `###` mapping sections. | Canonical goals can resolve successfully while producing incomplete/empty skill sets. |
| AUD-002 | P1 | Recommendation tests were synthetic rather than behavioral. | Original `tests/test_recommendations.py` constructed dictionaries/lists directly and never instantiated `RecommendationEngine`. | Core recommendation behavior could regress while the suite remained green. **Remediated on hardening branch.** |
| AUD-003 | P1 | Blueprint tests were synthetic rather than behavioral. | Original `tests/test_blueprints.py` constructed blueprint dictionaries directly and never called `BlueprintGenerator`. | Blueprint regressions could pass CI. **Remediated on hardening branch.** |
| AUD-004 | P1 | Calibration could reorder skills using positional synthetic base scores while API summaries retained pre-calibration scores. | `RankingCalibrator._normalise_input()` assigns `10.0 - index` to ID-only inputs; the API used `calibrate_ids()` and retained `s["score"]`. | Ranking and displayed score could describe different orderings. **Remediated on hardening branch by calibrating actual engine scores.** |
| AUD-005 | P1 | Consistency scenario metadata is stale relative to the current goal taxonomy. | `evaluation/consistency_suite.json` maps Browser Agent to `G02`, while the current taxonomy defines Browser Agent as `G03`; several other mappings also drift. | A parity suite can validate the wrong semantic contract. |
| AUD-006 | P1 | Experience level is accepted by the API contract but is not used by `RecommendationEngine.recommend()`. | Request model validates `experience`, but the engine signature only accepts `goal_query`. | User context promised by the API does not affect recommendation behavior. |
| AUD-007 | P1 | Time-budget filtering is presentation-layer logic and only filters required skills. | `api/routes/recommend.py` filters `required_skills` after calibration and leaves optional skills unchanged. | Budget-constrained output can be semantically inconsistent. |
| AUD-008 | P2 | Blueprint IDs and timestamps are generated from wall-clock time. | `BlueprintGenerator.generate()` uses `datetime.now()` for `id` and `generated_at`. | Blueprint content is not fully reproducible including identity metadata. |
| AUD-009 | P2 | Framework evidence is goal-level maximum framework strength, not skill-level framework evidence. | `EvidenceDeriver.derive()` receives `top_fw_stars` and applies it to each skill. | Explanations can imply skill-level framework alignment without skill-level evidence. |
| AUD-010 | P2 | CLI and MCP use `FastAPI TestClient` as their application integration mechanism. | `cli/main.py` and `mcp/tools.py` construct in-process `TestClient` instances. | Domain/application logic is coupled to the HTTP transport. |
| AUD-011 | P2 | API uses wildcard CORS and exposes exception strings through error responses. | `api/main.py` uses wildcard CORS and serializes `str(exc)` as `detail`. | Production hardening and information-disclosure risk. |
| AUD-012 | P2 | Calibration tables are hardcoded Python dictionaries. | `tools/ranking_calibrator.py` defines global, goal, and keyword adjustment tables in source. | Calibration changes are not independently versioned or traceable as data. |
| AUD-013 | P2 | Core intelligence remains concentrated in `tools/architect.py`. | Parser, graph, evidence, explanation, scoring, recommendation, and blueprint responsibilities are in one module. | High coupling and change risk. Extraction should follow the behavioral safety net. |
| AUD-014 | P3 | Repository contains extensive historical/sprint documentation and generated artifacts. | Tree inspection shows large `meta/`, `evaluation/`, workflow, and generated-data surfaces. | Documentation/source-of-truth drift is harder to detect. |
| AUD-015 | P0 | Existing Test Suite CI was unable to execute its configured test command. | Workflow `.github/workflows/test.yml` invoked `pytest` with `--cov` and `-n`, but the workflow installed `requirements.txt` without `pytest-cov` or `pytest-xdist`. Verified from GitHub Actions run `35242169584`: Python 3.13 job failed with `pytest: error: unrecognized arguments: --cov=tools ... -n`. | CI was red independently of application correctness; test enforcement was non-functional. **Remediated on hardening branch by declaring both plugins and aligning Python versions.** |

## Remediations already applied on hardening branch

- Added `tools/taxonomy_runtime.py` as a compatibility-preserving runtime parser for detailed Level-4 sub-goal mappings.
- API dependency construction now uses the runtime taxonomy adapter.
- Replaced synthetic recommendation tests with real engine/API behavioral tests.
- Replaced synthetic blueprint tests with real generator tests.
- API calibration now receives actual engine scores and returns calibrated scores to clients.
- Test CI now declares `pytest-cov` and `pytest-xdist` and tests only the Python versions supported by `pyproject.toml` (`3.11`–`3.13`).
- Added current/target architecture documentation and ADR-001.

## Source-of-truth matrix

| Domain | Current authoritative source | Assessment |
|---|---|---|
| Skills | `skills/` | Primary content source |
| Goals | `meta/GOAL_TAXONOMY.md` | Primary taxonomy source; parser coverage hardened on branch |
| Graph | `data/SKILLS_GRAPH.json` | Generated artifact; metadata says schema 3.1 |
| Graph generation | `tools/build_graph.py` | Generator source |
| Benchmarks | `benchmarks/INDEX.json` | Runtime evidence source |
| Calibration | `tools/ranking_calibrator.py` | Hardcoded source; should become versioned data |
| API contract | `api/models.py` | Pydantic contract |
| Blueprint contract | API model + generator output | No dedicated strict schema enforcement |
| Package version | `pyproject.toml` | `1.46.0` |

## Versioning observations

- Package version: `1.46.0`.
- Graph schema: `3.1` in `SKILLS_GRAPH.json` metadata.
- Taxonomy document is dated 2026-06-14 and describes itself as complete.
- Architect source comments still reference older graph schema terminology in places.
- Calibration has no runtime-exposed version.
- Recommendation/API response does not expose a traceable taxonomy/graph/benchmark/calibration version bundle.

## CI assessment

The repository has extensive CI coverage. During this hardening run, the existing Test Suite was directly inspected through GitHub Actions. Run `35242169584` failed on Python 3.13 before test collection because `pytest-cov` and `pytest-xdist` were not installed even though the command required their plugins. The workflow also tested Python 3.10 despite `pyproject.toml` declaring `requires-python = ">=3.11"`.

A new commit containing the CI remediation is now on the hardening branch. GitHub Actions is the authoritative validation source; no local test result is claimed because the execution environment used for this work cannot resolve GitHub for cloning.

## Security assessment

The workflows inspected use explicit read-only `contents` permissions in the build/verification paths, which is a positive baseline. Remaining concerns are API wildcard CORS, exception detail exposure, dependency/supply-chain policy depth, and ensuring every workflow maintains least privilege.

## Immediate execution plan

### P1 vertical slice — in progress

1. Establish real RecommendationEngine behavioral tests. **Done on branch.**
2. Establish real BlueprintGenerator behavioral tests. **Done on branch.**
3. Add deterministic/invariant assertions. **Done for initial recommendation/blueprint coverage.**
4. Add a regression test for canonical parent-goal skill resolution. **Done on branch.**
5. Route production taxonomy loading through a compatibility-preserving runtime adapter. **Done on branch.**
6. Validate the branch through GitHub CI. **Pending final post-remediation run.**

### Next P1 slices

- Reconcile consistency-suite goal IDs with the authoritative taxonomy.
- Make experience and time constraints real application-level inputs.
- Extract domain/application services incrementally.
- Version calibration data and expose provenance.
- Replace static goal-to-architecture selection with capability/graph-derived inference behind a compatibility fallback.
