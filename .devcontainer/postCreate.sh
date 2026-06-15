#!/usr/bin/env bash
set -euo pipefail

echo ""
echo "🌳 Skills Tree Architect — Codespaces Setup"
echo "=========================================="

# ---- 1. Install package (editable + dev extras) --------------------------
echo ""
echo "📦 Installing package..."
pip install -e '.[dev]' --quiet

# ---- 2. Verify CLI --------------------------------------------------------
echo ""
echo "🛠  Verifying CLI..."
skills-tree --version 2>/dev/null || true
skills-tree validate

# ---- 3. Smoke-test API layer ---------------------------------------------
echo ""
echo "🌐 Smoke-testing API layer..."
python - <<'PYEOF'
from fastapi.testclient import TestClient
from api.main import app
client = TestClient(app)
r = client.get("/health")
assert r.status_code == 200, f"Health check failed: {r.status_code}"
print(f"  /health          ✅  {r.json()}")
r2 = client.get("/goals")
assert r2.status_code == 200
print(f"  /goals           ✅  {len(r2.json()['goals'])} goals loaded")
r3 = client.get("/skills")
assert r3.status_code == 200
print(f"  /skills          ✅  {len(r3.json()['skills'])} skills loaded")
r4 = client.post("/recommend", json={"goal": "Coding Agent", "experience": "intermediate"})
assert r4.status_code == 200
print(f"  /recommend       ✅  goal_id={r4.json()['goal_id']} confidence={r4.json()['confidence_score']}")
print("")
print("✅ All API smoke tests passed.")
PYEOF

# ---- 4. Run test suite ---------------------------------------------------
echo ""
echo "🧪 Running test suite..."
pytest tests/ -q --tb=no 2>&1 | tail -5

# ---- 5. Print welcome ----------------------------------------------------
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🌳 Skills Tree Architect is ready!"
echo ""
echo "  Quick commands:"
echo "    skills-tree recommend --goal \"Coding Agent\""
echo "    skills-tree blueprint --goal \"Coding Agent\""
echo "    skills-tree goals"
echo "    skills-tree validate"
echo ""
echo "  Start API server:"
echo "    uvicorn api.main:app --reload"
echo "    → Swagger UI at http://localhost:8000/docs"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
