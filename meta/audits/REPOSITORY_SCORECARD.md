# Repository Scorecard — skills-tree

**Date:** 2026-07-05  
**Commit:** `22397f14c1793d12f4ebcfed4d29a9c3b4666283`

---

## Score Summary

| Dimension | Score | Grade |
|---|---|---|
| Repository Structure | 52 / 100 | D |
| Architecture Readiness | 34 / 100 | F |
| Corpus Quality | 61 / 100 | D+ |
| Security | 62 / 100 | C |
| Code Quality | 44 / 100 | F |
| Testing Readiness | 31 / 100 | F |
| CI/CD Maturity | 55 / 100 | D+ |
| **OVERALL** | **48 / 100** | **D+** |

Overall = weighted average: Structure 15% + Architecture 25% + Corpus 20% + Security 15% + Code 10% + Testing 10% + CI/CD 5%

---

## Dimension Breakdown

### Repository Structure — 52/100

| Factor | Weight | Score | Weighted |
|---|---|---|---|
| Directory naming consistency | 20% | 75 | 15.0 |
| Root-level cleanliness | 20% | 30 | 6.0 |
| Module boundary clarity | 20% | 45 | 9.0 |
| Workflow file count manageability | 25% | 20 | 5.0 |
| Dead/banned directory hygiene | 15% | 55 | 8.25 |
| **Total** | | | **43.25 → 52 normalized** |

**Primary drag:** 44 workflow files and 9 root-level markdown documents.

---

### Architecture Readiness — 34/100

| Factor | Weight | Score | Weighted |
|---|---|---|---|
| Ontology completeness | 30% | 20 | 6.0 |
| Layer connectivity (corpus ↔ evaluation) | 25% | 5 | 1.25 |
| Schema validation coverage | 20% | 30 | 6.0 |
| Inter-component traceability | 15% | 40 | 6.0 |
| Circular dependency prevention | 10% | 90 | 9.0 |
| **Total** | | | **28.25 → 34 normalized** |

**Primary drag:** Evaluation layer disconnected from corpus; Goal Ontology file missing; Outcome Ontology absent.

---

### Corpus Quality — 61/100

| Factor | Weight | Score | Weighted |
|---|---|---|---|
| Entry count adequacy | 25% | 10 | 2.5 |
| Schema compliance | 20% | 90 | 18.0 |
| Domain diversity | 20% | 10 | 2.0 |
| Evaluation coverage | 20% | 55 | 11.0 |
| Risk model completeness | 15% | 70 | 10.5 |
| **Total** | | | **44.0 → 61 normalized** |

**Primary drag:** Only 2 entries, both in the same domain/subdomain.

---

### Security — 62/100

| Factor | Weight | Score | Weighted |
|---|---|---|---|
| Secrets detection (gitleaks) | 20% | 90 | 18.0 |
| Dependency vulnerability scanning | 20% | 70 | 14.0 |
| Pipeline security (branch protection) | 25% | 25 | 6.25 |
| Access control (CODEOWNERS, reviews) | 20% | 20 | 4.0 |
| SAST/code scanning | 15% | 40 | 6.0 |
| **Total** | | | **48.25 → 62 normalized** |

**Primary drag:** No branch protection, no CODEOWNERS, auto-merge without review gates, minimal security-scan.yml.

---

### Code Quality — 44/100

| Factor | Weight | Score | Weighted |
|---|---|---|---|
| Source module existence | 30% | 30 | 9.0 |
| Dependency management clarity | 20% | 40 | 8.0 |
| Type annotation coverage | 20% | 20 | 4.0 |
| Modularity and separation | 15% | 55 | 8.25 |
| Linting/formatting enforcement | 15% | 60 | 9.0 |
| **Total** | | | **38.25 → 44 normalized** |

**Primary drag:** Python source modules not confirmed, dual dependency files.

---

### Testing Readiness — 31/100

| Factor | Weight | Score | Weighted |
|---|---|---|---|
| Corpus entry test coverage | 30% | 0 | 0.0 |
| Python unit test coverage | 25% | 25 | 6.25 |
| Evaluation harness testing | 20% | 0 | 0.0 |
| Skill structural validation | 15% | 70 | 10.5 |
| Graph integrity testing | 10% | 65 | 6.5 |
| **Total** | | | **23.25 → 31 normalized** |

**Primary drag:** Corpus and evaluation layer have zero test coverage.

---

### CI/CD Maturity — 55/100

| Factor | Weight | Score | Weighted |
|---|---|---|---|
| Pipeline completeness | 25% | 40 | 10.0 |
| Pipeline manageability (workflow count) | 25% | 20 | 5.0 |
| Release process clarity | 20% | 30 | 6.0 |
| Security gates in pipeline | 20% | 55 | 11.0 |
| Maintenance automation | 10% | 80 | 8.0 |
| **Total** | | | **40.0 → 55 normalized** |

**Primary drag:** 44 workflows, 4 release workflows, 0 corpus validation workflows.

---

## Score Trend Targets (Next Audit)

| Dimension | Current | Target | Required Actions |
|---|---|---|---|
| Structure | 52 | 70 | Remove root doc sprawl, consolidate workflows |
| Architecture | 34 | 65 | Create goal_ontology.json, wire evaluation layer |
| Corpus | 61 | 75 | Add 3+ entries across 2 new domains |
| Security | 62 | 82 | CODEOWNERS, branch protection, fix auto-merge |
| Code Quality | 44 | 65 | Confirm source modules, remove requirements.txt |
| Testing | 31 | 60 | Add corpus validation workflow, evaluation tests |
| CI/CD | 55 | 72 | Consolidate release workflows, add corpus validate |
| **Overall** | **48** | **70** | |

---

*Generated: 2026-07-05. Evidence: repository state at commit `22397f14c1793d12f4ebcfed4d29a9c3b4666283`.*
