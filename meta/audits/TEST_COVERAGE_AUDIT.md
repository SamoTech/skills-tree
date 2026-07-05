# TEST_COVERAGE_AUDIT

**Workstream:** D — Test Coverage Recovery  
**Sprint:** Phase 2 — Repository Maturity Sprint  
**Generated:** 2026-07-05  
**Status:** COMPLETE  
**Source of record:** `tests/` directory at commit `0752a72afcb2d659dc0219ec1d385840b7e69186`

---

## SECTION 1: Test Inventory

The `tests/` directory contains 14 test modules (excluding `__init__.py`).

| Test File | Size (bytes) | Domain |
|-----------|-------------|--------|
| `test_api.py` | 7,720 | API layer |
| `test_blueprints.py` | 8,227 | Blueprints |
| `test_changelog.py` | 3,765 | Release management |
| `test_check_broken_links.py` | 4,734 | Link validation |
| `test_cli.py` | 9,890 | CLI |
| `test_consistency.py` | 19,433 | **Largest** — cross-system consistency |
| `test_evaluator.py` | 5,306 | Evaluation harness |
| `test_graph.py` | 6,658 | Graph integrity |
| `test_mcp.py` | 6,681 | MCP layer |
| `test_osv_check.py` | 4,865 | OSV security checks |
| `test_osv_watch.py` | 4,311 | OSV watch process |
| `test_ranking_calibrator.py` | 7,917 | Ranking/calibration |
| `test_recommendations.py` | 8,112 | Recommendation engine |
| `test_sync_badges.py` | 2,330 | Badge sync |

**Total test files:** 14  
**Total estimated test size:** ~100 KB

---

## SECTION 2: Ontology Coverage Analysis

### Coverage Assessment

| Ontology Component | Test File | Coverage Status |
|-------------------|-----------|------------------|
| `capability_ontology.json` | `test_consistency.py` (cross-reference) | **PARTIAL** — referenced for cross-checks, not unit-tested directly |
| `evaluation_ontology.json` | `test_evaluator.py` | **PARTIAL** — harness tested but CAP-023/CAP-025 mismatches not caught |
| `goal_ontology` / taxonomy | `test_consistency.py` | **PARTIAL** — consistency checks reference taxonomy |
| Schema validation | `test_consistency.py`, `test_graph.py` | **PARTIAL** — graph integrity and consistency tested |
| Evaluation name → cap_id matching | **None** | **NOT COVERED** |
| P0 coverage enforcement | **None** | **NOT COVERED** |

**Ontology Coverage Score: ~35%**  
**Key Gap:** No test validates that `evaluation_ontology.json` names match `capability_ontology.json` names. The CAP-023 and CAP-025 mismatches passed through all existing tests undetected.

---

## SECTION 3: Corpus Coverage Analysis

| Corpus Dimension | Test File | Coverage Status |
|-----------------|-----------|------------------|
| Schema compliance per corpus entry | `test_consistency.py` | **PARTIAL** — schema validated |
| Capability ID cross-reference to ontology | `test_consistency.py` | **PARTIAL** |
| P0 capability evaluation gate | **None** | **NOT COVERED** |
| Corpus entry ↔ evaluation ontology mapping | **None** | **NOT COVERED** |
| Domain diversity enforcement | **None** | **NOT COVERED** |
| Risk model completeness per entry | **None** | **NOT COVERED** |

**Corpus Coverage Score: ~30%**  
**Key Gap:** No test verifies that P0 capabilities in corpus entries have corresponding evaluation entries. This is the mechanism that would have caught the CAP-025 deployment gate bypass.

---

## SECTION 4: Recommendation Coverage Analysis

| Recommendation Dimension | Test File | Coverage Status |
|--------------------------|-----------|------------------|
| Basic recommendation output | `test_recommendations.py` | **COVERED** |
| Ranking calibration | `test_ranking_calibrator.py` | **COVERED** |
| Recommendation ↔ corpus alignment | **None** | **NOT COVERED** |
| Recommendation ↔ evaluation status | **None** | **NOT COVERED** |
| P0 capability recommendation priority | **None** | **NOT COVERED** |
| Edge cases (no corpus, empty graph) | `test_recommendations.py` (partial) | **PARTIAL** |

**Recommendation Coverage Score: ~45%**  
**Key Gap:** No test verifies that recommendation engine respects evaluation status. An unevaluated P0 capability should not be recommended as production-ready.

---

## SECTION 5: Overall Coverage Matrix

| Domain | Estimated Coverage | Score |
|--------|--------------------|-------|
| API layer | Good (dedicated test) | ~60% |
| CLI | Good (dedicated test, largest) | ~65% |
| Graph integrity | Good | ~60% |
| Blueprints | Moderate | ~50% |
| Consistency checks | Moderate | ~50% |
| Evaluation harness | Moderate | ~45% |
| Recommendation engine | Moderate | ~45% |
| MCP layer | Moderate | ~40% |
| Ranking calibrator | Moderate | ~40% |
| Security (OSV) | Partial | ~35% |
| Ontology integrity | Low | ~35% |
| Corpus validation | Low | ~30% |
| Badge sync | Minimal | ~25% |
| Changelog | Minimal | ~20% |

**Estimated Overall Coverage: ~42%**  
**Target: ≥70%**  
**Gap: ~28 percentage points**

---

## SECTION 6: Critical Missing Tests

| Priority | Test Description | Target File | Effort |
|----------|-----------------|------------|--------|
| P0 | Evaluation name matches canonical capability name | `test_evaluator.py` or `test_ontology_integrity.py` (new) | 2 hours |
| P0 | P0 corpus capabilities have evaluation mappings | `test_consistency.py` extension | 2 hours |
| P0 | Deployment gate blocks agents without valid P0 evaluations | `test_evaluator.py` extension | 3 hours |
| P1 | Corpus entry ↔ evaluation ontology cross-validation | `test_corpus_evaluation.py` (new) | 4 hours |
| P1 | Recommendation engine respects evaluation status | `test_recommendations.py` extension | 3 hours |
| P1 | Schema validation for evaluation_ontology.json | `test_evaluator.py` extension | 2 hours |
| P2 | Domain diversity enforcement | `test_consistency.py` extension | 2 hours |
| P2 | Risk model completeness | `test_consistency.py` extension | 2 hours |

---

## SECTION 7: Audit Verdict

| Metric | Value |
|--------|-------|
| Total test files | 14 |
| Estimated overall coverage | ~42% |
| Target coverage | ≥70% |
| Coverage gap | ~28 pp |
| Critical untested paths | Ontology name-to-cap_id matching, P0 evaluation gate, corpus-evaluation cross-reference |
| Tests that would have caught Phase 1 defects | 0 (both CAP-023 and CAP-025 mismatches passed all tests) |

**Testing Readiness: BELOW TARGET — 42% vs 70% target. Recovery plan required.**  
See: `TEST_COVERAGE_RECOVERY_PLAN.md` (root)

---

*Generated: 2026-07-05. Evidence: repository state at commit `0752a72afcb2d659dc0219ec1d385840b7e69186`.*
