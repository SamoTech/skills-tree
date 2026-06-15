# First Run Experience

Sprint: **C-12** | Fresh machine workflow

---

## Installation

```bash
pip install skills-tree
```

Expected output:
```
Successfully installed skills-tree-1.0.0
```

---

## skills-tree validate

```bash
skills-tree validate
```

Expected output:
```json
{
  "status": "ok",
  "checks": {
    "health":  { "status_code": 200, "pass": true, "body": { "status": "ok", "version": "1.0" } },
    "goals":   { "status_code": 200, "pass": true, "goal_count": 11 },
    "skills":  { "status_code": 200, "pass": true, "skill_count": 12 }
  },
  "status": "ok",
  "all_pass": true
}
```

---

## skills-tree goals

```bash
skills-tree goals
```

Expected output (truncated):
```json
[
  { "id": "G01", "name": "Coding Agent" },
  { "id": "G02", "name": "Browser Agent" },
  { "id": "G03", "name": "Memory Agent" },
  { "id": "G04", "name": "RAG Assistant" },
  ...
]
```

---

## skills-tree recommend

```bash
skills-tree recommend --goal "Coding Agent"
```

Expected output:
```json
{
  "goal": "Coding Agent",
  "goal_id": "G01",
  "confidence_score": 0.86,
  "required_skills": [
    { "id": "skill:prompt-engineering",  "name": "Prompt Engineering",  "rank": 1 },
    { "id": "skill:code-generation",      "name": "Code Generation",      "rank": 2 },
    { "id": "skill:function-calling",     "name": "Function Calling",     "rank": 3 },
    { "id": "skill:error-recovery",       "name": "Error Recovery",       "rank": 4 },
    { "id": "skill:context-management",   "name": "Context Management",   "rank": 5 }
  ],
  "optional_skills": [ ... ],
  "learning_path": [ "Prompt Engineering", "Code Generation", "Function Calling", ... ],
  "deployment": "cloud",
  "complexity": "Intermediate",
  "estimated_learn_hours": 96,
  "calibration_applied": true
}
```

---

## skills-tree blueprint

```bash
skills-tree blueprint --goal "Coding Agent"
```

Expected output:
```json
{
  "id": "blueprint-20260615143000",
  "title": "Coding Agent",
  "goal": "Coding Agent",
  "goal_id": "G01",
  "confidence_score": 0.86,
  "architecture_type": "Single-Agent",
  "required_skills": [ ... ],
  "optional_skills": [ ... ],
  "learning_path": [ "Prompt Engineering", "Code Generation", "Function Calling" ],
  "risks": [ "LLM hallucination in code output", "Tool call error handling" ]
}
```

---

## Time to First Use

| Step | Estimated Time |
|---|---|
| `pip install skills-tree` | ~15 seconds |
| `skills-tree validate` | ~3 seconds |
| `skills-tree recommend --goal "Coding Agent"` | ~2 seconds |
| `skills-tree blueprint --goal "Coding Agent"` | ~2 seconds |
| **Total** | **< 25 seconds** |

Time to First Use: **< 30 seconds** from a machine with Python 3.11+ installed.
