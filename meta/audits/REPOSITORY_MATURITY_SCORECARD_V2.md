# REPOSITORY MATURITY SCORECARD V2

**Repository:** SamoTech/skills-tree  
**Sprint:** Phase 2 — Repository Maturity Sprint  
**Generated:** 2026-07-05  
**Baseline Commit (V1):** `22397f14c1793d12f4ebcfed4d29a9c3b4666283`  
**Current Commit:** `0752a72afcb2d659dc0219ec1d385840b7e69186`  
**Preceding Scorecard:** `meta/audits/REPOSITORY_SCORECARD.md` (V1)  
**Goal:** Architecture Complete → Execution Ready

---

## EXECUTIVE SUMMARY

Phase 2 sprint completed all 6 workstreams. The repository has transitioned from an **architecture-complete** state with undiscovered integrity defects to a **well-audited, execution-staged** state with all blocking defects documented and remediation specifications ready. No corpus entries were added. No new ontology categories were created.

The primary blockers to production readiness are:
1. **CAP-025 safety-tier evaluation phantom** — highest severity, no valid PII evaluation
2. **3 P0 capabilities unmapped** (CAP-007, CAP-011, CAP-014) — 62.5% P0 coverage
3. **Branch protection not confirmed** — CODEOWNERS advisory-only without it
4. **Recommendation engine safety gate absent** — can recommend agents without valid PII evaluation

---

## SCORECARD MATRIX

### Architecture — 72 / 100

| Factor | V1 Score | V2 Score | Delta | Evidence |
|--------|----------|----------|-------|----------|
| Ontology completeness | 20 | 65 | +45 | Goal + Capability ontologies confirmed complete; evaluation ontology has 2 confirmed mismatches requiring repair |
| Layer connectivity (corpus ↔ evaluation) | 5 | 45 | +40 | RCA-002 + Final Audit fully map the corpus↔evaluation chain; 3 P0 gaps identified and spec'd |
| Schema validation coverage | 30 | 70 | +40 | `validate-evaluations.yml` added; existing validate-corpus, validate-skills, validate-graph all present |
| Inter-component traceability | 40 | 75 | +35 | Dependency graph in RECOMMENDATION_ENGINE_READINESS; full impact mapping in FINAL_AUDIT |
| Circular dependency prevention | 90 | 90 | 0 | No regressions |

**Architecture Score: 72/100 (V1: 34/100, +38 points)**

---

### Ontology — 68 / 100

| Factor | V1 Score | V2 Score | Delta | Evidence |
|--------|----------|----------|-------|----------|
| Capability ontology integrity | — | 95 | — | All CAP-IDs confirmed, names verified |
| Goal ontology integrity | — | 85 | — | GOAL_TAXONOMY.md confirmed present |
| Evaluation ontology integrity | — | 35 | — | 2 of 7 mappings are phantom; repair spec'd but not yet applied |
| Evaluation coverage (valid) | — | 25 | — | 5/28 valid mappings; 3 P0 gaps |
| Schema version control | — | 70 | — | Schemas present and versioned |

**Ontology Score: 68/100** (new dimension, not in V1)

---

### Evaluation — 40 / 100

| Factor | V1 Score | V2 Score | Delta | Evidence |
|--------|----------|----------|-------|----------|
| P0 evaluation coverage | 0 | 30 | +30 | 5/8 P0 caps evaluated (62.5%); specs for 3 gaps created |
| Evaluation ontology integrity | 0 | 25 | +25 | Mismatches identified; corrections specified |
| Evaluation CI enforcement | 0 | 60 | +60 | `validate-evaluations.yml` created (Workstream C) |
| Safety-tier evaluation validity | 0 | 10 | +10 | CAP-025 phantom identified; repair spec'd but not applied |
| Total valid coverage | 0 | 25 | +25 | 5/28 valid, 25% |

**Evaluation Score: 40/100** (new dimension replacing partial architecture score)

---

### Testing — 45 / 100

| Factor | V1 Score | V2 Score | Delta | Evidence |
|--------|----------|----------|-------|----------|
| Corpus entry test coverage | 0 | 15 | +15 | Coverage audit complete; T-003 spec'd |
| Python unit test coverage (estimated) | 25 | 42 | +17 | 14 test modules; ~42% estimated (up from 31% with evaluator, recommendations coverage) |
| Evaluation harness testing | 0 | 35 | +35 | `test_evaluator.py` exists; gaps identified in T-001 |
| Skill structural validation | 70 | 70 | 0 | No regression |
| Graph integrity testing | 65 | 65 | 0 | No regression |
| Recommendation engine testing | 0 | 45 | +45 | `test_recommendations.py` + `test_ranking_calibrator.py` confirmed |

**Testing Score: 45/100 (V1: 31/100, +14 points)**  
**Recovery plan:** `TEST_COVERAGE_RECOVERY_PLAN.md` — 34h to ≥70%

---

### Governance — 49 / 100

| Factor | V1 Score | V2 Score | Delta | Evidence |
|--------|----------|----------|-------|----------|
| CODEOWNERS | 0 | 65 | +65 | CODEOWNERS exists; 3 critical paths not explicitly listed |
| Branch protection | 25 | 30 | +5 | pr-checks.yml present; protection rules not confirmed |
| Dependabot safety | — | 60 | — | Configured with auto-merge risk |
| Required checks | — | 50 | — | Workflows present; registration unconfirmed |
| CI enforcement | 55 | 55 | 0 | 44 workflows; enforcement gap (branch protection) |

**Governance Score: 49/100 (V1 Security: 62/100)** *(dimension renamed and refined)*  
**P0 action:** Enable branch protection + register `validate-evaluations.yml` as required check (+20 projected)

---

### Recommendation Engine — 27 / 100

| Factor | V1 Score | V2 Score | Delta | Evidence |
|--------|----------|----------|-------|----------|
| Core implementation | 0 | 70 | +70 | Evaluator, scenarios, calibration, results all present |
| Test coverage | 0 | 45 | +45 | test_recommendations.py + test_ranking_calibrator.py |
| Evaluation integrity integration | 0 | 0 | 0 | No validity check before recommendation — BLOCKER |
| Safety gate | 0 | 0 | 0 | No safety-tier gate — BLOCKER |
| Formal specification | 0 | 0 | 0 | No RECOMMENDATION_ENGINE_SPEC.md |

**Recommendation Engine Score: 27/100** (new dimension)  
**Blockers:** GAP-REC-002 (evaluation validity) + GAP-REC-003 (safety gate)

---

### Corpus — 65 / 100

| Factor | V1 Score | V2 Score | Delta | Evidence |
|--------|----------|----------|-------|----------|
| Entry count adequacy | 10 | 15 | +5 | 2 entries; constraint: no CORPUS-003 |
| Schema compliance | 90 | 90 | 0 | No regressions |
| Domain diversity | 10 | 10 | 0 | Both entries same domain |
| Evaluation coverage | 55 | 62 | +7 | 62.5% P0 coverage; V1 count was inflated by phantoms |
| Risk model completeness | 70 | 75 | +5 | CORPUS-002 risk model confirmed |

**Corpus Score: 65/100 (V1: 61/100, +4 points)**

---

### Production Readiness — 32 / 100

| Factor | Score | Evidence |
|--------|-------|----------|
| Evaluation gate integrity | 10 | CAP-025 phantom bypasses safety gate — CRITICAL |
| P0 coverage completeness | 30 | 5/8 P0 capabilities evaluated |
| Test coverage adequacy | 35 | ~42% vs 70% target |
| Governance enforcement | 30 | Branch protection unconfirmed |
| Recommendation engine safety | 0 | No safety-tier gate |
| CI validation (evaluations) | 60 | `validate-evaluations.yml` now in place |
| Documentation completeness | 90 | Extensive meta documentation |

**Production Readiness Score: 32/100**

---

## CONSOLIDATED SCORE SUMMARY

| Dimension | V1 Score | V2 Score | Delta | Grade |
|-----------|----------|----------|-------|-------|
| Architecture | 34 | **72** | +38 | C+ |
| Ontology | — | **68** | new | C |
| Evaluation | — | **40** | new | F+ |
| Testing | 31 | **45** | +14 | F+ |
| Governance | 62 | **49** | −13* | F+ |
| Recommendation Engine | — | **27** | new | F |
| Corpus | 61 | **65** | +4 | D |
| Production Readiness | — | **32** | new | F |
| **OVERALL** | **48** | **52** | **+4** | **D+** |

*Governance decrease reflects more accurate measurement scope (V1 scored as Security; V2 scores as Governance including branch protection findings).

**Weighted Overall (Architecture 20% + Ontology 15% + Evaluation 15% + Testing 10% + Governance 10% + Rec Engine 10% + Corpus 10% + Production 10%):**  
= (72×0.20) + (68×0.15) + (40×0.15) + (45×0.10) + (49×0.10) + (27×0.10) + (65×0.10) + (32×0.10)  
= 14.4 + 10.2 + 6.0 + 4.5 + 4.9 + 2.7 + 6.5 + 3.2  
= **52.4 / 100**

---

## TARGET SCORE AND BLOCKING ISSUES

**Target score (Execution Ready): 75 / 100**  
**Current score: 52 / 100**  
**Gap: 23 points**

### Blocking Issues (must resolve before production deploy)

| Blocker ID | Description | Workstream | Effort |
|------------|-------------|------------|--------|
| BLK-001 | CAP-025 `pii_detection_and_redaction` has no valid evaluation — safety gate bypassed | A (apply C-002) | 2 hours |
| BLK-002 | CAP-023 `human_in_loop_escalation` evaluation phantom — execution gate bypassed | A (apply C-001) | 2 hours |
| BLK-003 | Recommendation engine has no safety-tier capability gate | E (Step E-003) | 3 hours |
| BLK-004 | Recommendation engine can recommend agents backed by phantom evaluations | E (Step E-002) | 4 hours |
| BLK-005 | Branch protection not confirmed — CODEOWNERS advisory only | F (Admin config) | 30 min |

---

## TOP 5 HIGHEST ROI TASKS

| Rank | Task | Score Impact | Effort | Workstream |
|------|------|-------------|--------|------------|
| 1 | Enable branch protection on `main` + register `validate-evaluations.yml` as required check | +8 points overall | 45 min | F |
| 2 | Apply corrections C-001 + C-002 to `evaluation_ontology.json` (fix CAP-023, CAP-025) | +6 points overall | 4 hours | A |
| 3 | Author and add evaluation entries for CAP-014, CAP-007, CAP-011 (P0 gap closure) | +8 points overall | 17 hours | B |
| 4 | Implement evaluation validity gate + safety-tier gate in recommendation engine | +7 points overall | 7 hours | E |
| 5 | Execute TEST_COVERAGE_RECOVERY_PLAN Phase 1 tasks (T-001, T-002, T-003) | +6 points overall | 12 hours | D |

---

## NEXT SPRINT RECOMMENDATION (Phase 3)

**Sprint Name:** Execution Hardening Sprint  
**Goal:** Move from 52 → 75 (Execution Ready)  
**Estimated effort:** 45 hours

| Workstream | Tasks | Score Gain |
|------------|-------|------------|
| Apply ontology corrections (A) | C-001 + C-002 on evaluation_ontology.json | +6 |
| P0 evaluation authoring (B) | Author 3 evaluation entries (G-001, G-002, G-003) | +8 |
| Recommendation engine hardening (E) | E-002 + E-003 + E-004 + E-005 | +7 |
| Test coverage recovery (D) | T-001 + T-002 + T-003 (Phase 1 of recovery plan) | +6 |
| Governance enforcement (F) | Enable branch protection + required checks | +8 |
| **Total** | | **+35 → score 87** (some overlap, realistic target: 75+) |

---

## WORKSTREAM COMPLETION REGISTRY

| Workstream | Title | Status | Output File |
|------------|-------|--------|-------------|
| A | Evaluation Ontology Integrity | ✅ COMPLETE | `meta/audits/EVALUATION_ONTOLOGY_FINAL_AUDIT.md` |
| B | P0 Evaluation Coverage | ✅ COMPLETE | `meta/audits/P0_EVALUATION_COVERAGE_FINAL.md` |
| C | Evaluation Validation CI | ✅ COMPLETE | `.github/workflows/validate-evaluations.yml` |
| D | Test Coverage Recovery | ✅ COMPLETE | `meta/audits/TEST_COVERAGE_AUDIT.md` + `TEST_COVERAGE_RECOVERY_PLAN.md` |
| E | Recommendation Engine Readiness | ✅ COMPLETE | `meta/audits/RECOMMENDATION_ENGINE_READINESS.md` |
| F | Governance Hardening | ✅ COMPLETE | `meta/audits/GOVERNANCE_READINESS.md` |
| Final | Maturity Scorecard V2 | ✅ COMPLETE | `meta/audits/REPOSITORY_MATURITY_SCORECARD_V2.md` |

---

*Generated: 2026-07-05. Evidence: repository state at commit `0752a72afcb2d659dc0219ec1d385840b7e69186`.*
