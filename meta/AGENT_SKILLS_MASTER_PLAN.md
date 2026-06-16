# Agent Skills Canon — Master Plan

**Status:** Planning  
**Created:** 2026-06-16  
**Author:** SamoTech Architect  
**Scope:** Persistent implementation roadmap for the Agent Skills Canon project  
**Rule:** This document is a planning artefact. No production files are modified until a task from `AGENT_SKILLS_BACKLOG.md` is explicitly started.

---

## Inventory Baseline

> All counts are sourced from actual repository files as of 2026-06-16.
> Source of truth: `data/SKILLS_GRAPH.json` and `meta/GOAL_TAXONOMY.md`.

### Skills Graph (`data/SKILLS_GRAPH.json`)

| Metric | Value | Source |
|---|---|---|
| Total graph nodes | **15** | `statistics.total_nodes` |
| Total graph edges | **13** | `statistics.total_edges` |
| Average edge confidence | **0.906** | `statistics.avg_confidence` |
| Schema version | 1.3 | `schema_version` |

### Taxonomy (`meta/GOAL_TAXONOMY.md`)

| Metric | Value |
|---|---|
| Total skills declared | **361** |
| Skills mapped to goals | **287** (79.5%) |
| Skills unmapped | **74** (20.5%) |
| Goal categories | **12** (G01–G12) |
| Sub-goals | **48** |
| Required capabilities | **156** |

### Skill Files by Category

> `09-agentic-patterns` is the **only** category with a confirmed file count from a live directory listing.
> All other counts are sourced from Taxonomy section 10.2.

| Category Directory | Skill Files (excl. README) | In Graph | Gap |
|---|---|---|---|
| `01-perception` | ~42 | **0** | 42 |
| `02-reasoning` | ~38 | 1 (`prompt-engineering`) | ~37 |
| `03-memory` | ~35 | 4 (`vector-search`, `rag-retrieval`, `embedding-generation`, `context-management`) | ~31 |
| `04-action-execution` | ~28 | 1 (`error-recovery`) | ~27 |
| `05-code` | ~45 | 1 (`code-generation`) | ~44 |
| `06-communication` | unknown | **0** | unknown |
| `07-tool-use` | ~52 | 2 (`function-calling`, `api-integration`) | ~50 |
| `08-multimodal` | ~12 | **0** | 12 |
| `09-agentic-patterns` | **23** (confirmed) | 1 (`workflow-automation`) | **22** |
| `10-computer-use` | ~22 | 1 (`browser-automation`) | ~21 |
| `11-web` | unknown | 1 (`web-scraping`) | unknown |
| `12-data` | unknown | 1 (`data-extraction`) | unknown |
| `13-creative` | unknown | **0** | unknown |
| `14-security` | unknown | **0** | unknown |
| `15-orchestration` | ~18 | 2 (`llm-orchestration`, `multi-agent-coordination`) | ~16 |
| `16-domain-specific` | unknown | **0** | unknown |
| `17-infrastructure` | unknown | **0** | unknown |

### Targeted Skill Counts (for Roadmap Targets)

| Category | Actual Graph Nodes | Target After All Phases |
|---|---|---|
| Agent skills (agentic-patterns + orchestration) | 3 | 50 |
| Production skills (infrastructure + ops) | 0 | 40 |
| MCP skills (tool-use layer) | 2 | 30 |
| RAG skills (memory + retrieval) | 4 | 35 |
| Orchestration skills | 2 | 25 |
| Security & governance skills | 0 | 25 |
| **Total in graph** | **15** | **≥250** |

### Missing Categories (Not Represented in Graph at All)

1. `01-perception` — 0 nodes despite ~42 skill files
2. `06-communication` — 0 nodes, unknown file count
3. `08-multimodal` — 0 nodes despite ~12 skill files
4. `13-creative` — 0 nodes
5. `14-security` — 0 nodes (directory exists, no count)
6. `16-domain-specific` — 0 nodes
7. `17-infrastructure` — 0 nodes (critical gap for production readiness)

---

## Strategic Objectives

### North Star

Grow `SKILLS_GRAPH.json` from **15 nodes** to **≥250 nodes** across all 17 categories, while maintaining:
- avg edge confidence ≥ 0.85
- schema version compatibility
- 100% taxonomy goal coverage (G01–G12 and future G13+)
- zero phantom skills (every node in graph must have a corresponding `.md` file)

### Design Principles

1. **Graph-first**: Every skill added to `SKILLS_GRAPH.json` must have an existing or simultaneously-created `.md` file.
2. **Edge density matters**: Each new node should add ≥2 typed edges (REQUIRES, SUPPORTS, RECOMMENDED_WITH, or LEARN_BEFORE).
3. **Taxonomy-locked**: New skills must be linkable to at least one G-goal sub-goal.
4. **Stability tagging**: New skills must carry a `stability` value (`stable`, `evolving`, `experimental`, `deprecated`).
5. **No cross-phase orphans**: Phase N skills must not depend on Phase N+1 skills.

---

## Phase 1 — Core Agent Skills

**Status:** Not started  
**Target start:** Sprint C-13  
**Prerequisite:** None (baseline phase)

### Objectives

- Close the **agentic-patterns graph gap**: 22 confirmed skill files exist in `09-agentic-patterns/` with 0 corresponding graph nodes (excluding `workflow-automation`). Add all 22.
- Add the missing `02-reasoning` graph nodes (prompt chaining, CoT, ToT, ReAct, reflection, planning, self-consistency — skills that are referenced by G01–G04 but absent from the graph).
- Establish the core **perception layer** (`01-perception`) with at least 15 high-confidence nodes.
- Result: the recommendation engine can produce defensible outputs for G01 (Coding Agent) and G02 (Research Agent) goals without falling back to unmapped skills.

### Skill Count Target

| Category | Current Nodes | Add | Target |
|---|---|---|---|
| `02-reasoning` | 1 | +14 | 15 |
| `09-agentic-patterns` | 1 | +22 | 23 |
| `01-perception` | 0 | +15 | 15 |
| **Phase 1 total** | **2** | **+51** | **53** |

### Skill Files to Create

Agentic-patterns graph nodes (mapping existing `.md` files to graph):
- `skill:react-pattern` → `09-agentic-patterns/react.md`
- `skill:cot` → `09-agentic-patterns/cot.md`
- `skill:tot` → `09-agentic-patterns/tot.md`
- `skill:reflection-pattern` → `09-agentic-patterns/reflection.md`
- `skill:plan-and-execute` → `09-agentic-patterns/plan-and-execute.md`
- `skill:rag-pattern` → `09-agentic-patterns/rag.md`
- `skill:agent-as-tool` → `09-agentic-patterns/agent-as-tool.md`
- `skill:agent-handoffs` → `09-agentic-patterns/agent-handoffs.md`
- `skill:agentic-rag` → `09-agentic-patterns/agentic-rag.md`
- `skill:bootstrapping` → `09-agentic-patterns/bootstrapping.md`
- `skill:constitutional-ai` → `09-agentic-patterns/constitutional-ai.md`
- `skill:critic-agent` → `09-agentic-patterns/critic-agent.md`
- `skill:debate-pattern` → `09-agentic-patterns/debate-pattern.md`
- `skill:interruptible-agent-flows` → `09-agentic-patterns/interruptible-agent-flows.md`
- `skill:lats` → `09-agentic-patterns/lats.md`
- `skill:mcts` → `09-agentic-patterns/mcts.md`
- `skill:memory-augmented` → `09-agentic-patterns/memory-augmented.md`
- `skill:mixture-of-agents` → `09-agentic-patterns/mixture-of-agents.md`
- `skill:rag-pipeline` → `09-agentic-patterns/rag-pipeline.md`
- `skill:self-play` → `09-agentic-patterns/self-play.md`
- `skill:subagent-delegation` → `09-agentic-patterns/subagent-delegation.md`
- `skill:time-travel-debugging` → `09-agentic-patterns/time-travel-debugging.md`
- `skill:tool-use-loop` → `09-agentic-patterns/tool-use-loop.md`

New reasoning nodes (require new `.md` files in `02-reasoning/`):
- `skill:chain-of-thought` (already maps to `cot.md` pattern — needs reasoning-layer file)
- `skill:self-consistency` (new)
- `skill:tree-of-thought` (reasoning variant)
- `skill:step-back-prompting` (new)
- `skill:least-to-most` (new)
- `skill:meta-prompting` (new)
- `skill:context-engineering` (new — critical for 2026 agent landscape)
- `skill:planning-decomposition` (new)
- `skill:hypothesis-generation` (new)
- `skill:goal-decomposition` (new)
- `skill:reasoning-under-uncertainty` (new)
- `skill:analogical-reasoning` (new)
- `skill:causal-reasoning` (new)
- `skill:counterfactual-reasoning` (new)

New perception nodes (require new `.md` files in `01-perception/`):
- `skill:ocr` · `skill:screen-parsing` · `skill:ui-understanding` · `skill:vision-grounding`
- `skill:html-parsing` · `skill:structured-data-reading` · `skill:audio-transcription`
- `skill:pdf-parsing` · `skill:table-extraction` · `skill:image-classification`
- `skill:document-layout-analysis` · `skill:accessibility-tree-parsing`
- `skill:sentiment-detection` · `skill:named-entity-recognition` · `skill:intent-classification`

### Estimated Files

- `data/SKILLS_GRAPH.json`: +51 nodes, +80–90 edges
- `skills/01-perception/`: +15 new `.md` files
- `skills/02-reasoning/`: +14 new `.md` files
- `skills/09-agentic-patterns/`: 0 new files (all 23 already exist — only graph nodes added)
- `meta/GOAL_TAXONOMY.md`: update coverage metrics

**Total new files: ~29 skill files + 1 graph update**

### Dependencies

- `data/SKILLS_GRAPH.json` schema v1.3 must remain intact (no schema bump)
- `GoalTaxonomyParser` must recognise new skill IDs (add to G01–G04 mappings)
- `RecommendationEngine` re-ranking not required (new nodes are additive)

### Expected Impact

- Recommendation coverage for G01 (Coding Agent): ~60% → ~92%
- Recommendation coverage for G02 (Research Agent): ~55% → ~88%
- Graph node count: 15 → 66
- Graph edge density: 0.87 edges/node → ~2.1 edges/node
- Taxonomy unmapped skills: 74 → ~23

---

## Phase 2 — Production Agent Skills

**Status:** Not started  
**Target start:** Sprint C-15  
**Prerequisite:** Phase 1 complete (graph ≥66 nodes)

### Objectives

- Populate `17-infrastructure/` in the graph — currently **0 nodes** despite being a required category for production agents (deployment, containerisation, observability).
- Expand `07-tool-use/` from 2 nodes to 25 nodes — this category has ~52 skill files but only `function-calling` and `api-integration` are in the graph. All MCP-adjacent skills live here.
- Add the `04-action-execution/` layer beyond the single `error-recovery` node — file operations, subprocess execution, state checkpointing, retry logic.
- Add `15-orchestration/` depth beyond the 2 existing nodes — LangGraph, Mastra, Prefect, Airflow, custom DAGs.

### Skill Count Target

| Category | Current Nodes | Add | Target |
|---|---|---|---|
| `07-tool-use` | 2 | +23 | 25 |
| `17-infrastructure` | 0 | +20 | 20 |
| `04-action-execution` | 1 | +14 | 15 |
| `15-orchestration` | 2 | +13 | 15 |
| **Phase 2 total new** | **5** | **+70** | **75** |

### Key Skill Targets

**Tool Use / MCP layer** (`07-tool-use/`):
`skill:mcp-client` · `skill:mcp-server` · `skill:mcp-tool-registration`
`skill:openapi-tool-calling` · `skill:tool-schema-validation`
`skill:web-search-tool` · `skill:file-read-tool` · `skill:file-write-tool`
`skill:code-execution-tool` · `skill:shell-execution-tool`
`skill:database-query-tool` · `skill:email-send-tool` · `skill:calendar-tool`
`skill:vector-store-tool` · `skill:image-generation-tool`
`skill:tool-result-caching` · `skill:tool-timeout-handling`
`skill:parallel-tool-calling` · `skill:tool-selection` · `skill:tool-composition`
`skill:mcp-sampling` · `skill:mcp-resources` · `skill:mcp-prompts`

**Infrastructure** (`17-infrastructure/`):
`skill:docker-containerisation` · `skill:kubernetes-deployment`
`skill:github-actions-ci` · `skill:agent-health-monitoring`
`skill:distributed-tracing` · `skill:log-aggregation`
`skill:rate-limiting` · `skill:circuit-breaker` · `skill:blue-green-deployment`
`skill:secret-management` · `skill:environment-config` · `skill:agent-scaling`
`skill:latency-budgeting` · `skill:cost-tracking` · `skill:sla-enforcement`
`skill:chaos-engineering` · `skill:backup-and-restore` · `skill:api-gateway`
`skill:service-mesh` · `skill:agent-versioning`

**Action Execution** (`04-action-execution/`):
`skill:file-operations` · `skill:subprocess-execution` · `skill:state-checkpointing`
`skill:retry-with-backoff` · `skill:idempotent-actions` · `skill:action-logging`
`skill:rollback` · `skill:dry-run-mode` · `skill:action-confirmation`
`skill:parallel-execution` · `skill:execution-sandbox` · `skill:output-validation`
`skill:side-effect-tracking` · `skill:transactional-actions`

**Orchestration** (`15-orchestration/`):
`skill:langgraph` · `skill:mastra-workflows` · `skill:prefect-flows`
`skill:airflow-dags` · `skill:temporal-workflows` · `skill:event-driven-orchestration`
`skill:step-functions` · `skill:dag-construction` · `skill:conditional-branching`
`skill:fan-out-fan-in` · `skill:saga-pattern` · `skill:orchestration-monitoring`
`skill:workflow-versioning`

### Estimated Files

- `data/SKILLS_GRAPH.json`: +70 nodes, +140–160 edges
- `skills/07-tool-use/`: +23 new `.md` files
- `skills/17-infrastructure/`: +20 new `.md` files
- `skills/04-action-execution/`: +14 new `.md` files
- `skills/15-orchestration/`: +13 new `.md` files

**Total new files: ~70 skill files + 1 graph update**

### Dependencies

- Phase 1 complete — `01-perception`, `02-reasoning`, `09-agentic-patterns` graph nodes must exist
- MCP spec reading (`mcp/tools.py`) will need new tool IDs registered
- Goal taxonomy G06 (Workflow Automation) and G08 (Multi-Agent Systems) must be updated to reference new orchestration nodes

### Expected Impact

- Recommendation coverage for G06 (Workflow Automation): ~40% → ~85%
- Recommendation coverage for G08 (Multi-Agent Systems): ~30% → ~75%
- Graph node count: ~66 → ~136
- Production deployment blueprints: unlocked (require infrastructure nodes)
- MCP tool manifest: enriched with 23 callable tool skills

---

## Phase 3 — Multi-Agent Systems

**Status:** Not started  
**Target start:** Sprint C-17  
**Prerequisite:** Phase 2 complete (graph ≥136 nodes, MCP tool layer present)

### Objectives

- Deeply model the **multi-agent coordination space** beyond the single `skill:multi-agent-coordination` node currently in the graph.
- Add the **communication protocol layer** (`06-communication/`) — currently 0 graph nodes despite the directory existing. Covers agent-to-agent messaging, A2A protocol, inter-agent trust.
- Model **agent specialisation patterns**: supervisor–worker, peer-to-peer, hierarchical, swarm.
- Add **consensus and voting** skills — aggregating outputs from multiple agents.
- Model **agent memory sharing** — shared vector stores, distributed episodic memory, broadcast.

### Skill Count Target

| Category | Current Nodes | Add | Target |
|---|---|---|---|
| `15-orchestration` (multi-agent additions) | 15 | +10 | 25 |
| `06-communication` | 0 | +20 | 20 |
| `03-memory` (shared memory additions) | 4 | +11 | 15 |
| `09-agentic-patterns` (MAS patterns) | 23 | +7 | 30 |
| **Phase 3 total new** | **42** | **+48** | **90** |

### Key Skill Targets

**Communication** (`06-communication/`):
`skill:a2a-protocol` · `skill:inter-agent-messaging` · `skill:broadcast-channel`
`skill:event-bus` · `skill:agent-trust-scoring` · `skill:message-schema-validation`
`skill:async-message-queue` · `skill:pub-sub-pattern` · `skill:rpc-over-agents`
`skill:agent-discovery` · `skill:capability-advertisement` · `skill:negotiation-protocol`
`skill:delegation-contract` · `skill:result-acknowledgement` · `skill:agent-auth`
`skill:shared-scratchpad` · `skill:blackboard-pattern` · `skill:gossip-protocol`
`skill:agent-heartbeat` · `skill:conversation-history-sync`

**Multi-Agent Patterns** (new nodes in `09-agentic-patterns/`):
`skill:supervisor-worker` · `skill:hierarchical-agents` · `skill:swarm-intelligence`
`skill:voting-ensemble` · `skill:speculative-execution` · `skill:agent-parliament`
`skill:conflict-resolution-pattern`

**Shared Memory** (new nodes in `03-memory/`):
`skill:shared-vector-store` · `skill:distributed-episodic-memory`
`skill:working-memory-sync` · `skill:long-term-memory-consolidation`
`skill:memory-read-permission` · `skill:memory-write-permission`
`skill:cross-agent-context-passing` · `skill:conversation-summarisation`
`skill:knowledge-graph-memory` · `skill:temporal-memory` · `skill:forgetting-curves`

### Estimated Files

- `data/SKILLS_GRAPH.json`: +48 nodes, +100–120 edges
- `skills/06-communication/`: +20 new `.md` files
- `skills/03-memory/`: +11 new `.md` files
- `skills/09-agentic-patterns/`: +7 new `.md` files

**Total new files: ~38 skill files + 1 graph update**

### Dependencies

- Phase 2 complete — orchestration nodes (`langgraph`, `mastra-workflows`) must exist to reference from multi-agent patterns
- Goal taxonomy G08 (Multi-Agent Systems) sub-goals G08.1–G08.5 must be re-mapped to new graph nodes
- `api/routes/recommend.py` must support graph traversal depth ≥3 for multi-agent blueprints

### Expected Impact

- Recommendation coverage for G08 (Multi-Agent Systems): ~75% → ~95%
- New goal category possible: G13 (Collaborative AI Networks)
- Graph node count: ~136 → ~184
- A2A-capable blueprint generation: unlocked

---

## Phase 4 — AgentOps & LLMOps

**Status:** Not started  
**Target start:** Sprint C-19  
**Prerequisite:** Phase 3 complete (graph ≥184 nodes)

### Objectives

- Add a **dedicated evaluation layer** — currently G11 (Evaluation Systems) references 44 skills but the graph has zero evaluation nodes.
- Model **observability and tracing** at the LLM/agent level — spans, traces, cost attribution, token budgeting.
- Add **fine-tuning and RLHF** skills — increasingly required as agents are specialised for production domains.
- Model **prompt management** — prompt versioning, A/B testing prompts, prompt drift detection.
- Add **cost optimisation** skills — model routing, caching strategies, batching.

### Skill Count Target

| Category | Current Nodes | Add | Target |
|---|---|---|---|
| `11-evaluation` (new sub-category or additions) | 0 | +20 | 20 |
| `17-infrastructure` (LLMOps additions) | 20 | +10 | 30 |
| `02-reasoning` (meta-cognition additions) | 15 | +5 | 20 |
| `12-data` additions | 1 | +9 | 10 |
| **Phase 4 total new** | **36** | **+44** | **80** |

### Key Skill Targets

**Evaluation:**
`skill:llm-as-judge` · `skill:benchmark-dataset-creation` · `skill:evals-framework`
`skill:ragas-evaluation` · `skill:faithfulness-scoring` · `skill:relevance-scoring`
`skill:hallucination-detection` · `skill:regression-test-suite` · `skill:golden-dataset`
`skill:human-eval-pipeline` · `skill:model-comparison-harness` · `skill:leaderboard-tracking`
`skill:pairwise-evaluation` · `skill:critic-llm` · `skill:eval-driven-development`
`skill:safety-evaluation` · `skill:bias-detection` · `skill:toxicity-scoring`
`skill:groundedness-scoring` · `skill:agent-trajectory-evaluation`

**LLMOps / Observability:**
`skill:opentelemetry-tracing` · `skill:langfuse-observability` · `skill:arize-monitoring`
`skill:token-usage-tracking` · `skill:cost-per-query-tracking` · `skill:latency-p99-monitoring`
`skill:prompt-versioning` · `skill:prompt-ab-testing` · `skill:prompt-drift-detection`
`skill:model-routing` (e.g. route cheap queries to small models)

**Fine-Tuning / Adaptation:**
`skill:lora-fine-tuning` · `skill:rlhf-pipeline` · `skill:dpo-training`
`skill:preference-data-collection` · `skill:continual-learning`

### Estimated Files

- `data/SKILLS_GRAPH.json`: +44 nodes, +90–110 edges
- `skills/12-data/`: +9 new `.md` files
- New directory `skills/11-evaluation/` (or additions to existing 12-data): +20 new `.md` files
- `skills/17-infrastructure/`: +10 new `.md` files

**Total new files: ~44 skill files + 1 graph update**

### Dependencies

- Phase 3 complete
- Goal taxonomy G11 (Evaluation Systems) sub-goals G11.1–G11.5 must reference new evaluation nodes
- `BlueprintGenerator` must be capable of including eval skills in output blueprint
- Consideration: Does a new category `18-evaluation` or `19-llmops` need to be added to `skills/`?

### Expected Impact

- Recommendation coverage for G11 (Evaluation Systems): 0% → ~90%
- Evaluation-equipped blueprints: unlocked
- Cost-optimised deployment blueprints: unlocked
- Graph node count: ~184 → ~228

---

## Phase 5 — Security & Governance

**Status:** Not started  
**Target start:** Sprint C-21  
**Prerequisite:** Phase 4 complete (graph ≥228 nodes)

### Objectives

- Populate `14-security/` in the graph — currently **0 nodes** despite the directory existing.
- Model **prompt injection** defences, **jailbreak detection**, **output sanitisation**.
- Add **access control** and **data governance** skills for agents that access sensitive data.
- Model **audit trails**, **explainability**, and **compliance** (GDPR, HIPAA-adjacent patterns).
- Add **red-teaming** and **adversarial testing** skills.

### Skill Count Target

| Category | Current Nodes | Add | Target |
|---|---|---|---|
| `14-security` | 0 | +25 | 25 |
| `09-agentic-patterns` (safety patterns) | 30 | +5 | 35 |
| `17-infrastructure` (security additions) | 30 | +5 | 35 |
| **Phase 5 total new** | **60** | **+35** | **95** |

### Key Skill Targets

**Security (`14-security/`):**
`skill:prompt-injection-defence` · `skill:jailbreak-detection` · `skill:output-sanitisation`
`skill:pii-redaction` · `skill:data-leakage-prevention` · `skill:rbac-for-agents`
`skill:tool-call-auditing` · `skill:agent-sandboxing` · `skill:input-validation`
`skill:rate-limiting-per-user` · `skill:api-key-rotation` · `skill:secrets-scanning`
`skill:vulnerability-assessment` · `skill:threat-modelling` · `skill:red-teaming`
`skill:adversarial-robustness` · `skill:model-inversion-defence` · `skill:membership-inference-defence`
`skill:supply-chain-security` · `skill:llm-firewall`
`skill:audit-log-generation` · `skill:compliance-policy-enforcement`
`skill:explainability` · `skill:bias-mitigation` · `skill:fairness-testing`

**Safety Patterns (additions to `09-agentic-patterns/`):**
`skill:human-in-the-loop` · `skill:safe-stopping-criterion`
`skill:action-confirmation-gate` · `skill:guardrails-pattern` · `skill:self-censorship`

### Estimated Files

- `data/SKILLS_GRAPH.json`: +35 nodes, +70–90 edges
- `skills/14-security/`: +25 new `.md` files
- `skills/09-agentic-patterns/`: +5 new `.md` files
- `skills/17-infrastructure/`: +5 new `.md` files

**Total new files: ~35 skill files + 1 graph update**

### Dependencies

- Phase 4 complete
- Red-teaming skills require Phase 4 evaluation framework to exist (security evals use eval infrastructure)
- New goal G13 (Security-First Agent) may be added to taxonomy in parallel
- `constitutional-ai.md` (already in `09-agentic-patterns/`) should be linked to new security nodes

### Expected Impact

- Security-hardened blueprint generation: unlocked
- Compliance-aware agent recommendations: unlocked
- Graph node count: ~228 → ~263
- First version covering all 17 `skills/` categories: **achieved at end of Phase 5**

---

## Phase 6 — Emerging Agent Architectures

**Status:** Not started  
**Target start:** Sprint C-23  
**Prerequisite:** Phase 5 complete (graph ≥263 nodes, all 17 categories represented)

### Objectives

- Model **domain-specific agents** (`16-domain-specific/`) — finance, healthcare, legal, customer support, DevOps.
- Add **multimodal agent** skills (`08-multimodal/`) beyond the ~12 existing files — video understanding, audio generation, document Q&A.
- Model **creative agent** patterns (`13-creative/`) — content pipelines, style transfer, generative art.
- Add **frontier architectures**: cognitive architectures (ACT-R inspired), world models, long-horizon planning, self-improving agents.
- Establish a **deprecation registry** for skills that have become obsolete (e.g., older RAG patterns superseded by native retrieval).

### Skill Count Target

| Category | Current Nodes | Add | Target |
|---|---|---|---|
| `16-domain-specific` | 0 | +20 | 20 |
| `08-multimodal` | 0 | +15 | 15 |
| `13-creative` | 0 | +10 | 10 |
| Frontier (new nodes across existing categories) | varies | +20 | varies |
| **Phase 6 total new** | **0** | **+65** | **65** |

### Key Skill Targets

**Domain-Specific (`16-domain-specific/`):**
`skill:financial-analysis-agent` · `skill:code-review-agent` · `skill:legal-document-agent`
`skill:medical-triage-agent` · `skill:devops-automation-agent` · `skill:customer-support-agent`
`skill:data-analysis-agent` · `skill:research-synthesis-agent` · `skill:content-moderation-agent`
`skill:sales-qualification-agent` + 10 more vertical-specific skills

**Multimodal (`08-multimodal/`):**
`skill:video-understanding` · `skill:audio-generation` · `skill:document-qa`
`skill:chart-interpretation` · `skill:multimodal-reasoning` · `skill:cross-modal-search`
`skill:image-to-code` · `skill:speech-to-intent` · `skill:visual-agent-planning`
`skill:multimodal-embedding` + 5 more

**Creative (`13-creative/`):**
`skill:long-form-writing-agent` · `skill:style-transfer` · `skill:narrative-planning`
`skill:iterative-editing` · `skill:creative-brainstorming` · `skill:brand-voice-adaptation`
`skill:factual-grounding-in-creative` · `skill:content-pipeline-orchestration`
`skill:audience-adaptation` · `skill:multiformat-output`

**Frontier Architectures:**
`skill:world-model-agent` · `skill:self-improving-agent` · `skill:long-horizon-planning`
`skill:cognitive-architecture` · `skill:model-context-compression`
`skill:neuro-symbolic-reasoning` · `skill:active-inference-agent`
`skill:continual-self-evaluation` · `skill:emergent-capability-detection`
`skill:agent-lifecycle-management` + 10 more

### Estimated Files

- `data/SKILLS_GRAPH.json`: +65 nodes, +130–150 edges
- `skills/16-domain-specific/`: +20 new `.md` files
- `skills/08-multimodal/`: up to +3 new `.md` files (most already exist)
- `skills/13-creative/`: +10 new `.md` files
- Possible new directories: `skills/18-evaluation/`, `skills/19-frontier/`

**Total new files: ~33–45 skill files + 1 graph update + possible new directories**

### Dependencies

- Phase 5 complete
- Domain-specific skills depend on goal taxonomy expansion (G13–G16 likely)
- Frontier architecture skills are `stability: experimental` — must not be referenced by stable recommendations without a stability filter

### Expected Impact

- **All 17 `skills/` categories represented in graph**: achieved
- **Graph node count target ≥250**: achieved (~328 projected)
- Domain-specific blueprint generation: unlocked for 10+ verticals
- Frontier architecture roadmap: agents can recommend emerging patterns with appropriate confidence flags
- Full taxonomy goal coverage G01–G16+: achieved

---

## Cumulative Roadmap Summary

| Phase | Name | New Nodes | Cumulative Nodes | New Skill Files | Sprints |
|---|---|---|---|---|---|
| Baseline | Current state | — | **15** | — | — |
| **Phase 1** | Core Agent Skills | +51 | **66** | ~29 | C-13–C-14 |
| **Phase 2** | Production Agent Skills | +70 | **136** | ~70 | C-15–C-16 |
| **Phase 3** | Multi-Agent Systems | +48 | **184** | ~38 | C-17–C-18 |
| **Phase 4** | AgentOps & LLMOps | +44 | **228** | ~44 | C-19–C-20 |
| **Phase 5** | Security & Governance | +35 | **263** | ~35 | C-21–C-22 |
| **Phase 6** | Emerging Architectures | +65 | **328** | ~38–50 | C-23–C-24 |

**Target: ≥250 graph nodes by end of Phase 5 (Sprint C-22)**  
**Stretch: ~328 graph nodes by end of Phase 6 (Sprint C-24)**

---

## Risk Register

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Graph schema version bump breaks `SkillsGraph` loader | Medium | High | Pin schema to v1.3 through Phase 3; bump to v2.0 in Phase 4 with migration test |
| Skill ID collisions between phases | Low | High | All new IDs follow `skill:kebab-case` and are checked against existing graph before commit |
| `GoalTaxonomyParser` regex fails on new skill IDs | Medium | Medium | Add parser unit test for each new skill batch |
| Phantom skills (graph node without `.md` file) | Medium | High | CI check: `ast-sweep.yml` must validate every graph node has a corresponding file |
| Phase N skills depending on Phase N+1 skills | Low | High | Backlog task dependencies are explicitly declared; blocked tasks cannot be started |
| `stability: experimental` skills surfaced in stable recommendations | Medium | Medium | `RecommendationEngine` must filter by stability unless `include_experimental=true` |
| Taxonomy goal coverage drops below 79.5% during expansion | Low | Medium | Coverage check added to `quality-report.yml` |

---

## Maintenance Rules

1. **This file is never auto-generated** — it is the human-readable strategic layer.
2. **Counts must be kept accurate** — update the Inventory Baseline table after every phase completes.
3. **Phase completion criteria**: A phase is complete when (a) all its backlog tasks are `DONE`, (b) the graph node count has reached the phase target, and (c) `quality-report.yml` passes on main.
4. **No phase may be started while a previous phase has open blockers**.
5. **Deprecation**: when a skill becomes obsolete, add `"stability": "deprecated"` to the graph node and add a `deprecated_at` field — do not delete nodes.

---

*Roadmap version: 1.0.0 — Created 2026-06-16 — No production files modified.*
