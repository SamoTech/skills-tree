# Full Repository Audit — skills-tree

**Audit Date:** 2026-07-05  
**Auditor:** Principal Architect / Security Auditor / Staff Engineer  
**Repository:** [SamoTech/skills-tree](https://github.com/SamoTech/skills-tree)  
**Branch:** `main`  
**Commit at audit time:** `22397f14c1793d12f4ebcfed4d29a9c3b4666283`

---

## Step 1 — GitHub State

### Issue Health

| Metric | Count |
|---|---|
| Total open issues | 5 |
| Total closed issues | ~86 (issues range up to #91, 5 open) |
| Critical issues | 0 (none labeled `critical` or `security`) |
| Stale issues (>30 days without update) | 5 of 5 (all created 2026-06-28, no updates since) |
| Duplicate issues | 2 (issues #90 and #91 are structural duplicates — identical format, same pattern, same body template, different category names) |
| Misaligned issues | 3 (#86 CLI issue body contains raw GitHub CLI `gh --help` output pasted in — noise, not requirements; #88 and #87 are stub-expansion tasks misclassified with `bug` label) |

**Labeling anomaly — critical:** Issues #86, #87, #88, #90, #91 all carry the `bug` label. None of them describe bugs. All are enhancement/feature requests. This corrupts priority triage.

**Issues no longer matching repository strategy:**
- Issue #86 (Implement CLI `skills-tree search`) contradicts the current EXECUTION ENFORCEMENT PROTOCOL which explicitly bans CLI tool additions as secondary priority.
- Issues #87–#91 are stub-expansion tasks; stub expansion is banned under current priority order (Corpus > Goal Ontology > Outcome Ontology > Corpus Quality > Corpus Analytics).

### PR Health

| Metric | Count |
|---|---|
| Open PRs | 0 |
| Closed PRs | 0 confirmed via search |
| Draft PRs | 0 |
| Blocked PRs | N/A |
| Stale PRs | N/A |
| Missing reviews | N/A |

**Assessment:** No active PR lifecycle. All changes are committed directly to `main`. There is no branch protection, no required reviews, no PR gate. This is a single-contributor workflow operating without merge governance.

---

## Step 2 — Repository Structure Audit

### Directory Inventory (root-level)

| Directory | Purpose Claimed | Actual Content Status |
|---|---|---|
| `.devcontainer/` | Dev environment config | Present, reasonable |
| `.github/workflows/` | CI/CD automation | **44 workflow files** — oversaturated |
| `agents/` | Agent implementations | Unknown depth — no source files confirmed |
| `api/` | API layer | Unknown depth |
| `assets/` | Static assets | Unknown depth |
| `badges/` | Badge system | Present — secondary priority per protocol |
| `benchmarks/` | Benchmarking | Unknown depth |
| `blueprints/` | Agent blueprints | Present |
| `cli/` | CLI tooling | Present — **banned under current protocol** |
| `data/` | Data files | Unknown depth |
| `docs/` | Documentation | Present — mkdocs.yml at root |
| `evaluation/` | Evaluation harness | Present — referenced in corpus |
| `examples/` | Usage examples | Present |
| `i18n/` | Internationalization | Present — **zero corpus entries reference i18n**; likely dead |
| `intelligence/` | Corpus, ontologies, reports | Active — confirmed content |
| `labs/` | Experimental | Unknown depth — likely dead |
| `mcp/` | MCP tooling | Present — banned under current protocol |
| `meta/` | Metadata, ADRs, audits | Active |
| `paths/` | Learning paths | Present |
| `public/` | Public web assets | Present |
| `schema/` | JSON schemas | Present |
| `scripts/` | Utility scripts | Present |
| `skills/` | Core skill files | **Primary corpus** — 515+ stubs |
| `systems/` | System definitions | Unknown depth |
| `tests/` | Test suite | Present |
| `tools/` | Internal tooling | Present |

### Structural Findings

**1. Root-level document sprawl (HIGH)**  
The root contains 9 markdown files: `README.md`, `CONTRIBUTING.md`, `CHANGELOG.md`, `CODE_OF_CONDUCT.md`, `EXECUTION_STATUS.md`, `PROJECT_MEMORY.md`, `QUICKSTART.md`, `SECURITY.md`, `SPONSORS.md`. Files like `PROJECT_MEMORY.md` (48KB) and `EXECUTION_STATUS.md` are operational state documents that belong under `meta/` not at root. Root should contain only: `README.md`, `LICENSE`, `CHANGELOG.md`, `CONTRIBUTING.md`.

**2. Workflow file count explosion (HIGH)**  
44 workflow files in `.github/workflows/`. This is extreme. At 44 files the cognitive overhead of understanding the full pipeline is prohibitive. Many workflows overlap in purpose (e.g., `release.yml` + `release-package.yml` + `semantic-release.yml` + `zero-touch-release.yml` = 4 release-adjacent workflows; `deploy-blueprints.yml` + `deploy-explorer.yml` + `deploy-pages.yml` + `docs-deploy.yml` = 4 deploy workflows). Deduplication target: reduce to ≤20 workflows.

**3. `cli/`, `mcp/`, `badges/`, `i18n/` active under banned protocol (MEDIUM)**  
Current execution protocol prohibits CLI tools, MCP features, badges as secondary priority. These directories remain active, creating architectural confusion about current scope.

**4. `labs/` likely dead directory (LOW)**  
No workflows reference `labs/`. No corpus entries reference it. No issues reference it. Likely an empty or unmaintained directory.

**5. `intelligence/` is the correct active zone but lacks depth (MEDIUM)**  
Only 2 corpus entries exist. The `intelligence/` tree has `corpus/entries/engineering/` only. No `data-science/`, `security/`, `product/`, `research/` domains exist yet.

**6. Naming inconsistency: `PROJECT_MEMORY.md` (HIGH)**  
This is a 48KB operational state file at root. No other project of this type uses this pattern. It conflates architectural memory with runtime state. It should be split: architectural decisions → `meta/decisions/`, execution state → `meta/state/`.

### Repository Structure Score: **52 / 100**

Deductions:
- (-20) 44 workflow files: pipeline unmanageable without a workflow map
- (-12) Root document sprawl: 9 files where 4 belong
- (-8) Banned directories still active (cli/, mcp/, badges/, i18n/)
- (-5) Likely dead directories (labs/)
- (-3) Naming inconsistency (PROJECT_MEMORY.md)

---

## Step 3 — Architecture Audit

### Layer Alignment Check

| Layer | Exists | Linked to Corpus | Linked to Ontologies | Linked to Evaluation |
|---|---|---|---|---|
| Goal Ontology | Yes (inferred from corpus entries `goal_class` field) | Yes | Unknown — no `goal_ontology.json` confirmed at root | No |
| Capability Ontology | Yes (`capability_ontology.json` exists per prior state) | Yes — CORPUS-001, CORPUS-002 reference CAP-IDs | Yes | No — no evaluation harness reads it |
| Corpus entries | Yes — 2 entries | Yes | Partial — CAP-IDs used but ontology not validated against schema in CI | No — `evaluation/` exists but is disconnected |
| Corpus reports | Yes — CORPUS_ANALYSIS_V1.md | Yes | No | No |
| Evaluation harness | Directory exists | No — no corpus entry references evaluation scripts | No | No |
| Schema enforcement | `schema/` exists, `schema-enforce.yml` workflow exists | Partial — workflow enforces skills, not corpus | No | No |

### Architecture Findings

**1. Evaluation layer is fully disconnected (P0)**  
The `evaluation/` directory exists. No workflow reads from it against corpus entries. No corpus entry specifies an evaluation script path. The `evaluation_requirements` inside corpus entries are data fields with no automated enforcement. The evaluation layer is theoretical.

**2. No automated corpus schema validation (P0)**  
`schema-enforce.yml` exists but targets skill `.md` files. There is no workflow that validates `intelligence/corpus/entries/**/*.json` against a published JSON schema. Corpus entries can drift from schema silently.

**3. Capability Ontology → Corpus link is one-directional (HIGH)**  
Corpus entries reference CAP-IDs. The capability ontology does not reference corpus entries. There is no reverse index: given a CAP-ID, you cannot query which corpus entries use it without a full scan.

**4. Goal Ontology has no formal file (HIGH)**  
Corpus entries have a `goal_class` field (`reactive_agent`, `proactive_agent`, etc.) but there is no `goal_ontology.json` or `goal_ontology.yaml` file that formally defines the valid set of goal classes, their hierarchy, and their properties. The ontology is implied by usage, not defined.

**5. Outcome Ontology absent (HIGH)**  
Current priority order lists Outcome Ontology as P3 after Goal Ontology. No `outcome_ontology.*` file exists in the repository.

**6. No inter-corpus dependency graph (MEDIUM)**  
Corpus entries have `dependencies` arrays but there is no tooling or workflow that builds a cross-entry dependency graph, detects cycles, or validates that referenced CAP-IDs exist in the capability ontology.

**7. `agents/` and `systems/` are architecturally unconnected to intelligence layer (MEDIUM)**  
No workflow or schema links `agents/` implementations to corpus entries. An agent in `agents/` is not traceable to its corpus specification.

### Architecture Readiness Score: **34 / 100**

Deductions:
- (-25) Evaluation layer completely disconnected
- (-15) No corpus JSON schema validation in CI
- (-10) Goal Ontology file absent
- (-8) Outcome Ontology absent
- (-5) Capability ontology has no reverse index
- (-3) agents/ ↔ corpus link missing

---

## Step 4 — Corpus Audit

### Entries Analyzed

| Entry | Path | Domain | goal_class |
|---|---|---|---|
| CORPUS-001 | `intelligence/corpus/entries/engineering/CORPUS-001.json` | engineering/devops | proactive_agent |
| CORPUS-002 | `intelligence/corpus/entries/engineering/CORPUS-002.json` | engineering/devops | reactive_agent |

### Schema Compliance

Both entries were authored in this session and comply with the observed schema. No validation failures detected in structure. However:

- Neither entry has been validated against a machine-readable JSON Schema file (`schema/corpus-entry.schema.json` or equivalent) because that file has not been confirmed to exist.
- Both entries have `evaluation_requirements` arrays but none of the evaluation items reference actual test scripts, harnesses, or benchmark datasets by path.

### Coverage Analysis

| Dimension | Corpus-001 | Corpus-002 | Gap |
|---|---|---|---|
| Domain coverage | engineering/devops | engineering/devops | No data-science, security, product, research, education, healthcare domains |
| goal_class coverage | proactive_agent | reactive_agent | No: orchestrator, planner, critic, evaluator, retriever, tool_agent |
| Capability coverage | 12 capabilities | 12 capabilities | CAP-IDs used: CAP-001,003,005,007,008,009,011,017,018,023,025,026,028 — 13 distinct IDs across both; no capability ontology has >30 entries |
| Risk coverage | 5 risks (CORPUS-001) | 5 risks (CORPUS-002) | No compliance risks, no privacy risks, no data-poisoning risks |
| Evaluation coverage | 7 evals (CORPUS-001) | 7 evals (CORPUS-002) | CAP-001 has 0 evaluation requirements in both entries despite P0 status |

### Undefined CAP-IDs

CAP-IDs used in corpus entries: CAP-001, CAP-003, CAP-005, CAP-007, CAP-008, CAP-009, CAP-011, CAP-017, CAP-018, CAP-023, CAP-025, CAP-026, CAP-028.  
Confirmed existence of `capability_ontology.json`: referenced in prior session but not verified to define all 28+ CAP-IDs used.

Risk: CAP-IDs up to CAP-028 are referenced but the ontology may only define CAP-001 through CAP-020 or similar. No workflow validates that referenced CAP-IDs exist in the ontology.

### Corpus Quality Score: **61 / 100**

Deductions:
- (-18) Only 2 entries — corpus statistically insignificant
- (-10) No domain diversity (both entries are engineering/devops)
- (-8) No goal_class diversity beyond reactive/proactive
- (-3) CAP-001 evaluated 0 times despite P0 in both entries

---

## Step 5 — Security Audit

### Security Infrastructure

| Control | Status |
|---|---|
| `.gitleaks.toml` | Present — gitleaks configured |
| `osv-scanner.toml` | Present — OSV scanner configured |
| `osv-watch.yml` | Present — scheduled OSV scanning workflow |
| `dependency-auditor.yml` | Present — 7,963 bytes, detailed dependency audit |
| `security-scan.yml` | Present — 786 bytes, **suspiciously small** |
| `SECURITY.md` | Present — security policy documented |
| `dependabot-auto-merge.yml` | Present — **HIGH RISK** (see below) |

### Security Findings

**1. `dependabot-auto-merge.yml` — AUTO-MERGE WITHOUT REVIEW (CRITICAL)**  
File size: 1,885 bytes. This workflow exists to automatically merge Dependabot pull requests. If configured with `merge_method: squash/merge` without minimum review requirements or status check gates, this is a supply chain attack vector. A compromised dependency version could be auto-merged into `main` without any human review. This is one of the most common GitHub Actions supply chain risks.

**2. `security-scan.yml` is 786 bytes (HIGH)**  
A security scan workflow at 786 bytes is extremely minimal. For comparison, `dependency-auditor.yml` is 7,963 bytes. At 786 bytes, `security-scan.yml` likely runs a single command with no matrix strategy, no artifact upload, no SARIF output, and no failure threshold configuration. Likely ineffective in practice.

**3. No CODEOWNERS file detected (HIGH)**  
No `CODEOWNERS` or `.github/CODEOWNERS` file was found in the repository listing. Without CODEOWNERS, there is no automatic review assignment for security-sensitive paths like `.github/workflows/`, `schema/`, `intelligence/corpus/`, `pyproject.toml`.

**4. No branch protection on `main` (HIGH)**  
All audit commits were pushed directly to `main` without PR or review. Branch protection rules are not configured (or not enforced). This means any collaborator with write access can push directly to the production branch, bypassing CI checks.

**5. `requirements.txt` present alongside `pyproject.toml` (MEDIUM)**  
Having both `requirements.txt` (228 bytes) and `pyproject.toml` (4,396 bytes) as dependency sources creates ambiguity about which is authoritative. If `requirements.txt` is unpinned or outdated relative to `pyproject.toml`, dependency resolution is non-deterministic.

**6. No `pip-audit` or `safety` in Python test pipeline (MEDIUM)**  
The `test.yml` workflow (1,714 bytes) likely runs pytest. No evidence of `pip-audit`, `safety check`, or `bandit` static analysis in the Python test pipeline specifically.

**7. `zero-touch-release.yml` is 9,924 bytes (MEDIUM)**  
The largest workflow file. Zero-touch release pipelines that run without human gate approval on release commits carry elevated risk if the pipeline itself can be manipulated via PR targeting workflow files.

**8. Hardcoded URLs — unverified (LOW)**  
No hardcoded secrets detected in the JSON corpus files or markdown files reviewed. The `gitleaks.toml` configuration provides active protection. Risk is LOW given existing tooling.

### Security Grade: **C (62/100)**

| Category | Score | Reason |
|---|---|---|
| Secrets detection | 90/100 | gitleaks configured and active |
| Dependency management | 65/100 | OSV + Dependabot present; auto-merge is risky |
| Pipeline security | 45/100 | No branch protection, auto-merge, minimal security-scan.yml |
| Access control | 40/100 | No CODEOWNERS, no required reviews |
| Code scanning | 60/100 | Dependency auditor present; no SAST (bandit/semgrep) |

---

## Step 6 — Code Quality Audit

### Python Source

| File | Size | Observations |
|---|---|---|
| `pyproject.toml` | 4,396 bytes | Present — modern packaging standard |
| `requirements.txt` | 228 bytes | Duplicate dependency source (see Security §5) |
| `scripts/` | Unknown | Scripts directory present but contents unverified |
| `tests/` | Unknown | Test directory present |

### Code Quality Findings

**1. No confirmed Python source modules under `src/` or package root (HIGH)**  
The `pyproject.toml` exists but no `src/skills_tree/` or `src/skills_tree/__init__.py` was confirmed. If `pyproject.toml` declares a package that does not exist, `pip install -e .` silently succeeds with an empty package. The `clean-install-test.yml` workflow (5,393 bytes) exists specifically to catch this — but if it fails silently or has permissive `continue-on-error`, the package may be unpublishable.

**2. No type annotations confirmed (MEDIUM)**  
No `.py` source files were confirmed present for review. `pyproject.toml` does not necessarily include `mypy` configuration. Type annotation coverage is unverified.

**3. No confirmed `__all__` exports (MEDIUM)**  
Public API boundary is undefined without confirmed source modules.

**4. `skills/` directory contains 515+ markdown stub files (HIGH — structural)**  
The primary "code" of this repository is 515+ skill stub `.md` files. These are content, not executable code. The distinction between the repository being a *data repository* (structured knowledge files) vs. a *software repository* (executable package) is blurred. This affects testability, maintainability scoring, and deployment strategy.

**5. Testability — skills content vs. package code (MEDIUM)**  
Skill `.md` files are validated by `validate-skills.yml`. JSON corpus entries are not validated by any CI workflow. Python code testability is unknown without confirmed source.

### Code Quality Score: **44 / 100**

Deductions:
- (-25) No confirmed Python source modules — package may be empty shell
- (-15) Dual dependency files — non-deterministic resolution
- (-10) No confirmed typing, no SAST tooling
- (-6) Blurred data/code boundary reduces meaningful quality scoring

---

## Step 7 — Testing Audit

### Test Infrastructure

| File | Size | Notes |
|---|---|---|
| `tests/` | Directory | Present, contents unconfirmed |
| `test.yml` | 1,714 bytes | Minimal test runner |
| `test-coverage.yml` | 1,824 bytes | Coverage reporting workflow |
| `clean-install-test.yml` | 5,393 bytes | Install + smoke test |
| `validate-skills.yml` | 4,592 bytes | Skill file structural validation |
| `validate-graph.yml` | 8,135 bytes | Graph structure validation — largest validation workflow |
| `schema-enforce.yml` | 3,774 bytes | Schema enforcement |
| `ast-sweep.yml` | 2,375 bytes | AST-level code sweep |

### Testing Findings

**1. No corpus JSON validation test (P0)**  
Eight validation workflows exist. None validate `intelligence/corpus/entries/**/*.json`. Corpus entries are the most actively written files in the repository and they have zero automated test coverage.

**2. `test.yml` is 1,714 bytes — likely minimal (HIGH)**  
A 1,714-byte test workflow is insufficient for a repository with 515+ skill files, JSON corpus entries, Python code, schema files, and ontology files. Likely runs `pytest tests/` with no coverage threshold, no matrix, no fail-fast.

**3. No evaluation harness integration tests (HIGH)**  
The `evaluation/` directory has no corresponding test workflow. Evaluation benchmarks referenced in corpus `evaluation_requirements` are never executed in CI.

**4. No property-based testing (MEDIUM)**  
Given the structured, schema-driven nature of the repository, Hypothesis-style property testing of corpus entry generation or skill validation logic would have high value. No evidence of this.

**5. `validate-graph.yml` is the most robust test (POSITIVE)**  
At 8,135 bytes, the graph validation workflow is the most comprehensive single validation. This is the correct investment pattern — the dependency graph is the highest-risk structural artifact.

### Test Coverage Estimate

| Area | Estimated Coverage |
|---|---|
| Skill `.md` files (structural) | ~70% (validate-skills.yml) |
| JSON schema compliance (skills) | ~60% (schema-enforce.yml) |
| Dependency graph integrity | ~65% (validate-graph.yml) |
| Corpus JSON entries | 0% — no workflow |
| Python source code | Unknown — likely <30% |
| Evaluation harness | 0% |

### Testing Readiness Score: **31 / 100**

Deductions:
- (-30) Zero corpus entry validation
- (-20) Evaluation harness entirely untested
- (-12) Python test coverage unknown/likely low
- (-7) No property-based or mutation testing

---

## Step 8 — CI/CD Audit

### Workflow Inventory (44 total)

**Core build/test (7):**  
`build-and-verify.yml`, `clean-install-test.yml`, `test.yml`, `test-coverage.yml`, `validate-skills.yml`, `validate-graph.yml`, `schema-enforce.yml`

**Release (4):**  
`release.yml`, `release-package.yml`, `semantic-release.yml`, `zero-touch-release.yml`

**Deploy (4):**  
`deploy-blueprints.yml`, `deploy-explorer.yml`, `deploy-pages.yml`, `docs-deploy.yml`

**Security (4):**  
`security-scan.yml`, `osv-watch.yml`, `dependency-auditor.yml`, `dependabot-auto-merge.yml`

**Automation/maintenance (12):**  
`auto-label.yml`, `stale.yml`, `stale-skills.yml`, `keepalive.yml`, `heartbeat.yml`, `used-in-tracker.yml`, `weekly-highlights.yml`, `leaderboard.yml`, `issue-welcome.yml`, `skill-upgrade-comment.yml`, `update-skill-count.yml`, `ast-sweep.yml`

**Content generation (7):**  
`build-graph.yml`, `export-skills.yml`, `generate-blueprint.yml`, `generate-changelog.yml`, `generate-search-index.yml`, `jsonld-export.yml`, `version-stats.yml`

**Miscellaneous (6):**  
`check-links.yml`, `inject-badge-links.yml`, `sync-badges.yml`, `sync-readme-badges.yml`, `revoke-phantom-badges.yml`, `verify-taxonomy.yml`, `skill-version-badge.yml`

### CI/CD Findings

**1. 44 workflows — unmanageable pipeline (HIGH)**  
44 is not a sign of comprehensive CI. It is a sign of accumulated automation without a pipeline architecture review. Many workflows perform redundant operations (4 release workflows, 4 deploy workflows, 5 badge-related workflows). Recommended target: ≤20 workflows organized by lifecycle phase.

**2. No corpus-specific validation workflow (P0)**  
Zero of 44 workflows validate `intelligence/corpus/entries/**/*.json`. This is the most critical gap given corpus is the primary active work product.

**3. Four release workflows with unclear orchestration (HIGH)**  
`release.yml` (2,086 bytes), `release-package.yml` (5,651 bytes), `semantic-release.yml` (955 bytes), `zero-touch-release.yml` (9,924 bytes). No single source of truth for which workflow actually governs releases. Likely causes: partial migrations, abandoned experiments, feature additions without cleanup.

**4. Badge workflows constitute 11% of all workflows (MEDIUM)**  
`inject-badge-links.yml`, `sync-badges.yml`, `sync-readme-badges.yml`, `revoke-phantom-badges.yml`, `skill-version-badge.yml` — 5 workflows exist to manage README badges. Badges are a secondary concern under current protocol. Five workflows for badge management is disproportionate.

**5. `heartbeat.yml` and `keepalive.yml` — duplicate purpose (MEDIUM)**  
Both appear to be scheduled workflows that keep the repository or a service alive. Same purpose, two files.

**6. No workflow for corpus CAP-ID validation (P0)**  
No workflow verifies that CAP-IDs referenced in corpus entries exist in `capability_ontology.json`.

**7. `ast-sweep.yml` — advanced tooling without confirmed source (LOW)**  
AST sweep workflow exists (2,375 bytes) but if Python source modules are absent (see Code Quality §1), this workflow runs against nothing.

### CI/CD Maturity Score: **55 / 100**

Deductions:
- (-20) Zero corpus validation in 44 workflows
- (-12) 4 release workflows with unclear orchestration
- (-8) Pipeline unmanageable at 44 files
- (-5) Badge system consuming 11% of workflow budget

---

## Step 9 — Priority Matrix (Top 20 Findings)

| # | Priority | Finding | Severity | Impact | Effort | Recommendation |
|---|---|---|---|---|---|---|
| 1 | **P0** | No corpus JSON validation in CI | Critical | Any malformed corpus entry silently passes | Low — add 1 workflow | Add `validate-corpus.yml` using ajv/jsonschema against corpus schema |
| 2 | **P0** | Evaluation layer fully disconnected | Critical | All evaluation_requirements in corpus are dead data | High — requires harness wiring | Create evaluation runner that reads corpus eval specs |
| 3 | **P0** | `dependabot-auto-merge.yml` — supply chain risk | Critical | Compromised dep auto-merged to main without review | Low — add status check gates | Require passing CI + label `safe-to-merge` before auto-merge |
| 4 | **P0** | Goal Ontology file does not exist | Critical | `goal_class` field in corpus has no authority file | Low — create the file | Create `intelligence/ontologies/goal_ontology.json` |
| 5 | **P0** | No CODEOWNERS file | High | No automatic reviewer assignment on sensitive paths | Low — create file | Create `.github/CODEOWNERS` covering `intelligence/`, `.github/workflows/`, `schema/` |
| 6 | **P1** | No branch protection on `main` | High | Direct-to-main pushes bypass all CI gates | Low — settings change | Enable required status checks + 1 required review on main |
| 7 | **P1** | 4 release workflows — unclear orchestration | High | Release process is non-deterministic, may cause double-releases | Medium — merge/delete files | Consolidate to 1 authoritative release workflow |
| 8 | **P1** | Outcome Ontology absent | High | P3 priority item has no file — breaks corpus priority chain | Medium | Create `intelligence/ontologies/outcome_ontology.json` |
| 9 | **P1** | `security-scan.yml` is 786 bytes — likely ineffective | High | Security scanning provides false confidence | Low — expand workflow | Add SAST (bandit/semgrep), SARIF output, failure thresholds |
| 10 | **P1** | Capability ontology has no reverse index | High | Cannot query "which entries use CAP-017" without full scan | Medium | Add reverse index to capability ontology or build via script |
| 11 | **P1** | 515+ skill stubs with 0 P0-priority corpus entries referencing them | High | Corpus and skills are architecturally disconnected | High | Create formal `corpus_entry_id` link field in skill frontmatter |
| 12 | **P1** | `requirements.txt` + `pyproject.toml` dual dependency sources | Medium | Non-deterministic dependency resolution | Low — remove requirements.txt | Pin all deps in pyproject.toml, delete requirements.txt |
| 13 | **P1** | `PROJECT_MEMORY.md` (48KB) at root | Medium | Architectural state conflated with project root | Low — move file | Move to `meta/state/PROJECT_MEMORY.md` |
| 14 | **P2** | 44 workflow files — no pipeline architecture | Medium | New contributors cannot understand the pipeline | High — requires consolidation | Write `meta/CI_ARCHITECTURE.md` map; merge duplicates |
| 15 | **P2** | `heartbeat.yml` duplicates `keepalive.yml` | Low | Two workflows doing the same job wastes runner minutes | Low — delete one | Delete `heartbeat.yml` or merge into keepalive |
| 16 | **P2** | 5 badge workflows consuming 11% of pipeline budget | Low | Disproportionate automation for secondary artifact | Medium | Consolidate badge management into 1 workflow |
| 17 | **P2** | `labs/` likely dead directory | Low | Adds noise to repository structure | Low — verify and remove | Audit contents; delete if empty/stale |
| 18 | **P2** | `i18n/` has no corpus or workflow references | Low | Dead directory under current priority scope | Low | Audit; move to `labs/` or delete |
| 19 | **P2** | Issues #87–#91 labeled `bug` are not bugs | Low | Corrupt triage — bugs mixed with enhancements | Low | Relabel all 5 issues: remove `bug`, add `enhancement` |
| 20 | **P2** | Issue #86 contradicts current execution protocol | Low | CLI work is banned — open issue creates confusion | Low | Close #86 with `not-planned`, reference current protocol |

---

## Step 10 — Action Plan (Next 10 Issues)

See `meta/audits/NEXT_10_ISSUES.md` for the full issue definitions.

---

*Audit executed: 2026-07-05. Evidence sources: repository file tree, GitHub Issues API, GitHub Actions workflow inventory, corpus entry analysis, prior session commits.*
