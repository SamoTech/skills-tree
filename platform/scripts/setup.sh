#!/usr/bin/env bash
set -euo pipefail

echo "🤖 AgentForge Setup"
echo "==================="

# Check Python
if ! command -v python3.11 &>/dev/null; then
  echo "❌ Python 3.11+ required"; exit 1
fi

# Check Docker
if ! command -v docker &>/dev/null; then
  echo "❌ Docker required"; exit 1
fi

# Copy env
[ ! -f .env ] && cp .env.example .env && echo "✅ .env created — fill in your API keys"

# Install Python deps
pip install -e '.[dev]' --quiet
echo "✅ Python deps installed"

# Start Docker services
docker compose -f docker/docker-compose.yml up -d postgres redis chroma
echo "✅ Postgres, Redis, Chroma started"

# Wait for Postgres
echo "⏳ Waiting for Postgres..."
until docker compose -f docker/docker-compose.yml exec -T postgres pg_isready -U agentforge &>/dev/null; do
  sleep 1
done
echo "✅ Postgres ready"

# Run migrations
alembic upgrade head
echo "✅ Database migrated"

# Install frontend deps
if command -v npm &>/dev/null; then
  cd frontend && npm install --silent && cd ..
  echo "✅ Frontend deps installed"
fi

echo ""
echo "🎉 Setup complete!"
echo "  API:      uvicorn agentforge.api.main:app --reload"
echo "  Frontend: cd frontend && npm run dev"
echo "  CLI:      agentforge --help"
