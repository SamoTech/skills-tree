# Agent Skills Canon — Backlog

**Status:** Active  
**Created:** 2026-06-16  
**Owner:** SamoTech Architect  
**Rule:** Each task is atomic. One task = one PR. No task modifies production files until explicitly started.

---

## Task Status Legend

| Status | Meaning |
|---|---|
| `OPEN` | Ready to be started; all dependencies met |
| `BLOCKED` | Cannot start; depends on another task |
| `IN PROGRESS` | A PR is open for this task |
| `DONE` | Merged and verified |
| `CANCELLED` | Decided not to implement |

---

## Phase 1 — Core Agent Skills

### TASK-001

**Title:** Map existing `09-agentic-patterns/` files to graph nodes  
**Status:** `OPEN`  
**Phase:** 1  
**Category:** `09-agentic-patterns`  
**Depends on:** None  
**Estimated graph changes:** +22 nodes, +44–55 edges in `SKILLS_GRAPH.json`  
**Files touched:** `data/SKILLS_GRAPH.json` only  
**Description:**  
All 23 skill `.md` files in `skills/09-agentic-patterns/` exist but only `skill:workflow-automation` is present in the graph. Add graph nodes for the remaining 22 files:
`react`, `cot`, `tot`, `reflection`, `plan-and-execute`, `rag`, `agent-as-tool`, `agent-handoffs`, `agentic-rag`, `bootstrapping`, `constitutional-ai`, `critic-agent`, `debate-pattern`, `interruptible-agent-flows`, `lats`, `mcts`, `memory-augmented`, `mixture-of-agents`, `rag-pipeline`, `self-play`, `subagent-delegation`, `time-travel-debugging`, `tool-use-loop`.  
Each node must include: `id`, `type`, `name`, `category`, `level`, `stability`, `centrality`.  
Each node must have ≥2 typed edges connecting it to existing or co-added nodes.  
**Acceptance criteria:**  
- `statistics.total_nodes` in graph increases by exactly 22  
- All 22 new IDs follow `skill:kebab-case` convention  
- `ast-sweep.yml` passes (every new node maps to an existing `.md` file)

---

### TASK-002

**Title:** Add Context Engineering skills  
**Status:** `OPEN`  
**Phase:** 1  
**Category:** `02-reasoning`  
**Depends on:** None  
**Estimated graph changes:** +5 nodes, +10–12 edges  
**Files touched:** `data/SKILLS_GRAPH.json`, `skills/02-reasoning/context-engineering.md`, `skills/02-reasoning/context-window-management.md`, `skills/02-reasoning/prompt-chaining.md`, `skills/02-reasoning/few-shot-selection.md`, `skills/02-reasoning/system-prompt-design.md`  
**Description:**  
Context engineering is the 2026 evolution of prompt engineering — it covers how agents manage, compress, and inject context across long sessions. Add 5 new skill files and corresponding graph nodes.  
**Acceptance criteria:**  
- 5 new `.md` files created with valid frontmatter (`id`, `name`, `category`, `level`, `stability`, `learn_time_hrs`)  
- 5 new graph nodes added  
- At least 3 edges connecting new nodes to `skill:prompt-engineering` and each other  
- `meta/GOAL_TAXONOMY.md` updated: G01 and G02 sub-goal skill lists reference new node IDs

---

### TASK-003

**Title:** Add chain-of-thought and advanced reasoning skills to graph  
**Status:** `OPEN`  
**Phase:** 1  
**Category:** `02-reasoning`  
**Depends on:** None (parallel with TASK-002)  
**Estimated graph changes:** +9 nodes, +18–22 edges  
**Files touched:** `data/SKILLS_GRAPH.json`, 9 new `.md` files in `skills/02-reasoning/`  
**Description:**  
Add: `self-consistency`, `step-back-prompting`, `least-to-most`, `meta-prompting`, `planning-decomposition`, `hypothesis-generation`, `goal-decomposition`, `reasoning-under-uncertainty`, `analogical-reasoning`.  
**Acceptance criteria:**  
- 9 new `.md` files, 9 new graph nodes  
- Each new node linked to `skill:prompt-engineering` via `LEARN_BEFORE` or `REQUIRES`  
- `stability` values: `self-consistency` → `stable`; `least-to-most` → `stable`; `step-back-prompting` → `evolving`; rest → as appropriate

---

### TASK-004

**Title:** Add causal and counterfactual reasoning skills  
**Status:** `OPEN`  
**Phase:** 1  
**Category:** `02-reasoning`  
**Depends on:** TASK-003 (causal reasoning builds on basic reasoning nodes)  
**Estimated graph changes:** +3 nodes, +6–8 edges  
**Files touched:** `data/SKILLS_GRAPH.json`, `skills/02-reasoning/causal-reasoning.md`, `skills/02-reasoning/counterfactual-reasoning.md`, `skills/02-reasoning/abductive-reasoning.md`  
**Acceptance criteria:**  
- 3 new `.md` files, 3 new graph nodes  
- `causal-reasoning` has `REQUIRES` edge to `hypothesis-generation` (from TASK-003)

---

### TASK-005

**Title:** Add core perception skills (OCR, screen parsing, UI understanding)  
**Status:** `OPEN`  
**Phase:** 1  
**Category:** `01-perception`  
**Depends on:** None  
**Estimated graph changes:** +6 nodes, +12–15 edges  
**Files touched:** `data/SKILLS_GRAPH.json`, 6 new `.md` files in `skills/01-perception/`  
**Description:**  
Add: `ocr`, `screen-parsing`, `ui-understanding`, `vision-grounding`, `html-parsing`, `accessibility-tree-parsing`.  
These are required by G03 (Browser Agent) and currently completely absent from the graph.  
**Acceptance criteria:**  
- 6 new `.md` files created  
- `skill:screen-parsing` has `REQUIRES` edge to `skill:browser-automation` (already in graph)  
- `skill:ocr` has `RECOMMENDED_WITH` edge to `skill:screen-parsing`

---

### TASK-006

**Title:** Add document and data perception skills  
**Status:** `OPEN`  
**Phase:** 1  
**Category:** `01-perception`  
**Depends on:** TASK-005 (builds on perception layer)  
**Estimated graph changes:** +9 nodes, +15–18 edges  
**Files touched:** `data/SKILLS_GRAPH.json`, 9 new `.md` files in `skills/01-perception/`  
**Description:**  
Add: `pdf-parsing`, `table-extraction`, `image-classification`, `document-layout-analysis`, `structured-data-reading`, `audio-transcription`, `sentiment-detection`, `named-entity-recognition`, `intent-classification`.  
**Acceptance criteria:**  
- 9 new `.md` files, 9 new graph nodes  
- `intent-classification` linked to `skill:embedding-generation` via `RECOMMENDED_WITH`

---

### TASK-007

**Title:** Update GOAL_TAXONOMY.md coverage metrics after Phase 1  
**Status:** `BLOCKED` (by TASK-001, TASK-002, TASK-003, TASK-004, TASK-005, TASK-006)  
**Phase:** 1  
**Category:** meta  
**Depends on:** All Phase 1 tasks  
**Files touched:** `meta/GOAL_TAXONOMY.md` only  
**Description:**  
Update sections 10.1 and 10.2 with real post-Phase-1 counts. Update skill mappings for G01, G02, G03 to reference new node IDs.  
**Acceptance criteria:**  
- `total_nodes` in taxonomy matches `SKILLS_GRAPH.json statistics.total_nodes`  
- Coverage percentage recalculated  
- G01.1, G01.4, G02.1, G03.1 skill tables updated

---

## Phase 2 — Production Agent Skills

### TASK-008

**Title:** Add MCP client and server skills  
**Status:** `BLOCKED` (by Phase 1 completion)  
**Phase:** 2  
**Category:** `07-tool-use`  
**Depends on:** TASK-001 (agent-as-tool pattern must be in graph first)  
**Estimated graph changes:** +5 nodes, +10–12 edges  
**Files touched:** `data/SKILLS_GRAPH.json`, `skills/07-tool-use/mcp-client.md`, `skills/07-tool-use/mcp-server.md`, `skills/07-tool-use/mcp-tool-registration.md`, `skills/07-tool-use/mcp-sampling.md`, `skills/07-tool-use/mcp-resources.md`  
**Description:**  
MCP (Model Context Protocol) is the primary tool-calling standard as of 2026. Add 5 foundational MCP skill nodes. These are referenced by `mcp/tools.py` and should map to `dispatch_tool` callable actions.  
**Acceptance criteria:**  
- 5 new `.md` files, 5 new graph nodes  
- `skill:mcp-client` has `REQUIRES` edge to `skill:function-calling` (already in graph)  
- `skill:mcp-server` has `REQUIRES` edge to `skill:api-integration` (already in graph)  
- `mcp/tools.py` tool list (recommend_skills, generate_blueprint, list_goals, list_skills) referenced in `mcp-client.md` as usage examples

---

### TASK-009

**Title:** Add MCP advanced skills (prompts, resources, sampling)  
**Status:** `BLOCKED` (by TASK-008)  
**Phase:** 2  
**Category:** `07-tool-use`  
**Depends on:** TASK-008  
**Estimated graph changes:** +3 nodes, +6–8 edges  
**Files touched:** `data/SKILLS_GRAPH.json`, `skills/07-tool-use/mcp-prompts.md`, `skills/07-tool-use/mcp-resources-advanced.md`, `skills/07-tool-use/mcp-protocol-versioning.md`  
**Acceptance criteria:**  
- 3 new `.md` files, 3 new graph nodes with `stability: evolving`

---

### TASK-010

**Title:** Add tool composition and parallel tool calling skills  
**Status:** `BLOCKED` (by TASK-008)  
**Phase:** 2  
**Category:** `07-tool-use`  
**Depends on:** TASK-008  
**Estimated graph changes:** +5 nodes, +10–12 edges  
**Files touched:** `data/SKILLS_GRAPH.json`, 5 new `.md` files  
**Description:**  
Add: `parallel-tool-calling`, `tool-selection`, `tool-composition`, `tool-result-caching`, `tool-timeout-handling`.  
**Acceptance criteria:** 5 nodes, all linked to `skill:function-calling`

---

### TASK-011

**Title:** Add domain-specific tool skills (database, email, calendar, code execution)  
**Status:** `BLOCKED` (by TASK-008)  
**Phase:** 2  
**Category:** `07-tool-use`  
**Depends on:** TASK-008  
**Estimated graph changes:** +10 nodes, +20–24 edges  
**Files touched:** `data/SKILLS_GRAPH.json`, 10 new `.md` files in `skills/07-tool-use/`  
**Description:**  
Add: `web-search-tool`, `file-read-tool`, `file-write-tool`, `code-execution-tool`, `shell-execution-tool`, `database-query-tool`, `email-send-tool`, `calendar-tool`, `vector-store-tool`, `image-generation-tool`.  
**Acceptance criteria:** 10 nodes, all have `stability: stable` or `evolving`

---

### TASK-012

**Title:** Add action execution skills (file ops, subprocess, state checkpointing)  
**Status:** `BLOCKED` (by Phase 1 completion)  
**Phase:** 2  
**Category:** `04-action-execution`  
**Depends on:** TASK-001  
**Estimated graph changes:** +8 nodes, +16–20 edges  
**Files touched:** `data/SKILLS_GRAPH.json`, 8 new `.md` files in `skills/04-action-execution/`  
**Description:**  
Add: `file-operations`, `subprocess-execution`, `state-checkpointing`, `retry-with-backoff`, `idempotent-actions`, `action-logging`, `rollback`, `dry-run-mode`.  
**Acceptance criteria:** `state-checkpointing` has `REQUIRES` edge to `skill:error-recovery`

---

### TASK-013

**Title:** Add action validation and sandboxing skills  
**Status:** `BLOCKED` (by TASK-012)  
**Phase:** 2  
**Category:** `04-action-execution`  
**Depends on:** TASK-012  
**Estimated graph changes:** +6 nodes, +12–14 edges  
**Files touched:** `data/SKILLS_GRAPH.json`, 6 new `.md` files  
**Description:**  
Add: `action-confirmation`, `parallel-execution`, `execution-sandbox`, `output-validation`, `side-effect-tracking`, `transactional-actions`.  
**Acceptance criteria:** `execution-sandbox` has `REQUIRES` edge to `skill:dry-run-mode`

---

### TASK-014

**Title:** Add infrastructure skills (Docker, Kubernetes, CI/CD)  
**Status:** `BLOCKED` (by Phase 1 completion)  
**Phase:** 2  
**Category:** `17-infrastructure`  
**Depends on:** TASK-001  
**Estimated graph changes:** +6 nodes, +10–12 edges  
**Files touched:** `data/SKILLS_GRAPH.json`, 6 new `.md` files in `skills/17-infrastructure/`  
**Description:**  
Add: `docker-containerisation`, `kubernetes-deployment`, `github-actions-ci`, `agent-health-monitoring`, `distributed-tracing`, `log-aggregation`.  
**Acceptance criteria:** All 6 nodes have `stability: stable`

---

### TASK-015

**Title:** Add infrastructure resiliency skills (circuit breaker, rate limiting, scaling)  
**Status:** `BLOCKED` (by TASK-014)  
**Phase:** 2  
**Category:** `17-infrastructure`  
**Depends on:** TASK-014  
**Estimated graph changes:** +7 nodes, +14–18 edges  
**Files touched:** `data/SKILLS_GRAPH.json`, 7 new `.md` files  
**Description:**  
Add: `rate-limiting`, `circuit-breaker`, `blue-green-deployment`, `secret-management`, `agent-scaling`, `latency-budgeting`, `cost-tracking`.  
**Acceptance criteria:** `circuit-breaker` has `REQUIRED_WITH` edge to `skill:error-recovery`

---

### TASK-016

**Title:** Add advanced infrastructure skills (chaos, backup, API gateway, versioning)  
**Status:** `BLOCKED` (by TASK-015)  
**Phase:** 2  
**Category:** `17-infrastructure`  
**Depends on:** TASK-015  
**Estimated graph changes:** +7 nodes, +12–14 edges  
**Files touched:** `data/SKILLS_GRAPH.json`, 7 new `.md` files  
**Description:**  
Add: `sla-enforcement`, `chaos-engineering`, `backup-and-restore`, `api-gateway`, `service-mesh`, `agent-versioning`, `environment-config`.  

---

### TASK-017

**Title:** Add LangGraph and Mastra orchestration skills  
**Status:** `BLOCKED` (by Phase 1 completion)  
**Phase:** 2  
**Category:** `15-orchestration`  
**Depends on:** TASK-001  
**Estimated graph changes:** +5 nodes, +10–12 edges  
**Files touched:** `data/SKILLS_GRAPH.json`, 5 new `.md` files in `skills/15-orchestration/`  
**Description:**  
Add: `langgraph`, `mastra-workflows`, `dag-construction`, `conditional-branching`, `event-driven-orchestration`.  
**Acceptance criteria:** Both `langgraph` and `mastra-workflows` have `REQUIRES` edge to `skill:llm-orchestration`

---

### TASK-018

**Title:** Add enterprise and advanced orchestration skills  
**Status:** `BLOCKED` (by TASK-017)  
**Phase:** 2  
**Category:** `15-orchestration`  
**Depends on:** TASK-017  
**Estimated graph changes:** +8 nodes, +16–20 edges  
**Files touched:** `data/SKILLS_GRAPH.json`, 8 new `.md` files  
**Description:**  
Add: `prefect-flows`, `airflow-dags`, `temporal-workflows`, `fan-out-fan-in`, `saga-pattern`, `orchestration-monitoring`, `workflow-versioning`, `step-functions`.  

---

### TASK-019

**Title:** Update GOAL_TAXONOMY.md coverage metrics after Phase 2  
**Status:** `BLOCKED` (by TASK-008 through TASK-018)  
**Phase:** 2  
**Category:** meta  
**Depends on:** All Phase 2 tasks  
**Files touched:** `meta/GOAL_TAXONOMY.md` only  
**Description:**  
Update sections 10.1 and 10.2. Update G06 (Workflow Automation) and G08 (Multi-Agent Systems) skill mappings.

---

## Phase 3 — Multi-Agent Systems

### TASK-020

**Title:** Add A2A protocol and inter-agent messaging skills  
**Status:** `BLOCKED` (by Phase 2 completion)  
**Phase:** 3  
**Category:** `06-communication`  
**Depends on:** TASK-017 (orchestration layer must exist)  
**Estimated graph changes:** +8 nodes, +16–20 edges  
**Files touched:** `data/SKILLS_GRAPH.json`, 8 new `.md` files in `skills/06-communication/`  
**Description:**  
Add: `a2a-protocol`, `inter-agent-messaging`, `broadcast-channel`, `event-bus`, `agent-trust-scoring`, `message-schema-validation`, `async-message-queue`, `pub-sub-pattern`.  

---

### TASK-021

**Title:** Add agent discovery and negotiation communication skills  
**Status:** `BLOCKED` (by TASK-020)  
**Phase:** 3  
**Category:** `06-communication`  
**Depends on:** TASK-020  
**Estimated graph changes:** +12 nodes, +24–28 edges  
**Files touched:** `data/SKILLS_GRAPH.json`, 12 new `.md` files  
**Description:**  
Add: `rpc-over-agents`, `agent-discovery`, `capability-advertisement`, `negotiation-protocol`, `delegation-contract`, `result-acknowledgement`, `agent-auth`, `shared-scratchpad`, `blackboard-pattern`, `gossip-protocol`, `agent-heartbeat`, `conversation-history-sync`.  

---

### TASK-022

**Title:** Add multi-agent coordination patterns (supervisor, swarm, voting)  
**Status:** `BLOCKED` (by TASK-020)  
**Phase:** 3  
**Category:** `09-agentic-patterns`  
**Depends on:** TASK-020  
**Estimated graph changes:** +7 nodes, +14–18 edges  
**Files touched:** `data/SKILLS_GRAPH.json`, 7 new `.md` files  
**Description:**  
Add: `supervisor-worker`, `hierarchical-agents`, `swarm-intelligence`, `voting-ensemble`, `speculative-execution`, `agent-parliament`, `conflict-resolution-pattern`.  
**Acceptance criteria:** `supervisor-worker` has `REQUIRES` edge to `skill:multi-agent-coordination`

---

### TASK-023

**Title:** Add shared and distributed memory skills  
**Status:** `BLOCKED` (by TASK-020)  
**Phase:** 3  
**Category:** `03-memory`  
**Depends on:** TASK-020  
**Estimated graph changes:** +11 nodes, +22–26 edges  
**Files touched:** `data/SKILLS_GRAPH.json`, 11 new `.md` files in `skills/03-memory/`  
**Description:**  
Add: `shared-vector-store`, `distributed-episodic-memory`, `working-memory-sync`, `long-term-memory-consolidation`, `memory-read-permission`, `memory-write-permission`, `cross-agent-context-passing`, `conversation-summarisation`, `knowledge-graph-memory`, `temporal-memory`, `forgetting-curves`.  

---

### TASK-024

**Title:** Add multi-agent orchestration depth (G08 complete coverage)  
**Status:** `BLOCKED` (by TASK-022, TASK-023)  
**Phase:** 3  
**Category:** `15-orchestration`  
**Depends on:** TASK-022, TASK-023  
**Estimated graph changes:** +10 nodes, +20–24 edges  
**Files touched:** `data/SKILLS_GRAPH.json`, 10 new `.md` files  
**Description:**  
Add final orchestration layer for multi-agent deployments — coordination protocols, resource allocation, agent lifecycle management within a fleet.  

---

### TASK-025

**Title:** Update GOAL_TAXONOMY.md after Phase 3 — add G13 (Collaborative AI Networks)  
**Status:** `BLOCKED` (by TASK-020 through TASK-024)  
**Phase:** 3  
**Category:** meta  
**Depends on:** All Phase 3 tasks  
**Files touched:** `meta/GOAL_TAXONOMY.md` only  
**Description:**  
Add new goal G13 Collaborative AI Networks with 5 sub-goals. Update G08 mappings to reference new Phase 3 nodes.

---

## Phase 4 — AgentOps & LLMOps

### TASK-026

**Title:** Add LLM evaluation skills (llm-as-judge, RAGAS, faithfulness)  
**Status:** `BLOCKED` (by Phase 3 completion)  
**Phase:** 4  
**Category:** `evaluation` (new sub-category within `12-data/` or new `skills/18-evaluation/`)  
**Depends on:** Phase 3 complete  
**Estimated graph changes:** +10 nodes, +20–24 edges  
**Files touched:** `data/SKILLS_GRAPH.json`, 10 new `.md` files  
**Description:**  
Add: `llm-as-judge`, `ragas-evaluation`, `faithfulness-scoring`, `relevance-scoring`, `hallucination-detection`, `pairwise-evaluation`, `critic-llm`, `golden-dataset`, `human-eval-pipeline`, `agent-trajectory-evaluation`.  

---

### TASK-027

**Title:** Add evaluation infrastructure skills (benchmark design, regression testing)  
**Status:** `BLOCKED` (by TASK-026)  
**Phase:** 4  
**Category:** evaluation  
**Depends on:** TASK-026  
**Estimated graph changes:** +10 nodes, +18–22 edges  
**Files touched:** `data/SKILLS_GRAPH.json`, 10 new `.md` files  
**Description:**  
Add: `benchmark-dataset-creation`, `evals-framework`, `regression-test-suite`, `model-comparison-harness`, `leaderboard-tracking`, `eval-driven-development`, `safety-evaluation`, `bias-detection`, `toxicity-scoring`, `groundedness-scoring`.  

---

### TASK-028

**Title:** Add AgentOps skills  
**Status:** `BLOCKED` (by Phase 3 completion)  
**Phase:** 4  
**Category:** `17-infrastructure`  
**Depends on:** TASK-016  
**Estimated graph changes:** +6 nodes, +12–14 edges  
**Files touched:** `data/SKILLS_GRAPH.json`, 6 new `.md` files  
**Description:**  
Add: `opentelemetry-tracing`, `langfuse-observability`, `arize-monitoring`, `token-usage-tracking`, `cost-per-query-tracking`, `latency-p99-monitoring`.  

---

### TASK-029

**Title:** Add prompt management skills (versioning, A/B testing, drift detection)  
**Status:** `BLOCKED` (by Phase 3 completion)  
**Phase:** 4  
**Category:** `02-reasoning`  
**Depends on:** TASK-002, TASK-003  
**Estimated graph changes:** +3 nodes, +6–8 edges  
**Files touched:** `data/SKILLS_GRAPH.json`, 3 new `.md` files  
**Description:**  
Add: `prompt-versioning`, `prompt-ab-testing`, `prompt-drift-detection`.  

---

### TASK-030

**Title:** Add fine-tuning and model adaptation skills  
**Status:** `BLOCKED` (by Phase 3 completion)  
**Phase:** 4  
**Category:** `02-reasoning`  
**Depends on:** TASK-003  
**Estimated graph changes:** +5 nodes, +10–12 edges  
**Files touched:** `data/SKILLS_GRAPH.json`, 5 new `.md` files  
**Description:**  
Add: `lora-fine-tuning`, `rlhf-pipeline`, `dpo-training`, `preference-data-collection`, `continual-learning`.  

---

### TASK-031

**Title:** Add cost optimisation and model routing skills  
**Status:** `BLOCKED` (by TASK-028)  
**Phase:** 4  
**Category:** `17-infrastructure`  
**Depends on:** TASK-028  
**Estimated graph changes:** +4 nodes, +8–10 edges  
**Files touched:** `data/SKILLS_GRAPH.json`, 4 new `.md` files  
**Description:**  
Add: `model-routing`, `inference-caching`, `batching-strategy`, `token-budget-management`.  

---

### TASK-032

**Title:** Add data pipeline skills for agent inputs  
**Status:** `BLOCKED` (by Phase 3 completion)  
**Phase:** 4  
**Category:** `12-data`  
**Depends on:** TASK-023  
**Estimated graph changes:** +9 nodes, +18–22 edges  
**Files touched:** `data/SKILLS_GRAPH.json`, 9 new `.md` files in `skills/12-data/`  
**Description:**  
Add: `data-validation`, `data-chunking`, `data-deduplication`, `incremental-ingestion`, `schema-inference`, `data-lineage`, `streaming-data-ingestion`, `document-preprocessing`, `metadata-extraction`.  

---

### TASK-033

**Title:** Update GOAL_TAXONOMY.md after Phase 4 — update G11 mappings  
**Status:** `BLOCKED` (by TASK-026 through TASK-032)  
**Phase:** 4  
**Category:** meta  
**Depends on:** All Phase 4 tasks  
**Files touched:** `meta/GOAL_TAXONOMY.md` only  

---

## Phase 5 — Security & Governance

### TASK-034

**Title:** Add Agent Security skills  
**Status:** `BLOCKED` (by Phase 4 completion)  
**Phase:** 5  
**Category:** `14-security`  
**Depends on:** TASK-028 (observability must exist before security auditing)  
**Estimated graph changes:** +10 nodes, +20–24 edges  
**Files touched:** `data/SKILLS_GRAPH.json`, 10 new `.md` files in `skills/14-security/`  
**Description:**  
Add: `prompt-injection-defence`, `jailbreak-detection`, `output-sanitisation`, `pii-redaction`, `data-leakage-prevention`, `rbac-for-agents`, `tool-call-auditing`, `agent-sandboxing`, `input-validation`, `rate-limiting-per-user`.  
**Acceptance criteria:** `prompt-injection-defence` has `REQUIRES` edge to `skill:output-sanitisation`

---

### TASK-035

**Title:** Add API and supply-chain security skills  
**Status:** `BLOCKED` (by TASK-034)  
**Phase:** 5  
**Category:** `14-security`  
**Depends on:** TASK-034  
**Estimated graph changes:** +5 nodes, +10–12 edges  
**Files touched:** `data/SKILLS_GRAPH.json`, 5 new `.md` files  
**Description:**  
Add: `api-key-rotation`, `secrets-scanning`, `vulnerability-assessment`, `supply-chain-security`, `llm-firewall`.  

---

### TASK-036

**Title:** Add governance, compliance and explainability skills  
**Status:** `BLOCKED` (by TASK-034)  
**Phase:** 5  
**Category:** `14-security`  
**Depends on:** TASK-034, TASK-026 (fairness testing relies on eval infrastructure)  
**Estimated graph changes:** +10 nodes, +20–22 edges  
**Files touched:** `data/SKILLS_GRAPH.json`, 10 new `.md` files  
**Description:**  
Add: `audit-log-generation`, `compliance-policy-enforcement`, `explainability`, `bias-mitigation`, `fairness-testing`, `threat-modelling`, `red-teaming`, `adversarial-robustness`, `model-inversion-defence`, `membership-inference-defence`.  

---

### TASK-037

**Title:** Add safety agent pattern skills (HITL, guardrails, safe-stop)  
**Status:** `BLOCKED` (by TASK-034)  
**Phase:** 5  
**Category:** `09-agentic-patterns`  
**Depends on:** TASK-034  
**Estimated graph changes:** +5 nodes, +10–12 edges  
**Files touched:** `data/SKILLS_GRAPH.json`, 5 new `.md` files  
**Description:**  
Add: `human-in-the-loop`, `safe-stopping-criterion`, `action-confirmation-gate`, `guardrails-pattern`, `self-censorship`.  
**Acceptance criteria:** `human-in-the-loop` has `SUPPORTS` edge to `skill:interruptible-agent-flows` (from TASK-001)

---

### TASK-038

**Title:** Update GOAL_TAXONOMY.md after Phase 5 — add G14 (Security-First Agent)  
**Status:** `BLOCKED` (by TASK-034 through TASK-037)  
**Phase:** 5  
**Category:** meta  
**Depends on:** All Phase 5 tasks  
**Files touched:** `meta/GOAL_TAXONOMY.md` only  

---

## Phase 6 — Emerging Agent Architectures

### TASK-039

**Title:** Add domain-specific agent skills  
**Status:** `BLOCKED` (by Phase 5 completion)  
**Phase:** 6  
**Category:** `16-domain-specific`  
**Depends on:** Phase 5 complete  
**Estimated graph changes:** +20 nodes, +40–50 edges  
**Files touched:** `data/SKILLS_GRAPH.json`, 20 new `.md` files in `skills/16-domain-specific/`  
**Description:**  
Add vertical-specific agent skill nodes: coding, legal, medical, financial, DevOps, customer support, data analysis, research synthesis, content moderation, sales qualification + 10 more.  
All nodes carry `stability: evolving` — domain requirements shift faster than core agent patterns.

---

### TASK-040

**Title:** Add multimodal agent skills  
**Status:** `BLOCKED` (by Phase 5 completion)  
**Phase:** 6  
**Category:** `08-multimodal`  
**Depends on:** TASK-005, TASK-006 (perception layer must be complete)  
**Estimated graph changes:** +15 nodes, +30–36 edges  
**Files touched:** `data/SKILLS_GRAPH.json`, up to 3 new `.md` files (most exist), 12 new graph nodes  
**Description:**  
Add: `video-understanding`, `audio-generation`, `document-qa`, `chart-interpretation`, `multimodal-reasoning`, `cross-modal-search`, `image-to-code`, `speech-to-intent`, `visual-agent-planning`, `multimodal-embedding` + 5 more.

---

### TASK-041

**Title:** Add creative and content pipeline agent skills  
**Status:** `BLOCKED` (by Phase 5 completion)  
**Phase:** 6  
**Category:** `13-creative`  
**Depends on:** Phase 5 complete  
**Estimated graph changes:** +10 nodes, +20–24 edges  
**Files touched:** `data/SKILLS_GRAPH.json`, 10 new `.md` files in `skills/13-creative/`  
**Description:**  
Add: `long-form-writing-agent`, `style-transfer`, `narrative-planning`, `iterative-editing`, `creative-brainstorming`, `brand-voice-adaptation`, `factual-grounding-in-creative`, `content-pipeline-orchestration`, `audience-adaptation`, `multiformat-output`.  

---

### TASK-042

**Title:** Add frontier architecture skills and update GOAL_TAXONOMY.md to final state  
**Status:** `BLOCKED` (by TASK-039, TASK-040, TASK-041)  
**Phase:** 6  
**Category:** cross-category  
**Depends on:** TASK-039, TASK-040, TASK-041  
**Estimated graph changes:** +20 nodes, +40–50 edges  
**Files touched:** `data/SKILLS_GRAPH.json`, 10–12 new `.md` files across categories, `meta/GOAL_TAXONOMY.md`  
**Description:**  
Add frontier architecture nodes: `world-model-agent`, `self-improving-agent`, `long-horizon-planning`, `cognitive-architecture`, `model-context-compression`, `neuro-symbolic-reasoning`, `active-inference-agent`, `continual-self-evaluation`, `emergent-capability-detection`, `agent-lifecycle-management` + 10 more.  
Final taxonomy update: add G15 (Multimodal Agent), G16 (Autonomous Research Agent). Update all coverage metrics to final state.  
**Acceptance criteria:**  
- `statistics.total_nodes` in graph ≥250  
- All 17 `skills/` category directories have ≥1 graph node  
- `quality-report.yml` passes  
- `meta/AGENT_SKILLS_MASTER_PLAN.md` Inventory Baseline updated with final counts

---

## Backlog Summary

| Phase | Tasks | Open | Blocked | Done |
|---|---|---|---|---|
| Phase 1 — Core Agent Skills | 7 | **7** | 0 | 0 |
| Phase 2 — Production Agent Skills | 12 | 0 | **12** | 0 |
| Phase 3 — Multi-Agent Systems | 6 | 0 | **6** | 0 |
| Phase 4 — AgentOps & LLMOps | 8 | 0 | **8** | 0 |
| Phase 5 — Security & Governance | 5 | 0 | **5** | 0 |
| Phase 6 — Emerging Architectures | 4 | 0 | **4** | 0 |
| **Total** | **42** | **7** | **35** | **0** |

**Immediately startable tasks:** TASK-001, TASK-002, TASK-003, TASK-005, TASK-006 (parallel)  
**TASK-004** startable after TASK-003.  
**TASK-007** (taxonomy update) startable only after all 6 other Phase 1 tasks are DONE.

---

*Backlog version: 1.0.0 — Created 2026-06-16 — No production files modified.*
