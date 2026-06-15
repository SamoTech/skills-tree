# Clean Install Report

Sprint: **C-12.75** | Environment: GitHub Actions `ubuntu-latest` + Python 3.12 (no cache)

---

## Test Environment

| Property | Value |
|---|---|
| OS | `ubuntu-latest` (GitHub-hosted runner) |
| Python | 3.12 (no pip cache — true clean install) |
| Starting state | Fresh runner, no prior packages |
| Clone method | `actions/checkout@v4` |
| Install command | `pip install -e .` |

---

## How to Reproduce

All evidence is machine-generated on every push to `main`. To reproduce manually:

1. Go to [Actions → C-12.75 Clean Install Test](https://github.com/SamoTech/skills-tree/actions/workflows/clean-install-test.yml)
2. Click **Run workflow**
3. Inspect the **Step Summary** and download the **clean-install-evidence** artifact

Or locally on a fresh machine:

```bash
git clone https://github.com/SamoTech/skills-tree.git
cd skills-tree
pip install -e .
skills-tree validate
```

---

## Expected Execution Timeline

| Step | Expected Duration |
|---|---|
| `git clone` | < 5 s |
| `pip install -e .` (cold, no cache) | 30–60 s |
| `skills-tree validate` | < 3 s |
| `skills-tree recommend --goal "Coding Agent"` | < 2 s |
| `pytest tests/ -q` | < 10 s |
| **Total time to working product** | **< 75 seconds** |

---

## Expected Outputs

### skills-tree validate

```json
{
  "status": "ok",
  "checks": {
    "health":  { "status_code": 200, "pass": true },
    "goals":   { "status_code": 200, "pass": true, "goal_count": 11 },
    "skills":  { "status_code": 200, "pass": true, "skill_count": 12 }
  },
  "all_pass": true
}
```

### skills-tree recommend --goal "Coding Agent"

```json
{
  "goal": "Coding Agent",
  "goal_id": "G01",
  "confidence_score": 0.86,
  "required_skills": [ ... ],
  "calibration_applied": true
}
```

---

## Evidence Location

All runtime evidence (logs, JSON outputs, test results) is uploaded as a GitHub Actions artifact named `clean-install-evidence-<run_number>` and retained for 90 days. Download at:

```
https://github.com/SamoTech/skills-tree/actions/workflows/clean-install-test.yml
```

---

## Known Pre-conditions

| Requirement | Status |
|---|---|
| Python ≥ 3.11 | Must be installed on target machine |
| `pip` available | Standard with Python 3.11+ |
| Internet access | Required only for `pip install` |
| API keys | None required |
| External services | None |

**Zero manual fixes required** for any pre-condition beyond Python 3.11+ being installed.
