# RECOMMENDATION_ENGINE_READINESS

**Workstream:** E — Recommendation Engine Readiness  
**Sprint:** Phase 2 — Repository Maturity Sprint  
**Generated:** 2026-07-05  
**Status:** COMPLETE  
**Note:** No `RECOMMENDATION_ENGINE_SPEC.md` exists in the repository at the time of this audit. This report assesses implementation readiness by inspecting actual source files, test coverage, and corpus data artifacts.

---

## SECTION 1: Recommendation Engine Source Inventory

The following files constitute the recommendation engine as currently implemented:

| File | Size | Role |
|------|------|------|
| `tests/test_recommendations.py` | 8,112 bytes | Test coverage for recommendations |
| `tests/test_ranking_calibrator.py` | 7,917 bytes | Test coverage for ranking/calibration |
| `evaluation/evaluator.py` | 16,410 bytes | Evaluation harness (feeds recommendation engine) |
| `evaluation/results.json` | 3,368 bytes | Evaluation results |
| `evaluation/calibration_report.json` | 6,109 bytes | Calibration data |
| `evaluation/consistency_report.json` | 3,085 bytes | Consistency report |
| `evaluation/scenarios.json` | 20,459 bytes | Evaluation scenarios |
| `meta/INITIATIVE_009D_RECOMMENDATION_BENCHMARK.md` | 2,050 bytes | Benchmark spec |
| `meta/INITIATIVE_009_RECOMMENDATION_BENCHMARK.md` | 3,608 bytes | Benchmark spec v2 |

**No formal RECOMMENDATION_ENGINE_SPEC.md found in repository.**  
The engine is implicitly specified through the test files, evaluation artifacts, and initiative documents.

---

## SECTION 2: Implementation Status Assessment

### Implemented Components

| Component | Evidence | Status |
|-----------|----------|--------|
| Basic recommendation output | `test_recommendations.py` exists (8KB — substantial) | ✅ IMPLEMENTED |
| Ranking calibration | `test_ranking_calibrator.py` (7.9KB) + `evaluation/calibration_report.json` | ✅ IMPLEMENTED |
| Evaluation harness | `evaluation/evaluator.py` (16.4KB — largest eval file) | ✅ IMPLEMENTED |
| Evaluation scenarios | `evaluation/scenarios.json` (20.4KB) + `evaluation/cli_scenarios.json` | ✅ IMPLEMENTED |
| Consistency scoring | `evaluation/consistency_report.json` + `evaluation/consistency_suite.json` | ✅ IMPLEMENTED |
| Results persistence | `evaluation/results.json` | ✅ IMPLEMENTED |

### Partially Implemented Components

| Component | Evidence | Gap | Status |
|-----------|----------|-----|--------|
| Corpus-aware recommendations | `test_recommendations.py` references corpus | No corpus-evaluation cross-reference in engine | ⚠️ PARTIAL |
| P0 capability prioritization | Referenced in benchmark docs but not in test assertions | No test enforces P0 caps are recommended first | ⚠️ PARTIAL |
| Evaluation status awareness | Evaluator exists but no test verifies unevaluated caps excluded | Engine may recommend unevaluated P0 capabilities as ready | ⚠️ PARTIAL |

### Missing Components

| Component | Gap | Severity |
|-----------|-----|----------|
| Formal specification document | No RECOMMENDATION_ENGINE_SPEC.md | MEDIUM |
| Evaluation ontology ↔ recommendation linkage | Engine does not verify evaluation validity before recommending | HIGH |
| Safety-tier gate in recommendations | No mechanism to exclude safety-tier caps without valid evaluation | CRITICAL |
| P0 evaluation completeness gate | No gate preventing P0-incomplete agent recommendations | HIGH |
| Dependency graph for recommendations | No explicit dependency specification between engine components | MEDIUM |

---

## SECTION 3: Gap Analysis

| Gap ID | Description | Impact | Priority |
|--------|-------------|--------|----------|
| GAP-REC-001 | No formal spec document | Onboarding friction; no authoritative source of truth | P2 |
| GAP-REC-002 | Evaluation validity not checked before recommendation | Engine can recommend agents backed by phantom evaluations (CAP-023, CAP-025) | **P0 BLOCKER** |
| GAP-REC-003 | Safety-tier capabilities not gated | Agents requiring CAP-025 (PII) can be recommended without valid PII evaluation | **P0 BLOCKER** |
| GAP-REC-004 | P0 evaluation coverage not enforced | 3 P0 capabilities unmapped; engine unaware | P1 |
| GAP-REC-005 | No corpus-diversity signal in ranking | All recommendations from 2 corpus entries in same domain | P1 |
| GAP-REC-006 | No dependency graph documented | Hard to trace recommendation → evaluation → capability chain | P2 |

---

## SECTION 4: Execution Plan

### Step E-001: Create RECOMMENDATION_ENGINE_SPEC.md [P2]

- Author formal spec documenting: inputs (corpus, capability ontology, evaluation ontology), processing (scoring algorithm, ranking calibration, P0 gating), outputs (ranked recommendation list with evaluation status)
- **Effort:** 4 hours
- **Dependency:** None

### Step E-002: Implement evaluation validity check [P0 BLOCKER]

- Add pre-recommendation gate: before any capability is recommended, verify its evaluation entry exists **and** the name matches the canonical capability name
- This directly addresses GAP-REC-002 and the phantom evaluation bypass
- **Target file:** `evaluation/evaluator.py` or recommendation engine source
- **Effort:** 4 hours
- **Dependency:** Workstream A corrections (C-001, C-002) must be applied first

### Step E-003: Implement safety-tier gate [P0 BLOCKER]

- Add capability tier check: any capability with `tier=safety` requires a valid evaluation before being included in a production recommendation
- **Target file:** Recommendation engine source
- **Effort:** 3 hours
- **Dependency:** E-002 (evaluation validity check)

### Step E-004: Add P0 evaluation completeness gate [P1]

- Add check: if any P0 capability in the target corpus entry is unmapped in evaluation_ontology, recommendation returns WARNING status (not READY)
- **Target file:** Recommendation engine source
- **Effort:** 3 hours
- **Dependency:** E-002

### Step E-005: Add test coverage [P1]

- Extend `test_recommendations.py` to assert E-002, E-003, E-004 behavior
- See TEST_COVERAGE_RECOVERY_PLAN.md Task T-004
- **Effort:** 3 hours
- **Dependency:** E-002, E-003, E-004 implemented

---

## SECTION 5: Dependency Graph

```
Capability Ontology (capability_ontology.json)
        │
        ▼
Evaluation Ontology (evaluation_ontology.json)
        │
        ├── [GATE] Name matches canonical cap name  ← Workstream A (C-001, C-002)
        │
        ▼
Evaluator (evaluation/evaluator.py)
        │
        ├── [GATE] Safety-tier caps have valid eval  ← Step E-003
        ├── [GATE] P0 caps have valid eval            ← Step E-004
        │
        ▼
Ranking Calibrator
        │
        ▼
Recommendation Engine
        │
        ├── [GATE] Evaluation validity pre-check      ← Step E-002
        │
        ▼
Corpus Entries (CORPUS-001, CORPUS-002)
```

---

## SECTION 6: Readiness Score

| Dimension | Score | Notes |
|-----------|-------|-------|
| Core implementation | 70/100 | Engine, harness, calibration all present |
| Test coverage | 45/100 | Tests exist but miss critical gates |
| Evaluation integrity | 20/100 | Phantom evaluations not caught |
| Safety gate | 0/100 | No safety-tier gate in engine |
| Formal specification | 0/100 | No RECOMMENDATION_ENGINE_SPEC.md |
| **Overall readiness** | **27/100** | **NOT PRODUCTION READY** |

**Blockers before production:** GAP-REC-002 (evaluation validity) and GAP-REC-003 (safety gate) must be resolved.

---

*Generated: 2026-07-05. Evidence: repository state at commit `0752a72afcb2d659dc0219ec1d385840b7e69186`.*
