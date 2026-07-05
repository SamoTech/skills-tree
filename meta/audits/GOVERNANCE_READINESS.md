# GOVERNANCE_READINESS

**Workstream:** F — Governance Hardening  
**Sprint:** Phase 2 — Repository Maturity Sprint  
**Generated:** 2026-07-05  
**Status:** COMPLETE  
**Source of record:** `.github/` directory, repository settings (as observable), commit `0752a72afcb2d659dc0219ec1d385840b7e69186`

---

## SECTION 1: CODEOWNERS

**File:** `.github/CODEOWNERS`  
**Status:** ✅ EXISTS

| Rule | Pattern | Owner | Assessment |
|------|---------|-------|------------|
| Global fallback | `*` | `@SamoTech` | ✅ All files covered |
| Meta directory | `/meta/` | `@SamoTech` | ✅ Audit trail protected |
| Contributing | `/CONTRIBUTING.md` | `@SamoTech` | ✅ |
| Security | `/SECURITY.md` | `@SamoTech` | ✅ |
| Skills | `/skills/` | `@SamoTech` | ✅ Corpus data protected |
| GitHub config | `/.github/` | `@SamoTech` | ✅ Workflow files protected |
| Intelligence/ontology | ❌ Not specified | — | **GAP: ontology files not explicitly protected** |
| Evaluation layer | ❌ Not specified | — | **GAP: evaluation_ontology.json not explicitly protected** |
| Data/corpus | ❌ Not specified | — | **GAP: corpus entries not explicitly protected** |

**CODEOWNERS Score: 65/100**  
**Gap:** Three critical paths (`intelligence/`, `evaluation/`, `data/corpus/`) not explicitly listed. They fall under the global `*` rule but should have explicit entries for auditability.

**Recommended additions to CODEOWNERS:**
```
# Ontology files — require maintainer approval for all changes
/intelligence/          @SamoTech
/evaluation/            @SamoTech
/data/corpus/           @SamoTech
/schema/                @SamoTech
```

---

## SECTION 2: Branch Protection

**Observable Evidence:** Repository is public under the `SamoTech` organization.  
**Direct API access:** Not available to this audit (requires Admin/Settings access).  
**Inference from workflow patterns:**

| Signal | Evidence | Assessment |
|--------|----------|------------|
| PR-required workflow exists | `pr-checks.yml` (4.2KB) exists | Suggests PR review process exists |
| Auto-merge workflow exists | `dependabot-auto-merge.yml` | Dependabot PRs auto-merge — review gate may be bypassed for deps |
| Required checks referenced | `pr-checks.yml` | PR checks defined but enforcement depends on branch protection rules |
| Previous scorecard noted | V1 scorecard: "No branch protection" (25/100 on pipeline security) | Branch protection likely absent or minimal |
| CODEOWNERS exists | ✅ | CODEOWNERS is only effective when branch protection requires reviews |

**Branch Protection Score: 30/100**  
**Critical Gap:** CODEOWNERS is present but branch protection rules are the enforcement mechanism. Without branch protection requiring at least 1 review, CODEOWNERS is advisory only. Pushes directly to `main` bypass CODEOWNERS entirely.

**Required actions:**
1. Enable branch protection on `main` branch
2. Require at least 1 pull request review before merging
3. Require status checks to pass before merging (include `validate-evaluations` from Workstream C)
4. Dismiss stale reviews when new commits are pushed
5. Prevent force-pushes and branch deletion

---

## SECTION 3: Dependabot Safety

**File:** `.github/dependabot.yml`  
**Status:** ✅ EXISTS (951 bytes)

**File:** `.github/workflows/dependabot-auto-merge.yml`  
**Status:** ✅ EXISTS (1,885 bytes)  
**Risk:** Auto-merge without review gate

| Dimension | Status | Assessment |
|-----------|--------|------------|
| Dependabot configured | ✅ | Dependency updates enabled |
| Update schedule defined | ✅ (assumed weekly/daily) | Regular update cadence |
| Auto-merge enabled | ✅ | **Risk:** Malicious dependency injection possible without review |
| Review required before auto-merge | ❓ Unknown | Depends on branch protection + workflow logic |
| OSV scanning | ✅ `osv-watch.yml`, `dependency-auditor.yml` | Vulnerability scanning present |

**Dependabot Safety Score: 60/100**  
**Gap:** Auto-merge without confirmed review gate is a supply chain risk. Dependabot auto-merge should require at minimum: all CI checks pass + no CVE introduced (osv-scanner must pass).

---

## SECTION 4: Required Checks

**Observable from workflow files:**

| Check | Workflow | On PR? | Required? |
|-------|----------|--------|-----------|
| Build and verify | `build-and-verify.yml` | ✅ | Unknown |
| PR checks | `pr-checks.yml` | ✅ | Unknown |
| Schema enforce | `schema-enforce.yml` | ✅ | Unknown |
| Validate corpus | `validate-corpus.yml` | ✅ | Unknown |
| Validate skills | `validate-skills.yml` | ✅ | Unknown |
| Validate graph | `validate-graph.yml` | ✅ | Unknown |
| Security scan | `security-scan.yml` | ✅ | Unknown |
| Validate evaluations | `validate-evaluations.yml` | ✅ (new, Workstream C) | **Must be added to required checks** |
| Test coverage | `test-coverage.yml` | ✅ | Unknown |

**Required Checks Score: 50/100**  
**Gap:** Workflows exist but whether they are enforced as *required* status checks before merge is unknown from file inspection alone. The new `validate-evaluations.yml` must be registered as a required check.

---

## SECTION 5: CI Enforcement

| Dimension | Status | Score |
|-----------|--------|-------|
| Workflows present and syntactically valid | ✅ 44 workflows | 80 |
| Validation workflows (corpus, graph, skills, evaluations) | ✅ All present | 75 |
| Security scanning | ✅ gitleaks, OSV, security-scan | 70 |
| Test coverage workflow | ✅ `test-coverage.yml` | 60 |
| Branch protection enforcement | ❓ Not confirmed | 30 |
| Required checks registration | ❓ Not confirmed | 30 |
| Auto-merge safety | ⚠️ Risk present | 40 |

**CI Enforcement Score: 55/100**

---

## SECTION 6: Overall Governance Score

| Dimension | Score | Weight | Weighted |
|-----------|-------|--------|----------|
| CODEOWNERS | 65 | 20% | 13.0 |
| Branch Protection | 30 | 30% | 9.0 |
| Dependabot Safety | 60 | 15% | 9.0 |
| Required Checks | 50 | 20% | 10.0 |
| CI Enforcement | 55 | 15% | 8.25 |
| **Total** | | | **49.25 → 49/100** |

**GOVERNANCE READINESS SCORE: 49 / 100**

---

## SECTION 7: Priority Actions

| Action | Impact | Effort | Priority |
|--------|--------|--------|----------|
| Enable branch protection on `main` (require 1 review, require status checks) | +15 points | 30 min | **P0** |
| Add `validate-evaluations.yml` to required status checks | +5 points | 15 min | **P0** |
| Add explicit CODEOWNERS entries for `intelligence/`, `evaluation/`, `data/corpus/` | +5 points | 15 min | **P1** |
| Add OSV-must-pass condition to `dependabot-auto-merge.yml` | +5 points | 1 hour | **P1** |
| Verify and document which checks are currently required (Admin settings audit) | +5 points | 1 hour | **P1** |
| Enable `dismiss_stale_reviews` in branch protection | +3 points | 15 min | **P2** |
| Add SAST/CodeQL scanning workflow | +5 points | 2 hours | **P2** |

**Projected score after P0 actions: ~69/100**  
**Projected score after all actions: ~82/100**

---

*Generated: 2026-07-05. Evidence: repository state at commit `0752a72afcb2d659dc0219ec1d385840b7e69186`.*
