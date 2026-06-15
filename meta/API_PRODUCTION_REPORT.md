# API Production Report

Sprint: **C-12.75** | Service: Architect FastAPI

---

## Test Methodology

All latency figures are measured via `time.perf_counter()` inside the GitHub Actions runner using `fastapi.testclient.TestClient`, which exercises the full request-response cycle including Pydantic validation and engine execution — without network overhead. These represent floor-level latency.

For real HTTP server latency (uvicorn), add ~1–3ms per request.

---

## Endpoint Benchmarks

| Method | Endpoint | Expected Status | Expected Latency | Response Size |
|---|---|---|---|---|
| GET | `/health` | 200 | < 5 ms | ~60 B |
| GET | `/goals` | 200 | < 20 ms | ~800 B |
| GET | `/skills` | 200 | < 20 ms | ~1.2 KB |
| POST | `/recommend` | 200 | < 50 ms | ~1.8 KB |
| POST | `/blueprint` | 200 | < 60 ms | ~2.1 KB |

See live measurements in the `clean-install-evidence-<run>` artifact (`api_results.json`).

---

## Response Schema Validation

### GET /health
```json
{ "status": "ok", "version": "1.0" }
```

### GET /goals
```json
{
  "goals": [
    { "id": "G01", "name": "Coding Agent", "description": "..." },
    ...
  ]
}
```

### POST /recommend
```json
{
  "goal": "Coding Agent",
  "goal_id": "G01",
  "confidence_score": 0.86,
  "required_skills": [...],
  "optional_skills": [...],
  "learning_path": [...],
  "calibration_applied": true
}
```

### POST /blueprint
```json
{
  "id": "blueprint-...",
  "title": "Coding Agent",
  "goal_id": "G01",
  "architecture_type": "Single-Agent",
  "confidence_score": 0.86,
  "required_skills": [...],
  "learning_path": [...],
  "risks": [...]
}
```

---

## Error Rate

| Condition | Expected Behavior |
|---|---|
| Valid request | 200 OK, < 60 ms |
| Unknown goal | 404, `{"detail": "Goal not found: ..."}` |
| Missing required field | 422 Unprocessable Entity |
| Internal engine error | 500 + structured error |

Error rate on valid inputs: **0%** (enforced by CI).

---

## Local Server

```bash
uvicorn api.main:app --reload --port 8000
# Swagger UI: http://localhost:8000/docs
# ReDoc:      http://localhost:8000/redoc
```

Expected startup time: < 2 seconds. The engine loads taxonomy and graph on first request (lazy init) or on startup depending on `api/dependencies.py` implementation.

---

## Evidence

All endpoint responses captured in `api_results.json` artifact from CI run. Download from:
```
https://github.com/SamoTech/skills-tree/actions/workflows/clean-install-test.yml
```
