"""FastAPI application entry point."""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from agentforge.core.config import settings
from agentforge.core.logger import logger
from agentforge.api.routes import auth, agents, skills, tasks, admin, billing
from agentforge.skills.registry.registry import SkillRegistry
from agentforge.skills.catalog import load_all_skills

_registry: SkillRegistry | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global _registry
    logger.info('AgentForge starting', env=settings.app_env)
    _registry = SkillRegistry()
    load_all_skills(_registry)
    app.state.skill_registry = _registry
    logger.info('Skills loaded', count=len(_registry.list_all()))
    yield
    logger.info('AgentForge shutting down')


app = FastAPI(
    title='AgentForge API',
    description='Mega AI Agent Platform — 10,000+ skills, multi-agent orchestration',
    version='0.1.0',
    docs_url='/docs',
    redoc_url='/redoc',
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(auth.router,    prefix='/auth',    tags=['Auth'])
app.include_router(agents.router,  prefix='/agents',  tags=['Agents'])
app.include_router(skills.router,  prefix='/skills',  tags=['Skills'])
app.include_router(tasks.router,   prefix='/tasks',   tags=['Tasks'])
app.include_router(admin.router,   prefix='/admin',   tags=['Admin'])
app.include_router(billing.router, prefix='/billing', tags=['Billing'])


@app.get('/health', tags=['System'])
async def health():
    registry = getattr(app.state, 'skill_registry', None)
    return {
        'status': 'ok',
        'version': '0.1.0',
        'env': settings.app_env,
        'skills': len(registry.list_all()) if registry else 0,
    }
