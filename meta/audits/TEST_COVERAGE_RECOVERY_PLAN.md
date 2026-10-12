# TEST COVERAGE RECOVERY PLAN

**Workstream:** D — Test Coverage Recovery  
**Sprint:** Phase 2 — Repository Maturity Sprint  
**Generated:** 2026-07-05  
**Current Coverage:** ~42%  
**Target Coverage:** ≥70%  
**Status:** APPROVED — PENDING EXECUTION

---

## Objective

Recover test coverage from ~42% to ≥70% through targeted test additions. No new corpus entries. No new ontologies. Tests must validate **existing** code and data artifacts.

---

## Phase 1 — Critical Path (Coverage: 42% → 55%)

Estimated effort: 12 hours  
Blocker: YES — these tests block production deployment readiness

### Task T-001: Ontology Name Integrity Tests

**Target:** `tests/test_evaluator.py` (extend) or new `tests/test_ontology_integrity.py`  
**What to add:**
```python
def test_evaluation_names_match_capability_ontology():
    """Every name in evaluation_ontology must match the canonical name in capability_ontology."""
    # Load both ontologies
    # For each evaluation entry: assert eval['name'] == capability_registry[eval['cap_id']]['name']
    # This test would have caught CAP-023 and CAP-025 mismatches

def test_all_eval_cap_ids_exist_in_capability_ontology():
    """Every cap_id in evaluation_ontology must exist in capability_ontology."""
    # Load both ontologies
    # For each evaluation entry: assert eval['cap_id'] in capability_registry

def test_evaluation_thresholds_are_defined():
    """Every evaluation entry must have a min_required_score or equivalent threshold."""

def test_evaluation_metrics_are_defined():
    """Every evaluation entry must reference at least one metric."""
```
**Estimated coverage gain:** +3%  
**Effort:** 2 hours

---

### Task T-002: P0 Evaluation Gate Tests

**Target:** `tests/test_consistency.py` (extend)  
**What to add:**
```python
def test_all_p0_capabilities_have_evaluations():
    """Every P0 capability in every corpus entry must have an evaluation mapping."""
    # Load all corpus entries
    # Collect P0 cap_ids
    # Assert each P0 cap_id exists in evaluation_ontology
    # Current expected failures: CAP-007, CAP-011, CAP-014
    # This test should be marked xfail until those gaps are closed

def test_safety_tier_capabilities_have_evaluations():
    """Every capability with tier=safety must have a valid evaluation."""
    # CAP-025 pii_detection_and_redaction is safety-tier
    # This test must pass after C-002 correction is applied
```
**Estimated coverage gain:** +4%  
**Effort:** 2 hours

---

### Task T-003: Corpus-Evaluation Cross-Reference Tests

**Target:** New `tests/test_corpus_evaluation.py`  
**What to add:**
```python
def test_corpus_evaluation_cross_reference():
    """For each corpus entry, verify all capabilities reference valid evaluations."""

def test_corpus_entry_schema_compliance():
    """All corpus entries comply with corpus JSON schema."""

def test_corpus_capability_ids_in_ontology():
    """All cap_ids in corpus entries exist in capability_ontology."""

def test_p0_evaluation_completeness_per_corpus_entry():
    """Each corpus entry explicitly lists evaluation coverage for P0 capabilities."""
```
**Estimated coverage gain:** +6%  
**Effort:** 4 hours

---

## Phase 2 — Coverage Improvement (Coverage: 55% → 65%)

Estimated effort: 14 hours  
Blocker: NO — required for 70% target but not production gate

### Task T-004: Recommendation Engine Evaluation-Awareness Tests

**Target:** `tests/test_recommendations.py` (extend)  
**What to add:**
- Test that recommendation engine does not rank unevaluated capabilities as production-ready
- Test that evaluation status is reflected in recommendation scores
- Test P0 unmapped capabilities trigger evaluation recommendation

**Estimated coverage gain:** +5%  
**Effort:** 3 hours

### Task T-005: Evaluation Harness Integration Tests

**Target:** `tests/test_evaluator.py` (extend)  
**What to add:**
- Full evaluation run against known test fixtures
- Evaluation threshold enforcement (fail below min_required_score)
- Schema validation for evaluation output JSON
- Safety gate independent test (ET-009 must pass independently)

**Estimated coverage gain:** +5%  
**Effort:** 5 hours

### Task T-006: Graph + Ontology Integration Tests

**Target:** `tests/test_graph.py` (extend)  
**What to add:**
- Test that all capability nodes in graph exist in capability_ontology
- Test that evaluation nodes reference valid capabilities
- Test graph load succeeds after evaluation_ontology update

**Estimated coverage gain:** +3%  
**Effort:** 3 hours

### Task T-007: MCP Layer Evaluation Tests

**Target:** `tests/test_mcp.py` (extend)  
**What to add:**
- MCP tools return evaluation status for capabilities
- MCP evaluation query returns correct coverage percentage
- MCP P0 gap report is accurate

**Estimated coverage gain:** +3%  
**Effort:** 3 hours

---

## Phase 3 — Target Achievement (Coverage: 65% → 70%+)

Estimated effort: 8 hours  
Blocker: NO

### Task T-008: Risk Model and Domain Diversity Tests

**Target:** `tests/test_consistency.py` (extend)  
**What to add:**
- Risk model completeness per corpus entry
- Domain diversity enforcement (at least 2 domains per N entries)
- Corpus entry count adequacy (warn at < 5 entries)

**Estimated coverage gain:** +3%  
**Effort:** 2 hours

### Task T-009: CI Workflow Validation Tests

**Target:** New `tests/test_ci_workflows.py`  
**What to add:**
- All required workflows exist
- validate-evaluations.yml is syntactically valid
- Required checks registered in CI include evaluation validation

**Estimated coverage gain:** +2%  
**Effort:** 2 hours

### Task T-010: Security and Governance Tests

**Target:** `tests/test_osv_check.py` (extend)  
**What to add:**
- CODEOWNERS file exists and is valid
- Dependabot configuration is valid
- Security scan workflow is valid

**Estimated coverage gain:** +2%  
**Effort:** 2 hours

---

## Coverage Projection

| Phase | Tasks | Coverage | Effort |
|-------|-------|----------|--------|
| Baseline | — | ~42% | — |
| Phase 1 | T-001, T-002, T-003 | ~55% | 12h |
| Phase 2 | T-004, T-005, T-006, T-007 | ~65% | 14h |
| Phase 3 | T-008, T-009, T-010 | **~72%** | 8h |
| **Total** | 10 tasks | **≥70%** | **34 hours** |

---

## Execution Order

1. **T-001** — Ontology name integrity (catches existing defects, confirms Phase 1 audit findings)
2. **T-002** — P0 evaluation gate (enforces Phase 2 Workstream B requirements)
3. **T-003** — Corpus-evaluation cross-reference (new test module)
4. **T-005** — Evaluation harness integration (extends existing test_evaluator.py)
5. **T-004** — Recommendation evaluation-awareness
6. **T-006, T-007** — Graph + MCP integration
7. **T-008, T-009, T-010** — Remaining coverage

---

## Success Criteria

- [ ] pytest reports ≥70% line coverage on `make test`
- [ ] T-001 catches CAP-023 and CAP-025 mismatches before production deployment
- [ ] T-002 reports 3 P0 gaps (CAP-007, CAP-011, CAP-014) as expected failures pending evaluation authoring
- [ ] T-003 all corpus entry cross-reference tests pass
- [ ] CI `test-coverage.yml` workflow runs T-001 and T-002 on every PR

---

*Generated: 2026-07-05. Baseline from: meta/audits/TEST_COVERAGE_AUDIT.md.*
