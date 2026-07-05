# Next 10 GitHub Issues — Post-Audit Action Plan

**Source:** Full Repository Audit 2026-07-05  
**Evidence base:** `meta/audits/FULL_REPOSITORY_AUDIT.md`  
**All issues are directly supported by audit findings. No generic issues included.**

---

## Issue 1 — P0

**Title:** `[security] dependabot-auto-merge.yml must require passing CI and manual label before merge`

**Priority:** P0 — Critical  
**Audit source:** Step 5, Finding #1

**Description:**  
`.github/workflows/dependabot-auto-merge.yml` (1,885 bytes) automatically merges Dependabot pull requests. If this workflow does not require all status checks to pass AND a human-applied `safe-to-merge` label before executing the merge, it is a supply chain attack vector. A compromised dependency version published to PyPI or npm could be automatically merged into `main` without any human review.

**Acceptance Criteria:**
- [ ] Workflow requires ALL required status checks to pass before merge executes
- [ ] Workflow requires a `safe-to-merge` label (applied only by maintainer) OR requires Dependabot PRs to pass `security-scan.yml` and `dependency-auditor.yml` first
- [ ] `auto-merge` is scoped to `patch` and `minor` version bumps only — never `major`
- [ ] A comment is posted to the PR summarizing what was auto-merged and why
- [ ] Manual merge remains available if automation is blocked

---

## Issue 2 — P0

**Title:** `[corpus] add validate-corpus.yml — JSON schema validation for all corpus entries in CI`

**Priority:** P0 — Critical  
**Audit source:** Step 8, Finding #2; Step 7, Finding #1

**Description:**  
44 CI workflows exist in this repository. Zero of them validate `intelligence/corpus/entries/**/*.json`. Corpus entries are the primary active work product of the repository's current priority phase. Without CI validation, entries can drift from schema, reference undefined CAP-IDs, or omit required fields with no automated detection.

**Acceptance Criteria:**
- [ ] New workflow file at `.github/workflows/validate-corpus.yml`
- [ ] Triggers on: `push` and `pull_request` targeting any file under `intelligence/corpus/entries/`
- [ ] Validates each `.json` entry against `schema/corpus-entry.schema.json` (or the confirmed schema path)
- [ ] Validates that all `capability_id` values referenced in entries exist in `capability_ontology.json`
- [ ] Workflow fails with a clear error message identifying the invalid entry and the field that failed
- [ ] Workflow passes on both CORPUS-001.json and CORPUS-002.json without changes to those files

---

## Issue 3 — P0

**Title:** `[ontology] create intelligence/ontologies/goal_ontology.json — formal authority file for goal_class values`

**Priority:** P0 — Critical  
**Audit source:** Step 3, Finding #4

**Description:**  
Corpus entries reference a `goal_class` field (e.g., `reactive_agent`, `proactive_agent`). No formal `goal_ontology.json` file exists to define the valid set of goal classes, their hierarchy, properties, and definitions. This means the `goal_class` field in every corpus entry is validated only by convention, not by machine-readable authority.

**Acceptance Criteria:**
- [ ] File created at `intelligence/ontologies/goal_ontology.json`
- [ ] Defines at minimum: `reactive_agent`, `proactive_agent`, `orchestrator`, `planner`, `critic`, `evaluator`, `retriever`, `tool_agent`
- [ ] Each goal class entry contains: `id`, `name`, `description`, `characteristic_capabilities` (array of CAP-IDs), `typical_domains`
- [ ] `validate-corpus.yml` (Issue 2) validates corpus `goal_class` values against this file
- [ ] CORPUS-001 (`proactive_agent`) and CORPUS-002 (`reactive_agent`) both pass validation

---

## Issue 4 — P0

**Title:** `[security] create .github/CODEOWNERS — enforce reviewer assignment on sensitive paths`

**Priority:** P0 — High  
**Audit source:** Step 5, Finding #3

**Description:**  
No `CODEOWNERS` file exists. Without it, changes to security-sensitive paths (`.github/workflows/`, `schema/`, `intelligence/corpus/`, `pyproject.toml`, `requirements.txt`) receive no automatic reviewer assignment. This is a prerequisite for effective branch protection.

**Acceptance Criteria:**
- [ ] File created at `.github/CODEOWNERS`
- [ ] `@SamoTech` is owner of: `intelligence/corpus/` `intelligence/ontologies/` `schema/` `.github/workflows/` `pyproject.toml` `requirements.txt` `SECURITY.md`
- [ ] All other paths have a default owner fallback
- [ ] CODEOWNERS file is syntactically valid (no rule errors)
- [ ] After creation, a test PR to `intelligence/corpus/` automatically requests review from `@SamoTech`

---

## Issue 5 — P1

**Title:** `[ci] consolidate 4 release workflows into 1 authoritative release pipeline`

**Priority:** P1 — High  
**Audit source:** Step 8, Finding #3

**Description:**  
Four workflows govern or overlap with the release process: `release.yml` (2,086 bytes), `release-package.yml` (5,651 bytes), `semantic-release.yml` (955 bytes), `zero-touch-release.yml` (9,924 bytes). There is no documentation identifying which is the authoritative release workflow. This creates a risk of double-releases, conflicting version tags, and untraceable release failures.

**Acceptance Criteria:**
- [ ] Audit of all 4 release workflows to determine which is currently active and correct
- [ ] Single authoritative release workflow identified and documented in `meta/CI_ARCHITECTURE.md`
- [ ] All non-authoritative release workflows either deleted or converted to reusable workflows called by the authoritative one
- [ ] At most 1 file triggers a PyPI publish or GitHub Release creation
- [ ] Reduced to ≤2 release-related workflow files total
- [ ] A test release (dry-run or pre-release) confirms the consolidated pipeline produces a correct release artifact

---

## Issue 6 — P1

**Title:** `[security] expand security-scan.yml — add bandit SAST, SARIF output, and failure threshold`

**Priority:** P1 — High  
**Audit source:** Step 5, Finding #2

**Description:**  
`security-scan.yml` is 786 bytes — the smallest security workflow in the repository, yet one of the most important. It provides false confidence that security scanning is active when the actual scanning depth is likely a single command with no thresholds, no SARIF artifact upload, and no PR blocking on findings.

**Acceptance Criteria:**
- [ ] Add `bandit -r . -ll` (medium severity and above) with `-o bandit-results.sarif -f sarif` output format
- [ ] Upload SARIF results to GitHub Security tab via `github/codeql-action/upload-sarif`
- [ ] Workflow fails (non-zero exit) on HIGH or CRITICAL severity findings
- [ ] Workflow reports MEDIUM findings as warnings without failing
- [ ] Results are stored as workflow artifacts for 30 days
- [ ] File size after expansion must be ≥ 2,000 bytes (evidence of substantive content)

---

## Issue 7 — P1

**Title:** `[ontology] create intelligence/ontologies/outcome_ontology.json — P3 priority item from execution protocol`

**Priority:** P1 — High  
**Audit source:** Step 3, Finding #5; current execution priority order

**Description:**  
The current execution priority order lists Outcome Ontology as the 3rd priority after Goal Ontology and Capability Ontology. No `outcome_ontology.json` or equivalent file exists. Corpus entries do not have an `outcome_class` or `expected_outcomes` field because the ontology that would define valid outcomes does not exist.

**Acceptance Criteria:**
- [ ] File created at `intelligence/ontologies/outcome_ontology.json`
- [ ] Defines at minimum 10 outcome classes covering: task_completion, decision_output, recommendation, artifact_generation, classification, retrieval_result, plan, evaluation_report, error_state, escalation
- [ ] Each outcome class contains: `id`, `name`, `description`, `measurable_criteria`, `typical_goal_classes` (array referencing goal_ontology IDs)
- [ ] Schema for outcome_ontology.json is added to `schema/`
- [ ] `validate-corpus.yml` is updated to optionally validate `outcome_class` fields in corpus entries if present

---

## Issue 8 — P1

**Title:** `[deps] remove requirements.txt — consolidate all Python dependencies into pyproject.toml`

**Priority:** P1 — Medium  
**Audit source:** Step 5, Finding #5; Step 6, Finding #2

**Description:**  
Both `requirements.txt` (228 bytes) and `pyproject.toml` (4,396 bytes) define Python dependencies. This dual-source pattern creates non-deterministic dependency resolution: `pip install -r requirements.txt` may install different versions than `pip install -e .`. The `requirements.txt` pattern is a legacy artifact that conflicts with the modern `pyproject.toml` standard the repository has adopted.

**Acceptance Criteria:**
- [ ] All packages listed in `requirements.txt` are present in `pyproject.toml` under `[project.dependencies]` or `[project.optional-dependencies]`
- [ ] `requirements.txt` is deleted from the repository root
- [ ] All workflow files that reference `requirements.txt` (e.g., `pip install -r requirements.txt`) are updated to use `pip install -e .` or `pip install -e ".[dev]"`
- [ ] `clean-install-test.yml` passes after the change
- [ ] No workflow references `requirements.txt` after the change

---

## Issue 9 — P1

**Title:** `[structure] move PROJECT_MEMORY.md and EXECUTION_STATUS.md from root to meta/state/`

**Priority:** P1 — Medium  
**Audit source:** Step 2, Finding #1; Step 2, Finding #6

**Description:**  
Two large operational state files exist at the repository root: `PROJECT_MEMORY.md` (48,049 bytes) and `EXECUTION_STATUS.md` (4,382 bytes). The repository root should contain only: `README.md`, `LICENSE`, `CHANGELOG.md`, `CONTRIBUTING.md`. Operational state documents belong under `meta/state/`. Their presence at root pollutes the first impression of the repository for new contributors and consumers.

**Acceptance Criteria:**
- [ ] `PROJECT_MEMORY.md` moved to `meta/state/PROJECT_MEMORY.md`
- [ ] `EXECUTION_STATUS.md` moved to `meta/state/EXECUTION_STATUS.md`
- [ ] `README.md` updated if it links to either file at root path
- [ ] Any workflow that reads or writes either file is updated with the new path
- [ ] Root directory contains ≤6 markdown files after the move: `README.md`, `CHANGELOG.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`, `QUICKSTART.md`

---

## Issue 10 — P2

**Title:** `[hygiene] relabel issues #86–#91: remove incorrect 'bug' label, close #86 as not-planned`

**Priority:** P2 — Low  
**Audit source:** Step 1, Issue Health

**Description:**  
All 5 open issues (#86, #87, #88, #90, #91) carry the `bug` label. None of them describe bugs. Issues #87, #88, #90, #91 are enhancement/feature requests for stub expansion and new skills. Issue #86 (CLI implementation) contradicts the current execution protocol which explicitly bans CLI tool additions as a secondary priority. The corrupted `bug` labeling pollutes triage and inflates the apparent critical issue count.

**Acceptance Criteria:**
- [ ] Issue #86: Closed with state_reason `not_planned`; comment added referencing current execution protocol priority order
- [ ] Issues #87, #88, #90, #91: `bug` label removed; `enhancement` label confirmed present
- [ ] Issue #87 and #88: `help wanted` label confirmed
- [ ] Issue #91: Body cleaned of pasted raw `gh --help` output noise (or issue closed as misformatted and replaced with a clean version)
- [ ] After relabeling: open `bug`-labeled issues = 0
- [ ] After closing #86: open issues = 4

---

*All 10 issues derived directly from audit evidence in `meta/audits/FULL_REPOSITORY_AUDIT.md`. No speculative or generic issues included.*
