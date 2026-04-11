# 🤖 AgentForge — Mega AI Agent Platform

Production-ready, scalable AI agent platform with 10,000+ modular skills, multi-agent orchestration, persistent memory, and SaaS infrastructure.

## ✨ Features

- **10,000+ Modular Skills** — plugin-style, dynamically loaded, searchable registry
- **Multi-Agent Orchestration** — Planner, Executor, Specialist, Memory agents
- **Multi-Framework** — LangChain, AutoGen, CrewAI, LlamaIndex, OpenAI SDK adapters
- **Persistent Memory** — Short-term (Redis), Long-term (ChromaDB/FAISS), Team-shared
- **SaaS-Ready** — JWT auth, Stripe billing, usage tracking, admin dashboard
- **CLI Tool** — `agentforge` command for managing agents, skills, tasks
- **Auto-Skill Generator** — LLM generates new skill modules on demand

## 🗂️ Structure

```
platform/
├── agentforge/              # Python backend package
│   ├── api/                 # FastAPI routes
│   ├── agents/              # Agent roles (planner, executor, specialist, memory)
│   ├── skills/              # Skill system (base, registry, 10+ catalog skills)
│   ├── orchestrator/        # Central task orchestrator
│   ├── core/memory/         # Short/long-term/team memory
│   ├── frameworks/          # LangChain, AutoGen, CrewAI adapters
│   ├── auth/                # JWT auth
│   ├── billing/             # Stripe integration
│   ├── db/                  # SQLAlchemy models + migrations
│   └── cli/                 # CLI tool
├── frontend/                # Next.js 14 dashboard
├── docker/                  # Docker Compose stack
└── scripts/                 # Setup & deployment scripts
```

## 🚀 Quick Start

```bash
# 1. Clone & enter
cd platform/

# 2. Setup environment
cp .env.example .env
# Edit .env with your API keys

# 3. Start all services
docker compose -f docker/docker-compose.yml up -d

# 4. Install Python deps
pip install -e ".[dev]"

# 5. Run migrations
alembic upgrade head

# 6. Start API
uvicorn agentforge.api.main:app --reload

# 7. Start frontend
cd frontend && npm install && npm run dev
```

## 📡 API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/auth/register` | Register user |
| POST | `/auth/login` | Get JWT token |
| GET | `/skills/` | List all skills |
| POST | `/skills/search` | Search skills by query |
| GET | `/agents/` | List user agents |
| POST | `/agents/` | Create agent |
| POST | `/tasks/` | Submit task |
| GET | `/tasks/{id}` | Get task result |
| GET | `/admin/stats` | Platform stats |
| POST | `/billing/checkout` | Create Stripe checkout |

## 🧠 Skill System

Every skill is a Python class inheriting `BaseSkill`:

```python
from agentforge.skills.base import BaseSkill, SkillInput, SkillOutput

class MySkill(BaseSkill):
    name = "my_skill"
    description = "Does something useful"
    category = "custom"
    tags = ["example"]
    input_schema = {"query": {"type": "string", "required": True}}
    output_schema = {"result": {"type": "string"}}

    async def execute(self, inp: SkillInput) -> SkillOutput:
        return SkillOutput(result=f"Processed: {inp.data['query']}")
```

Register it:
```bash
agentforge skills register path/to/my_skill.py
```

## 💰 Pricing Tiers

| Plan | Price | Agents | Skills/mo | API Calls/mo |
|------|-------|--------|-----------|---------------|
| Free | $0 | 2 | 100 | 1,000 |
| Pro | $29/mo | 10 | 1,000 | 50,000 |
| Teams | $99/mo | 50 | 10,000 | 500,000 |
| Enterprise | Custom | Unlimited | Unlimited | Unlimited |

## 📄 License

MIT © Ossama Hashim
