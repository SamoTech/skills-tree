# CRITICAL REMEDIATION PLAN

**Repository**: SamoTech/skills-tree  
**Based On**: SECURITY_QUALITY_ACTIONS_AUDIT.md  
**Plan Date**: 2026-06-14  
**Current Status**: 🔴 Grade F (39/100)  
**Target Status**: 🟢 Grade A (90/100)  

---

## EXECUTIVE SUMMARY

This remediation plan converts audit findings into executable recovery work. The repository currently scores **39/100** with **CRITICAL** security vulnerabilities and **0% executable test coverage**. This plan provides a phased approach to reach production readiness.

**Key Metrics:**
- Security: 35/100 → 90/100
- Reliability: 28/100 → 90/100
- Quality: 41/100 → 85/100
- Automation: 52/100 → 95/100

**Critical Risks:**
1. 🔴 No branch protection (IMMEDIATE)
2. 🔴 0% test coverage (HIGH)
3. 🔴 Release pipeline broken (HIGH)

---

## SECTION 1: IMMEDIATE 24-HOUR FIXES

### ⚠️ CRITICAL: These fixes must be completed within 24 hours

#### 1.1 Enable Branch Protection (5 minutes)
**Priority**: 🔴 CRITICAL  
**Risk Reduction**: 10/10  
**Effort**: 1/10  

**Action Steps:**
1. Navigate to: `Settings` → `Branches` → `Add rule`
2. Branch name pattern: `main`
3. Enable:
   - ✅ Require a pull request before merging
   - ✅ Require approvals: 1
   - ✅ Dismiss stale pull request approvals when new commits are pushed
   - ✅ Require status checks to pass before merging
   - ✅ Require branches to be up to date before merging
   - ✅ Require conversation resolution before merging
   - ✅ Require linear history
   - ✅ Do not allow bypassing the above settings
   - ✅ Restrict who can push to matching branches (admin only)
   - ✅ Lock branch (prevent deletion)
4. Save changes

**Expected Outcome:**
- Force push prevented
- Direct commits blocked
- Required reviews enforced
- Branch deletion prevented

**Verification:**
```bash
# Test: Attempt direct push to main (should fail)
git push origin main
# Expected: "required status checks" error
```

---

#### 1.2 Merge Dependabot PRs (10 minutes)
**Priority**: 🟠 HIGH  
**Risk Reduction**: 6/10  
**Effort**: 1/10  

**Action Steps:**
1. Review PR #82: pytest tmpdir vulnerability
2. Review PR #1: Requests .netrc credentials leak
3. Review PR #2: Requests insecure temp file reuse
4. For each PR:
   - Check dependency changes
   - Verify no breaking changes
   - Merge PR
5. Monitor CI after merge

**Expected Outcome:**
- 3 moderate vulnerabilities patched
- Security score: 35/100 → 45/100

**Verification:**
```bash
# Check Security tab: 0 open Dependabot alerts
```

---

#### 1.3 Disable Broken/Unknown Workflows (30 minutes)
**Priority**: 🟠 MEDIUM  
**Risk Reduction**: 4/10  
**Effort**: 3/10  

**Action Steps:**
1. Temporarily disable workflows with UNKNOWN status:
   - `.github/workflows/deploy-pages.yml` (never used)
   - `.github/workflows/generate-changelog.yml` (status unknown)
2. Add comment header to disabled workflows:
   ```yaml
   # DISABLED: 2026-06-14 - Unknown execution status
   # TODO: Test and re-enable after verification
   ```
3. Create tracking issue: "Audit and re-enable disabled workflows"

**Expected Outcome:**
- Reduce workflow noise
- Focus on working workflows
- Clear technical debt backlog

---

## SECTION 2: 7-DAY FIXES

### 🎯 Security Hardening (Days 1-3)

#### 2.1 Add Workflow Permissions (Day 1)
**Priority**: 🟠 MEDIUM  
**Risk Reduction**: 6/10  
**Effort**: 4/10  

**Action Steps:**
1. Audit all 34 workflows
2. Add least-privilege `permissions:` blocks
3. Template:
   ```yaml
   permissions:
     contents: read  # or write (only if needed)
     pull-requests: read  # or write (only if needed)
     issues: read  # or write (only if needed)
   ```

**Workflow-Specific Permissions:**

| Workflow | Required Permissions |
|----------|---------------------|
| `release-package.yml` | `contents: write`, `packages: write` |
| `sync-badges.yml` | `contents: write` |
| `auto-label.yml` | `issues: write`, `pull-requests: write` |
| `security-scan.yml` | `contents: read`, `security-events: write` |
| `pr-checks.yml` | `pull-requests: read`, `statuses: write` |
| All others | `contents: read` (default) |

**Expected Outcome:**
- Limit blast radius of compromised workflows
- Security score: 45/100 → 55/100

---

#### 2.2 Fix Release Pipeline (Day 2)
**Priority**: 🔴 HIGH  
**Risk Reduction**: 7/10  
**Effort**: 4/10  

**Action Steps:**
1. Inspect recent run logs:
   - Navigate to: `Actions` → `release-package.yml` → Latest run
   - Identify failure point
2. Common failure modes:
   - Missing `GITHUB_TOKEN` scope
   - Invalid tag format
   - Missing release notes
   - Artifact upload failure
3. Test fix locally:
   ```bash
   # Simulate release workflow
   gh release create v0.1.0-test --notes "Test release"
   ```
4. Fix workflow and re-test
5. Document release process in `RELEASE.md`

**Expected Outcome:**
- Release automation restored
- Automation score: 52/100 → 62/100

---

#### 2.3 Enable Required Status Checks (Day 3)
**Priority**: 🟠 HIGH  
**Risk Reduction**: 8/10  
**Effort**: 2/10  

**Action Steps:**
1. Update branch protection rule for `main`
2. Add required status checks:
   - `CodeQL`
   - `security-scan`
   - `test` (after Section 8 complete)
3. Ensure checks run on PRs

**Expected Outcome:**
- Failing builds cannot merge
- Security score: 55/100 → 65/100

---

### 🔧 CI/CD Foundation (Days 4-7)

#### 2.4 Add Error Handling to architect.py (Day 4)
**Priority**: 🔴 HIGH  
**Risk Reduction**: 8/10  
**Effort**: 3/10  

**Action Steps:**
1. Add try/except blocks for file operations:
   ```python
   import logging
   import sys
   
   logging.basicConfig(level=logging.INFO)
   logger = logging.getLogger(__name__)
   
   def __init__(self, graph_path: str = "../data/SKILLS_GRAPH.json"):
       try:
           with open(graph_path, 'r') as f:
               data = json.load(f)
       except FileNotFoundError:
           logger.error(f"Graph file not found: {graph_path}")
           logger.info("Creating empty graph...")
           data = {"nodes": [], "edges": []}
       except json.JSONDecodeError as e:
           logger.error(f"Invalid JSON in {graph_path}: {e}")
           sys.exit(1)
   ```
2. Add input validation:
   ```python
   def add_edge(self, source: str, target: str, edge_type: str):
       if source not in self.graph:
           raise ValueError(f"Node {source} does not exist")
       if target not in self.graph:
           raise ValueError(f"Node {target} does not exist")
       if edge_type not in ["REQUIRES", "LEARN_BEFORE"]:
           raise ValueError(f"Invalid edge type: {edge_type}")
   ```
3. Add logging throughout

**Expected Outcome:**
- Graceful failure on missing files
- Reliability score: 28/100 → 45/100

---

#### 2.5 Add Input Validation (Day 5)
**Priority**: 🟠 MEDIUM  
**Risk Reduction**: 7/10  
**Effort**: 5/10  

**Action Steps:**
1. Create JSON Schema for SKILLS_GRAPH.json:
   ```json
   {
     "$schema": "http://json-schema.org/draft-07/schema#",
     "type": "object",
     "required": ["nodes", "edges"],
     "properties": {
       "nodes": {
         "type": "array",
         "items": {
           "type": "object",
           "required": ["id", "name"],
           "properties": {
             "id": {"type": "string"},
             "name": {"type": "string"},
             "description": {"type": "string"}
           }
         }
       },
       "edges": {
         "type": "array",
         "items": {
           "type": "object",
           "required": ["source", "target", "type"],
           "properties": {
             "source": {"type": "string"},
             "target": {"type": "string"},
             "type": {"enum": ["REQUIRES", "LEARN_BEFORE"]}
           }
         }
       }
     }
   }
   ```
2. Add validation in architect.py:
   ```python
   import jsonschema
   
   def validate_graph(data: dict):
       with open('schemas/skills_graph_schema.json', 'r') as f:
           schema = json.load(f)
       jsonschema.validate(data, schema)
   ```
3. Run validation on load

**Expected Outcome:**
- Invalid graph data detected early
- Reliability score: 45/100 → 60/100

---

#### 2.6 Consolidate Redundant Workflows (Days 6-7)
**Priority**: 🟡 LOW  
**Risk Reduction**: 4/10  
**Effort**: 5/10  

**Action Steps:**
1. **Merge `heartbeat.yml` + `keepalive.yml`**:
   - Both prevent workflow disable
   - Keep `heartbeat.yml`, delete `keepalive.yml`
2. **Merge `sync-badges.yml` + `sync-readme-badges.yml`**:
   - Combine into single badge sync workflow
3. **Merge `stale.yml` + `stale-skills.yml`**:
   - Unify stale marking logic
4. Test merged workflows
5. Delete redundant files

**Expected Outcome:**
- 34 workflows → 31 workflows
- Maintainability score: 41/100 → 50/100

---

## SECTION 3: 30-DAY FIXES

### 🔬 Reliability (Days 8-15)

#### 3.1 Fix Test Suite (Days 8-10)
**Priority**: 🔴 CRITICAL  
**Risk Reduction**: 9/10  
**Effort**: 6/10  

**Action Steps** (from Sprint A.5 findings):

1. **Fix import paths** (Day 8):
   ```python
   # tests/test_graph.py
   import sys
   from pathlib import Path
   sys.path.insert(0, str(Path(__file__).parent.parent / 'tools'))
   
   from architect import SkillsGraph
   ```

2. **Create test fixtures** (Day 9):
   ```python
   # tests/conftest.py
   import pytest
   import json
   from pathlib import Path
   
   @pytest.fixture
   def sample_graph_data():
       return {
           "nodes": [
               {"id": "python", "name": "Python"},
               {"id": "flask", "name": "Flask"}
           ],
           "edges": [
               {"source": "flask", "target": "python", "type": "REQUIRES"}
           ]
       }
   
   @pytest.fixture
   def sample_graph(tmp_path, sample_graph_data):
       graph_file = tmp_path / "test_graph.json"
       graph_file.write_text(json.dumps(sample_graph_data))
       from architect import SkillsGraph
       return SkillsGraph(str(graph_file))
   ```

3. **Rewrite tests to use fixtures** (Day 10):
   ```python
   # tests/test_graph.py
   def test_add_node(sample_graph):
       sample_graph.add_node("django", "Django")
       assert "django" in sample_graph.graph
   
   def test_find_dependencies(sample_graph):
       deps = sample_graph.find_dependencies("flask")
       assert "python" in deps
   ```

4. **Run tests locally**:
   ```bash
   pytest tests/ -v
   # Target: 60/60 tests passing
   ```

**Expected Outcome:**
- 60 executable tests
- Quality score: 41/100 → 60/100

---

#### 3.2 Add Configuration Support (Days 11-12)
**Priority**: 🟡 MEDIUM  
**Risk Reduction**: 5/10  
**Effort**: 4/10  

**Action Steps:**
1. Create `config/architect.yaml`:
   ```yaml
   graph:
     path: "data/SKILLS_GRAPH.json"
     schema: "schemas/skills_graph_schema.json"
   
   logging:
     level: INFO
     format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
   
   validation:
     strict_mode: true
     check_orphaned_edges: true
   
   edge_types:
     - "REQUIRES"
     - "LEARN_BEFORE"
   ```

2. Load config in architect.py:
   ```python
   import yaml
   
   def load_config(config_path="config/architect.yaml"):
       with open(config_path, 'r') as f:
           return yaml.safe_load(f)
   ```

3. Replace hardcoded values with config

**Expected Outcome:**
- Configurable behavior
- Maintainability score: 50/100 → 60/100

---

### 📊 Observability (Days 13-15)

#### 3.3 Add Logging Framework (Day 13)
**Priority**: 🟠 MEDIUM  
**Risk Reduction**: 5/10  
**Effort**: 3/10  

**Action Steps:**
1. Configure logging in architect.py:
   ```python
   import logging
   
   logging.basicConfig(
       level=logging.INFO,
       format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
       handlers=[
           logging.FileHandler('logs/architect.log'),
           logging.StreamHandler()
       ]
   )
   logger = logging.getLogger(__name__)
   ```

2. Add log statements:
   ```python
   def add_node(self, node_id, name):
       logger.info(f"Adding node: {node_id} ({name})")
       # ... implementation ...
       logger.debug(f"Node {node_id} added successfully")
   ```

3. Log errors:
   ```python
   except Exception as e:
       logger.error(f"Failed to load graph: {e}", exc_info=True)
   ```

**Expected Outcome:**
- Debuggable failures
- Observability score: 38/100 → 50/100

---

#### 3.4 Add Metrics Collection (Days 14-15)
**Priority**: 🟡 LOW  
**Risk Reduction**: 3/10  
**Effort**: 4/10  

**Action Steps:**
1. Track operation metrics:
   ```python
   from collections import Counter
   import time
   
   class SkillsGraph:
       def __init__(self):
           self.metrics = {
               'operations': Counter(),
               'errors': Counter(),
               'latency': []
           }
       
       def add_node(self, node_id, name):
           start = time.time()
           try:
               # ... implementation ...
               self.metrics['operations']['add_node'] += 1
           except Exception as e:
               self.metrics['errors']['add_node'] += 1
               raise
           finally:
               self.metrics['latency'].append(time.time() - start)
   ```

2. Export metrics:
   ```python
   def get_metrics(self):
       return {
           'total_operations': sum(self.metrics['operations'].values()),
           'total_errors': sum(self.metrics['errors'].values()),
           'avg_latency': sum(self.metrics['latency']) / len(self.metrics['latency'])
       }
   ```

**Expected Outcome:**
- Performance visibility
- Observability score: 50/100 → 60/100

---

### 🤖 Automation (Days 16-30)

#### 3.5 Create Test Execution Workflow (Day 16)
**Priority**: 🔴 CRITICAL  
**Risk Reduction**: 8/10  
**Effort**: 3/10  

**See SECTION 8 for detailed implementation**

---

#### 3.6 Add Coverage Reporting (Day 17)
**Priority**: 🟠 HIGH  
**Risk Reduction**: 7/10  
**Effort**: 3/10  

**Action Steps:**
1. Install coverage tools:
   ```bash
   pip install pytest-cov
   ```

2. Configure pytest coverage:
   ```ini
   # pyproject.toml
   [tool.pytest.ini_options]
   addopts = "--cov=tools --cov-report=html --cov-report=term --cov-fail-under=80"
   ```

3. Add coverage upload to test workflow:
   ```yaml
   - name: Upload coverage to Codecov
     uses: codecov/codecov-action@v3
     with:
       files: ./coverage.xml
   ```

4. Add coverage badge to README.md:
   ```markdown
   [![codecov](https://codecov.io/gh/SamoTech/skills-tree/branch/main/graph/badge.svg)](https://codecov.io/gh/SamoTech/skills-tree)
   ```

**Expected Outcome:**
- Visible coverage metrics
- Quality score: 60/100 → 70/100

---

#### 3.7 Add Performance Testing (Days 18-20)
**Priority**: 🟡 LOW  
**Risk Reduction**: 4/10  
**Effort**: 5/10  

**Action Steps:**
1. Create `tests/test_performance.py`:
   ```python
   import pytest
   import time
   
   def test_large_graph_performance(tmp_path):
       # Generate graph with 10,000 nodes
       large_graph_data = {
           "nodes": [{"id": f"node_{i}", "name": f"Node {i}"} for i in range(10000)],
           "edges": [{"source": f"node_{i}", "target": f"node_{i+1}", "type": "REQUIRES"} for i in range(9999)]
       }
       
       graph_file = tmp_path / "large_graph.json"
       graph_file.write_text(json.dumps(large_graph_data))
       
       start = time.time()
       graph = SkillsGraph(str(graph_file))
       load_time = time.time() - start
       
       assert load_time < 1.0, f"Graph load too slow: {load_time}s"
   ```

2. Add benchmarking:
   ```bash
   pip install pytest-benchmark
   ```

3. Create benchmark workflow: `.github/workflows/benchmark.yml`

**Expected Outcome:**
- Performance regression detection
- Quality score: 70/100 → 75/100

---

## SECTION 4: GITHUB ACTIONS RECOVERY

### Workflow Decision Matrix

For each of the 34 workflows, decision: **Keep** / **Fix** / **Disable** / **Delete**

#### ✅ KEEP (Healthy Workflows)

| Workflow | Status | Action | Justification |
|----------|--------|--------|---------------|
| `security-scan.yml` | ✅ PASSING | Keep | Secret detection working |
| `CodeQL` | ✅ PASSING | Keep | Security scanning essential |
| `Automatic Dependency Submission` | ✅ PASSING | Keep | Dependency graph maintenance |
| `pages-build-deployment` | ✅ PASSING | Keep | GitHub Pages automation |
| `uptime-monitor.yml` | ✅ PASSING | Keep | Monitoring active |

**Total**: 5 workflows

---

#### 🔧 FIX (Broken/Failing Workflows)

| Workflow | Status | Fix Action | Priority | Timeline |
|----------|--------|------------|----------|----------|
| `release-package.yml` | 🔴 FAILING | Debug logs, fix root cause | CRITICAL | Day 2 |
| `generate-changelog.yml` | ⚠️ UNKNOWN | Test execution, verify output | MEDIUM | Day 10 |
| `build-graph.yml` | ✅ PASSING | Add error handling | LOW | Day 20 |
| `check-links.yml` | ✅ PASSING | Add link validation config | LOW | Day 25 |

**Total**: 4 workflows

**Fix Plan for `release-package.yml`**:
1. Review run logs for error details
2. Common fixes:
   - Add `permissions: contents: write, packages: write`
   - Fix tag pattern matching
   - Add release notes automation
3. Test with manual trigger
4. Document release process

---

#### ⏸️ DISABLE (Unknown Status - Audit Required)

| Workflow | Current Status | Disable Reason | Re-enable Condition |
|----------|----------------|----------------|---------------------|
| `ast-sweep.yml` | ⚠️ UNKNOWN | No recent runs | After testing |
| `dependency-auditor.yml` | ⚠️ UNKNOWN | Phase 3 unclear | After Sprint 3 |
| `heartbeat.yml` | ⚠️ UNKNOWN | Redundant with keepalive | After consolidation |
| `keepalive.yml` | ⚠️ UNKNOWN | Redundant with heartbeat | After consolidation |
| `leaderboard.yml` | ⚠️ UNKNOWN | No evidence of use | After verification |
| `quality-report.yml` | ⚠️ UNKNOWN | Status unknown | After testing |
| `pr-checks.yml` | ⚠️ UNKNOWN | Critical but untested | After testing |
| `auto-label.yml` | ⚠️ UNKNOWN | Nice-to-have | After testing |
| `issue-welcome.yml` | ⚠️ UNKNOWN | Community feature | After testing |
| `stale.yml` | ⚠️ UNKNOWN | Redundant | After consolidation |
| `stale-skills.yml` | ⚠️ UNKNOWN | Redundant | After consolidation |
| `deploy-pages.yml` | ⚠️ UNKNOWN | Never triggered | After use case defined |
| `export-skills.yml` | ⚠️ UNKNOWN | No recent runs | After testing |
| `generate-search-index.yml` | ⚠️ UNKNOWN | No recent runs | After testing |
| `inject-badge-links.yml` | ⚠️ UNKNOWN | No recent runs | After testing |
| `jsonld-export.yml` | ⚠️ UNKNOWN | No recent runs | After testing |
| `osv-watch.yml` | ⚠️ UNKNOWN | Security monitoring | After testing |
| `revoke-phantom-badges.yml` | ⚠️ UNKNOWN | No recent runs | After testing |
| `schema-enforce.yml` | ⚠️ UNKNOWN | Critical but untested | After testing |
| `skill-upgrade-comment.yml` | ⚠️ UNKNOWN | No recent runs | After testing |
| `skill-version-badge.yml` | ⚠️ UNKNOWN | No recent runs | After testing |
| `sync-badges.yml` | ⚠️ UNKNOWN | Redundant | After consolidation |
| `sync-readme-badges.yml` | ⚠️ UNKNOWN | Redundant | After consolidation |
| `update-skill-count.yml` | ⚠️ UNKNOWN | No recent runs | After testing |
| `used-in-tracker.yml` | ⚠️ UNKNOWN | No recent runs | After testing |
| `validate-skills.yml` | ⚠️ UNKNOWN | Critical but untested | After testing |
| `version-stats.yml` | ⚠️ UNKNOWN | No recent runs | After testing |
| `weekly-highlights.yml` | ⚠️ UNKNOWN | No recent runs | After testing |

**Total**: 28 workflows

**Disable Strategy**:
1. Add to each workflow file:
   ```yaml
   # TEMPORARILY DISABLED: 2026-06-14
   # Reason: Unknown execution status - requires testing
   # Re-enable after: Manual verification
   on:
     workflow_dispatch:  # Keep manual trigger only
   ```

2. Create tracking issue:
   ```markdown
   ## Workflow Audit Tracking
   
   28 workflows disabled pending verification:
   - [ ] ast-sweep.yml - Test and verify
   - [ ] dependency-auditor.yml - Define Phase 3
   ...
   ```

---

#### 🗑️ DELETE (Truly Redundant)

| Workflow | Delete Reason | Replacement |
|----------|---------------|-------------|
| None (initially) | Hold deletions until consolidation tested | TBD after Section 2.6 |

**Deletion Strategy**:
- After consolidation in Section 2.6, delete:
  - `keepalive.yml` (merged into heartbeat.yml)
  - `sync-readme-badges.yml` (merged into sync-badges.yml)
  - `stale-skills.yml` (merged into stale.yml)

**Total**: 3 workflows (after consolidation)

---

### Workflow Recovery Timeline

| Phase | Timeframe | Actions |
|-------|-----------|----------|
| **Phase 1**: Emergency | Day 1 | Disable 28 unknown workflows |
| **Phase 2**: Fix Critical | Days 2-7 | Fix `release-package.yml` |
| **Phase 3**: Consolidate | Days 6-7 | Merge redundant workflows |
| **Phase 4**: Test & Re-enable | Days 8-30 | Systematic testing of disabled workflows |

---

## SECTION 5: SECRETS RECOVERY

### 5.1 Secret Audit Status

**Current State**: ✅ **GOOD**  
- Gitleaks active (no secrets detected)
- CodeQL scanning enabled
- No hardcoded secrets observed

### 5.2 Secret Management Plan

#### Identify

**Action**: Comprehensive secret scan

1. **Repository Secrets** (GitHub Settings):
   ```bash
   # List configured secrets
   gh secret list
   ```
   
   Expected secrets:
   - `GITHUB_TOKEN` (auto-provided)
   - No custom secrets expected

2. **Workflow Hardcoded Secrets**:
   ```bash
   # Scan all workflow files
   grep -r "password\|token\|secret\|key" .github/workflows/
   ```
   
   Expected: None

3. **Code Secrets**:
   ```bash
   # Run additional scanners
   docker run --rm -v $(pwd):/src trufflesecurity/trufflehog:latest github --repo=SamoTech/skills-tree
   ```

**Findings**: No secrets requiring rotation (as of audit)

---

#### Rotate

**No immediate rotation required**

**Preventive Rotation Policy**:
1. **Quarterly rotation** of any API keys (when added)
2. **Immediate rotation** if:
   - Secret appears in commit history
   - Team member leaves
   - Suspicious activity detected

**Rotation Procedure** (for future use):
```bash
# 1. Generate new secret
# 2. Update GitHub secret
gh secret set NEW_SECRET < new_secret.txt

# 3. Update workflows
# 4. Test with new secret
# 5. Revoke old secret
```

---

#### Remove

**Action**: Remove any false-positive secrets

1. **Git History Cleanup** (if secrets ever found):
   ```bash
   # Use BFG Repo-Cleaner
   java -jar bfg.jar --replace-text passwords.txt
   git reflog expire --expire=now --all
   git gc --prune=now --aggressive
   ```

2. **Workflow Cleanup**:
   - Ensure no secrets in environment variables
   - Use GitHub Secrets properly:
     ```yaml
     env:
       API_KEY: ${{ secrets.API_KEY }}  # ✅ Correct
       # NOT: API_KEY: "sk-abc123..."  # ❌ Wrong
     ```

**Current Status**: No removal needed

---

#### Replace

**Action**: Migrate from any legacy secret handling

1. **Replace hardcoded values with secrets**:
   - None identified (repository clean)

2. **Future secret addition workflow**:
   ```bash
   # 1. Add secret via CLI
   gh secret set API_KEY < api_key.txt
   
   # 2. Reference in workflow
   # .github/workflows/example.yml
   env:
     API_KEY: ${{ secrets.API_KEY }}
   
   # 3. Never commit secret values
   ```

3. **Secret Storage Best Practices**:
   - ✅ Use GitHub Secrets for sensitive data
   - ✅ Use environment variables in workflows
   - ❌ Never hardcode in YAML
   - ❌ Never commit to .env files

---

### 5.3 Secret Monitoring (Continuous)

**Implement**:

1. **Pre-commit hooks**:
   ```yaml
   # .pre-commit-config.yaml
   repos:
     - repo: https://github.com/Yelp/detect-secrets
       rev: v1.4.0
       hooks:
         - id: detect-secrets
   ```

2. **GitHub Secret Scanning** (already enabled):
   - Partner patterns detected
   - Push protection enabled

3. **Gitleaks in CI** (already active):
   - `.github/workflows/security-scan.yml` ✅

**Expected Outcome**:
- Secrets never reach repository
- Security score: 65/100 → 70/100

---

## SECTION 6: BRANCH PROTECTION PLAN

### 6.1 Required Settings

**Branch**: `main`

#### General Settings

```yaml
Branch name pattern: main

Require a pull request before merging:
  ✅ Enabled
  
  Required approvals: 1
  ✅ Dismiss stale pull request approvals when new commits are pushed
  ✅ Require review from Code Owners
  ❌ Restrict who can dismiss pull request reviews (optional for solo dev)
  ✅ Allow specified actors to bypass required pull requests (admins only)
  ✅ Require approval of the most recent reviewable push

Require status checks to pass before merging:
  ✅ Enabled
  
  ✅ Require branches to be up to date before merging
  
  Required status checks:
    - CodeQL
    - security-scan
    - test (after Section 8)
    - build-graph (if re-enabled)

Require conversation resolution before merging:
  ✅ Enabled

Require signed commits:
  ⚠️ Optional (recommended for high-security projects)

Require linear history:
  ✅ Enabled (prevents merge commits)

Require deployments to succeed before merging:
  ❌ Disabled (no deployment environment)

Lock branch:
  ✅ Enabled (prevent deletion)

Do not allow bypassing the above settings:
  ✅ Enabled (enforce for all including admins)

Restrict who can push to matching branches:
  ✅ Enabled
  Allowed: Admins only

Allow force pushes:
  ❌ Disabled (CRITICAL)

Allow deletions:
  ❌ Disabled (CRITICAL)
```

---

### 6.2 Implementation Steps

**Day 1** (5 minutes):

1. Navigate to: `https://github.com/SamoTech/skills-tree/settings/branches`
2. Click: `Add rule`
3. Configure:
   - Branch name pattern: `main`
   - Enable all checkboxes per Section 6.1
   - Add required status checks:
     - `CodeQL`
     - `security-scan / Secret Scanning`
4. Save changes

**Verification**:
```bash
# Test 1: Direct push (should fail)
git push origin main
# Expected: Error: "required status checks"

# Test 2: Force push (should fail)
git push origin main --force
# Expected: Error: "force push is not allowed"

# Test 3: Create PR (should succeed)
git checkout -b test-branch-protection
echo "test" > test.txt
git add test.txt
git commit -m "Test branch protection"
git push origin test-branch-protection
gh pr create --title "Test PR" --body "Testing branch protection"
# Expected: PR created, awaiting reviews and checks
```

---

### 6.3 Post-Implementation Monitoring

**Week 1**: Monitor PR workflow
- Verify required reviews enforced
- Verify status checks block merges
- Verify no bypass attempts

**Week 2**: Adjust settings if needed
- Add/remove required status checks
- Adjust approval count if collaborators increase

**Expected Outcome**:
- Security score: 35/100 → 70/100 (immediate)
- Zero accidental force pushes
- All code reviewed before merge

---

## SECTION 7: DEPENDENCY REMEDIATION

### 7.1 Current Vulnerabilities

**Total**: 3 moderate vulnerabilities

#### Prioritized List

| # | Severity | Package | CVE | CVSS | Impact | Fix |
|---|----------|---------|-----|------|--------|-----|
| 1 | 🟠 MODERATE | pytest | CVE-2024-XXXX | 5.5 | tmpdir handling allows local file access | Merge PR #82 |
| 2 | 🟠 MODERATE | requests | CVE-2023-32681 | 6.1 | .netrc credentials leak to HTTP servers | Merge PR #1 |
| 3 | 🟠 MODERATE | requests | CVE-2024-YYYY | 5.3 | Insecure temp file reuse | Merge PR #2 |

---

### 7.2 Remediation Plan

#### PR #82: pytest tmpdir vulnerability

**Action** (Day 1):
```bash
# Review PR
gh pr view 82

# Check diff
gh pr diff 82

# Verify pytest version upgrade
# Expected: pytest==8.x.x (or latest secure version)

# Merge
gh pr merge 82 --squash
```

**Risk**: LOW (pytest is dev dependency, not runtime)

---

#### PR #1: requests .netrc credentials leak

**Action** (Day 1):
```bash
# Review PR
gh pr view 1

# Verify requests version upgrade
# Expected: requests>=2.31.0

# Check breaking changes
pip install requests==2.31.0
pytest tests/  # Ensure no breaks

# Merge
gh pr merge 1 --squash
```

**Risk**: MEDIUM (requests used if architect.py fetches remote data)

---

#### PR #2: requests insecure temp file reuse

**Action** (Day 1):
```bash
# Review and merge
gh pr merge 2 --squash
```

**Risk**: MEDIUM

---

### 7.3 Dependency Monitoring (Ongoing)

**Already Active**:
- ✅ Dependabot alerts enabled
- ✅ Automatic Dependency Submission workflow
- ✅ osv-watch.yml (status unknown - verify)

**Add** (Day 5):

1. **Weekly dependency audit workflow**:
   ```yaml
   # .github/workflows/dependency-audit.yml
   name: Dependency Audit
   on:
     schedule:
       - cron: '0 0 * * 1'  # Monday midnight
     workflow_dispatch:
   
   jobs:
     audit:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v4
         
         - name: Set up Python
           uses: actions/setup-python@v4
           with:
             python-version: '3.11'
         
         - name: Install dependencies
           run: pip install -r requirements.txt
         
         - name: Run pip audit
           run: |
             pip install pip-audit
             pip-audit --desc
         
         - name: Run safety check
           run: |
             pip install safety
             safety check --json
   ```

2. **Automated dependency updates**:
   ```yaml
   # .github/dependabot.yml (enhance existing)
   version: 2
   updates:
     - package-ecosystem: "pip"
       directory: "/"
       schedule:
         interval: "weekly"
       open-pull-requests-limit: 10
       reviewers:
         - "SamoTech"
       labels:
         - "dependencies"
         - "security"
   ```

**Expected Outcome**:
- Zero open vulnerabilities
- Weekly automated checks
- Security score: 70/100 → 75/100

---

### 7.4 Dependency Policy

**Policy** (document in SECURITY.md):

1. **Severity Response Times**:
   - 🔴 CRITICAL: Fix within 24 hours
   - 🟠 HIGH: Fix within 7 days
   - 🟡 MODERATE: Fix within 30 days
   - 🟢 LOW: Fix within 90 days

2. **Merge Criteria**:
   - All dependency PRs require:
     - ✅ Passing tests
     - ✅ CHANGELOG review
     - ✅ Breaking change assessment

3. **Pinning Strategy**:
   ```txt
   # requirements.txt
   # Pin exact versions for reproducibility
   pytest==8.0.0
   requests==2.31.0
   
   # Allow patch updates for security
   # Use renovate or dependabot for automation
   ```

---

## SECTION 8: TEST INTEGRATION PLAN

### 8.1 Current State

**Status**: 🔴 **FAILING**
- 60 tests created
- 0% executable (import errors)
- No CI integration

**Root Causes** (from Sprint A.5):
1. Import path mismatch
2. Missing test fixtures
3. Interface mismatch (tests expect dicts, code uses classes)
4. No pytest configuration

---

### 8.2 Fix Test Suite (Days 8-10)

#### Day 8: Fix Imports

**Create** `tests/__init__.py`:
```python
# tests/__init__.py
import sys
from pathlib import Path

# Add tools/ to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / 'tools'))
```

**Update test files**:
```python
# tests/test_graph.py
from architect import SkillsGraph, RecommendationEngine, BlueprintGenerator
```

**Verify**:
```bash
python -m pytest tests/test_graph.py -v
# Should import successfully (may still fail on assertions)
```

---

#### Day 9: Create Test Fixtures

**Create** `tests/conftest.py`:
```python
import pytest
import json
from pathlib import Path
import tempfile

@pytest.fixture
def sample_graph_data():
    """Minimal valid graph data."""
    return {
        "nodes": [
            {"id": "python", "name": "Python", "category": "Language"},
            {"id": "flask", "name": "Flask", "category": "Framework"},
            {"id": "django", "name": "Django", "category": "Framework"},
            {"id": "fastapi", "name": "FastAPI", "category": "Framework"}
        ],
        "edges": [
            {"source": "flask", "target": "python", "type": "REQUIRES"},
            {"source": "django", "target": "python", "type": "REQUIRES"},
            {"source": "fastapi", "target": "python", "type": "REQUIRES"}
        ]
    }

@pytest.fixture
def graph_file(tmp_path, sample_graph_data):
    """Create temporary graph JSON file."""
    graph_path = tmp_path / "skills_graph.json"
    graph_path.write_text(json.dumps(sample_graph_data))
    return str(graph_path)

@pytest.fixture
def skills_graph(graph_file):
    """Initialized SkillsGraph instance."""
    from architect import SkillsGraph
    return SkillsGraph(graph_file)

@pytest.fixture
def recommendation_engine(skills_graph):
    """Initialized RecommendationEngine instance."""
    from architect import RecommendationEngine
    return RecommendationEngine(skills_graph)

@pytest.fixture
def blueprint_generator(skills_graph):
    """Initialized BlueprintGenerator instance."""
    from architect import BlueprintGenerator
    return BlueprintGenerator(skills_graph)
```

---

#### Day 10: Rewrite Tests

**Example**: `tests/test_graph.py`

```python
import pytest
from architect import SkillsGraph

def test_graph_initialization(skills_graph):
    """Test graph loads correctly."""
    assert len(skills_graph.graph) == 4
    assert "python" in skills_graph.graph
    assert "flask" in skills_graph.graph

def test_find_dependencies(skills_graph):
    """Test dependency resolution."""
    deps = skills_graph.find_dependencies("flask")
    assert "python" in deps
    assert len(deps) == 1

def test_add_node(skills_graph):
    """Test node addition."""
    skills_graph.add_node("rust", "Rust")
    assert "rust" in skills_graph.graph
    assert skills_graph.graph["rust"]["name"] == "Rust"

def test_add_edge(skills_graph):
    """Test edge addition."""
    skills_graph.add_edge("django", "flask", "LEARN_BEFORE")
    # Verify edge exists in graph structure
    # (implementation-dependent)

def test_cyclic_dependency_detection(skills_graph):
    """Test cyclic dependency detection."""
    # Add cycle: python -> flask -> python
    skills_graph.add_edge("python", "flask", "REQUIRES")
    
    with pytest.raises(ValueError, match="cyclic"):
        skills_graph.validate_graph()

def test_missing_node_error(skills_graph):
    """Test error on missing node reference."""
    with pytest.raises(ValueError, match="does not exist"):
        skills_graph.add_edge("nonexistent", "python", "REQUIRES")
```

**Run all tests**:
```bash
pytest tests/ -v --tb=short
# Target: 60/60 passing
```

---

### 8.3 Create Test Workflow (Day 16)

**Create** `.github/workflows/test.yml`:

```yaml
name: Test Suite

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]
  workflow_dispatch:

jobs:
  test:
    name: Test Python ${{ matrix.python-version }}
    runs-on: ubuntu-latest
    
    strategy:
      matrix:
        python-version: ['3.9', '3.10', '3.11', '3.12']
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}
      
      - name: Cache dependencies
        uses: actions/cache@v3
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ hashFiles('requirements.txt') }}
      
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install pytest pytest-cov pytest-xdist
      
      - name: Run tests
        run: |
          pytest tests/ \
            --verbose \
            --cov=tools \
            --cov-report=xml \
            --cov-report=term \
            --cov-fail-under=80 \
            -n auto
      
      - name: Upload coverage to Codecov
        if: matrix.python-version == '3.11'
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage.xml
          flags: unittests
          name: codecov-umbrella
      
      - name: Archive test results
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: test-results-${{ matrix.python-version }}
          path: |
            htmlcov/
            .coverage

permissions:
  contents: read
  pull-requests: write  # For coverage comments
```

---

### 8.4 Add pytest Configuration (Day 16)

**Create** `pyproject.toml`:

```toml
[build-system]
requires = ["setuptools>=45", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "skills-tree"
version = "0.1.0"
description = "Skills graph management and recommendation system"
readme = "README.md"
requires-python = ">=3.9"

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]

addopts = [
    "--verbose",
    "--strict-markers",
    "--cov=tools",
    "--cov-report=html",
    "--cov-report=term-missing",
    "--cov-fail-under=80",
]

markers = [
    "slow: marks tests as slow (deselect with '-m \"not slow\"')",
    "integration: marks tests as integration tests",
    "unit: marks tests as unit tests",
]

[tool.coverage.run]
source = ["tools"]
omit = [
    "*/tests/*",
    "*/test_*.py",
]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
    "raise NotImplementedError",
    "if __name__ == .__main__.:",
    "if TYPE_CHECKING:",
]
```

---

### 8.5 Update Branch Protection (Day 16)

**Add required status check**:

1. Go to: `Settings` → `Branches` → Edit `main` rule
2. Add required status check:
   - `Test Suite / Test Python 3.11`
3. Save

**Result**: PRs cannot merge without passing tests

---

### 8.6 Expected Outcomes

**After Day 10**:
- ✅ 60 executable tests
- ✅ Tests pass locally
- Quality score: 41/100 → 60/100

**After Day 16**:
- ✅ CI test execution
- ✅ Coverage reporting
- ✅ Test results in PR comments
- Quality score: 60/100 → 75/100

**After Day 17**:
- ✅ Coverage badge in README
- ✅ 80%+ test coverage
- Quality score: 75/100 → 80/100

---

## SECTION 9: PRODUCTION READINESS PATH

### Scoring Progression

#### Current: 39/100 (Grade F)

**Breakdown**:
- Security: 35/100
- Reliability: 28/100
- Quality: 41/100
- Automation: 52/100
- Observability: 38/100

---

### Milestone 1: 50/100 (Grade D)
**Target**: End of Week 1 (Day 7)

#### Actions Required:
1. ✅ Enable branch protection (+30 security points)
2. ✅ Merge 3 Dependabot PRs (+10 security points)
3. ✅ Add workflow permissions (+10 security points)
4. ✅ Fix release pipeline (+10 automation points)
5. ✅ Add error handling to architect.py (+15 reliability points)

#### Expected Scores:
- Security: 35 → 75/100 ✅
- Reliability: 28 → 43/100 ⚠️
- Quality: 41/100 (unchanged)
- Automation: 52 → 62/100 ⚠️
- Observability: 38/100 (unchanged)

**Overall**: (75+43+41+62+38)/5 = **51.8/100** ✅

**Grade**: 🟡 **D**

---

### Milestone 2: 75/100 (Grade C)
**Target**: End of Week 3 (Day 21)

#### Additional Actions:
1. ✅ Fix test suite (+35 quality points)
2. ✅ Add test execution workflow (+20 quality points)
3. ✅ Add coverage reporting (+10 quality points)
4. ✅ Add input validation (+15 reliability points)
5. ✅ Add logging framework (+12 observability points)
6. ✅ Add configuration support (+10 maintainability points)
7. ✅ Consolidate workflows (+8 maintainability points)

#### Expected Scores:
- Security: 75 → 80/100 (required checks)
- Reliability: 43 → 70/100 ✅
- Quality: 41 → 86/100 ✅
- Automation: 62 → 72/100 ⚠️
- Observability: 38 → 55/100 ⚠️

**Overall**: (80+70+86+72+55)/5 = **72.6/100** ⚠️

**Adjusted Target**: Need +3 points

**Add**:
- ✅ Add metrics collection (+5 observability) → 60/100

**Overall**: (80+70+86+72+60)/5 = **73.6/100** ✅

**Grade**: 🟢 **C**

---

### Milestone 3: 90/100 (Grade A-)
**Target**: End of Week 4-5 (Day 30-35)

#### Additional Actions:
1. ✅ Add performance testing (+5 quality points)
2. ✅ Add static analysis (mypy, ruff) (+5 quality points)
3. ✅ Add integration tests (+10 quality points)
4. ✅ Add alerting system (+15 observability points)
5. ✅ Add deployment workflow (+10 automation points)
6. ✅ Add benchmarking (+8 observability points)
7. ✅ Audit and re-enable workflows (+10 automation points)
8. ✅ Add documentation coverage (+5 quality points)
9. ✅ Add pre-commit hooks (+5 security points)
10. ✅ Add SBOM generation (+5 security points)

#### Expected Scores:
- Security: 80 → 90/100 ✅
- Reliability: 70 → 85/100 ✅
- Quality: 86 → 91/100 ✅
- Automation: 72 → 92/100 ✅
- Observability: 60 → 83/100 ✅

**Overall**: (90+85+91+92+83)/5 = **88.2/100** ⚠️

**Adjusted**:
- Add: Security policy documentation (+2 security)
- Add: Disaster recovery plan (+3 reliability)

**Overall**: (92+88+91+92+83)/5 = **89.2/100** ≈ **90/100** ✅

**Grade**: 🟢 **A-**

---

### Visual Roadmap

```
Current                  Week 1              Week 3              Week 5
39/100 ────────────────> 50/100 ──────────> 75/100 ──────────> 90/100
Grade F                 Grade D             Grade C            Grade A-

🔴 CRITICAL              🟡 POOR             🟢 ACCEPTABLE       🟢 EXCELLENT
│                        │                   │                   │
├─ No branch protection  ├─ Branch protected  ├─ Tests passing    ├─ Full automation
├─ 0% tests executable   ├─ Vulns patched    ├─ 80%+ coverage    ├─ Monitoring active
├─ 3 vulnerabilities     ├─ Errors handled   ├─ Logging enabled  ├─ Benchmarks running
└─ Release broken        └─ Release fixed    └─ Workflows clean  └─ Production ready
```

---

### Maintenance Plan (Post-90/100)

**Monthly**:
- Review Dependabot PRs
- Audit workflow execution
- Review test coverage trends
- Update documentation

**Quarterly**:
- Security audit
- Performance benchmarking
- Dependency cleanup
- Workflow optimization

**Annually**:
- Full security penetration test
- Architecture review
- Tech debt cleanup sprint

---

## SECTION 10: EXECUTION ORDER

### Top 20 Fixes (Ranked)

| # | Fix | Risk Reduction | Effort | Impact | Priority Score | Day | Section |
|---|-----|----------------|--------|--------|----------------|-----|----------|
| 1 | **Enable Branch Protection** | 10 | 1 | 10 | **100** | 1 | 1.1 |
| 2 | **Add Test Execution Workflow** | 8 | 3 | 9 | **72** | 16 | 8.3 |
| 3 | **Require PR Reviews** | 8 | 1 | 8 | **64** | 1 | 1.1 |
| 4 | **Fix Release Pipeline** | 7 | 4 | 8 | **56** | 2 | 2.2 |
| 5 | **Add Error Handling** | 8 | 3 | 7 | **56** | 4 | 2.4 |
| 6 | **Fix Test Suite** | 9 | 6 | 9 | **54** | 8-10 | 3.1 |
| 7 | **Merge Dependabot PRs** | 6 | 1 | 6 | **36** | 1 | 1.2 |
| 8 | **Add Workflow Permissions** | 6 | 4 | 6 | **36** | 1 | 2.1 |
| 9 | **Add Input Validation** | 7 | 5 | 7 | **35** | 5 | 2.5 |
| 10 | **Add Coverage Reporting** | 7 | 3 | 7 | **33** | 17 | 3.6 |
| 11 | **Enable Required Status Checks** | 8 | 2 | 8 | **32** | 3 | 2.3 |
| 12 | **Add Logging Framework** | 5 | 3 | 7 | **28** | 13 | 3.3 |
| 13 | **Add Configuration Support** | 5 | 4 | 6 | **24** | 11-12 | 3.2 |
| 14 | **Disable Unknown Workflows** | 4 | 3 | 5 | **20** | 1 | 1.3 |
| 15 | **Consolidate Redundant Workflows** | 4 | 5 | 5 | **16** | 6-7 | 2.6 |
| 16 | **Add Metrics Collection** | 3 | 4 | 5 | **12** | 14-15 | 3.4 |
| 17 | **Add Performance Testing** | 4 | 5 | 4 | **12** | 18-20 | 3.7 |
| 18 | **Add Static Analysis** | 5 | 3 | 5 | **10** | 25 | - |
| 19 | **Add Pre-commit Hooks** | 5 | 2 | 4 | **10** | 28 | 5.3 |
| 20 | **Add Integration Tests** | 6 | 5 | 6 | **9** | 22-24 | - |

---

### Execution Timeline

#### Week 1 (Days 1-7): Critical Stabilization

**Day 1** (HIGH PRIORITY):
- [ ] #1: Enable branch protection (5 min)
- [ ] #3: Require PR reviews (included in #1)
- [ ] #7: Merge 3 Dependabot PRs (10 min)
- [ ] #8: Add workflow permissions (60 min)
- [ ] #14: Disable unknown workflows (30 min)

**Day 2**:
- [ ] #4: Fix release pipeline (2-3 hours)

**Day 3**:
- [ ] #11: Enable required status checks (15 min)

**Day 4**:
- [ ] #5: Add error handling (2 hours)

**Day 5**:
- [ ] #9: Add input validation (3 hours)

**Day 6-7**:
- [ ] #15: Consolidate redundant workflows (4 hours)

**Week 1 Target**: 50/100 ✅

---

#### Week 2 (Days 8-14): Quality Foundation

**Days 8-10**:
- [ ] #6: Fix test suite (8 hours total)
  - Day 8: Fix imports (2h)
  - Day 9: Create fixtures (3h)
  - Day 10: Rewrite tests (3h)

**Days 11-12**:
- [ ] #13: Add configuration support (4 hours)

**Day 13**:
- [ ] #12: Add logging framework (2 hours)

**Days 14-15**:
- [ ] #16: Add metrics collection (3 hours)

---

#### Week 3 (Days 15-21): Automation Integration

**Day 16**:
- [ ] #2: Add test execution workflow (2 hours)
- [ ] Update branch protection with test requirement (5 min)

**Day 17**:
- [ ] #10: Add coverage reporting (2 hours)

**Days 18-20**:
- [ ] #17: Add performance testing (4 hours)

**Day 21**:
- [ ] Verify Week 3 target: 75/100 ✅

---

#### Week 4-5 (Days 22-35): Production Hardening

**Days 22-24**:
- [ ] #20: Add integration tests (6 hours)

**Day 25**:
- [ ] #18: Add static analysis (mypy, ruff) (2 hours)

**Day 28**:
- [ ] #19: Add pre-commit hooks (1 hour)

**Days 29-30**:
- [ ] Re-enable and test disabled workflows (6 hours)

**Days 31-35**:
- [ ] Final polish and documentation
- [ ] Security policy
- [ ] Disaster recovery plan

**Week 5 Target**: 90/100 ✅

---

### Critical Path

```
Day 1 ─────> Day 16 ─────> Day 21 ─────> Day 35
  │             │             │             │
  ├─ Branch     ├─ Test CI    ├─ Coverage   ├─ Monitoring
  │  Protection │  Workflow   │  80%+       │  Active
  │             │             │             │
  └─> Blocks everything until complete
      (Cannot merge PRs without)
```

**Dependencies**:
- Test workflow (#2) **requires** fixed test suite (#6)
- Coverage reporting (#10) **requires** test workflow (#2)
- Required status checks (#11) **requires** test workflow (#2)
- Performance testing (#17) **requires** test suite (#6)

---

### Quick Reference Checklist

**Print this and check off as you complete:**

```
□ Day 1: Branch protection enabled
□ Day 1: Dependabot PRs merged
□ Day 1: Workflow permissions added
□ Day 2: Release pipeline fixed
□ Day 4: Error handling added
□ Day 5: Input validation added
□ Day 7: Redundant workflows consolidated
□ Day 10: Test suite fixed (60/60 passing)
□ Day 13: Logging framework added
□ Day 16: Test CI workflow added
□ Day 17: Coverage reporting enabled
□ Day 21: Verify 75/100 score
□ Day 25: Static analysis added
□ Day 30: Re-enable audited workflows
□ Day 35: Verify 90/100 score
```

---

## APPENDIX A: EMERGENCY ROLLBACK PLAN

If any fix causes critical breakage:

### Rollback Branch Protection
```bash
# Via GitHub UI:
# Settings → Branches → Delete rule for 'main'

# Via CLI:
gh api -X DELETE /repos/SamoTech/skills-tree/branches/main/protection
```

### Rollback Dependency Update
```bash
# Revert PR merge
git revert <commit-hash>
git push origin main

# Or: Roll back requirements.txt
git checkout HEAD~1 requirements.txt
git commit -m "Rollback dependency update"
git push origin main
```

### Rollback Workflow Changes
```bash
# Disable broken workflow
gh workflow disable <workflow-id>

# Or: Revert workflow file
git checkout HEAD~1 .github/workflows/<file>.yml
git commit -m "Rollback workflow changes"
git push origin main
```

---

## APPENDIX B: VALIDATION CHECKLIST

After each milestone, verify:

### Security Validation
```bash
# 1. Test branch protection
git push origin main --force
# Expected: Error

# 2. Check vulnerabilities
gh api /repos/SamoTech/skills-tree/vulnerability-alerts
# Expected: []

# 3. Verify secret scanning
gh api /repos/SamoTech/skills-tree/code-scanning/alerts
# Expected: No alerts
```

### Quality Validation
```bash
# 1. Run tests
pytest tests/ -v
# Expected: 60 passed

# 2. Check coverage
pytest --cov=tools --cov-report=term
# Expected: >= 80%

# 3. Run static analysis
mypy tools/
ruff check tools/
# Expected: No errors
```

### Automation Validation
```bash
# 1. Check workflow status
gh run list --limit 10
# Expected: Recent runs passing

# 2. Verify release
gh release list
# Expected: Recent release exists

# 3. Check CI time
gh run view <run-id>
# Expected: < 5 minutes
```

---

## SUMMARY

**This remediation plan**:
- Converts audit findings into 20 prioritized, executable fixes
- Provides detailed implementation steps for each fix
- Establishes clear milestones: 50/100 → 75/100 → 90/100
- Defines 35-day timeline to production readiness
- Includes rollback procedures for safety

**Critical Success Factors**:
1. ✅ Day 1 branch protection (non-negotiable)
2. ✅ Week 2 test suite fix (foundation for all quality)
3. ✅ Week 3 CI integration (automation baseline)
4. ✅ Week 5 monitoring (production readiness)

**Next Steps**:
1. Review this plan
2. Begin Day 1 critical fixes (2 hours total)
3. Track progress in GitHub Project
4. Update this plan as needed

---

**Plan Created**: 2026-06-14  
**Plan Owner**: Repository Maintainer  
**Review Cycle**: Weekly  
**Success Metric**: Grade A- (90/100) by Day 35  

**Status**: 🔴 **READY FOR EXECUTION**
