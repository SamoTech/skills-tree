# Blueprint Catalog V2

**Initiative:** INITIATIVE-014A.2 — Phase 3  
**Date:** 2026-06-24  
**Previous:** 25 goals (INITIATIVE-013)  
**Target:** 50 goals across 8 agent categories  

---

## Expansion Strategy

Previous catalog covered General Purpose, Research, and Code agent goals. V2 expands into 8 specialized categories with comprehensive coverage of production-grade agent patterns.

---

## Category 1 — Coding Agents (8 goals)

| # | Goal | Core Skills | Blueprint Tag |
|---|---|---|---|
| 1 | Build an autonomous code generation agent | code-generation, task-decomposition, function-calling | `coding-agent-v1` |
| 2 | Create a self-healing CI/CD agent | code-generation, error-detection, retry-logic, rollback | `self-healing-cicd` |
| 3 | Build a PR review automation agent | code-reading, reasoning, comment-generation, github-api | `pr-review-agent` |
| 4 | Create a test generation agent | code-reading, code-generation, test-execution | `test-gen-agent` |
| 5 | Build a refactoring agent with safety checks | code-reading, code-generation, input-sanitization, rollback | `refactor-agent` |
| 6 | Create a bug localization agent | code-reading, web-search, rag, reasoning | `bug-localize-agent` |
| 7 | Build a polyglot translation agent | code-reading, code-generation, function-calling | `polyglot-agent` |
| 8 | Create a dependency audit agent | code-reading, web-search, secret-scanning, audit-logging | `dep-audit-agent` |

---

## Category 2 — RAG Systems (6 goals)

| # | Goal | Core Skills | Blueprint Tag |
|---|---|---|---|
| 9 | Build a production RAG pipeline | embedding-generation, vector-store-retrieval, rag, openai-api | `rag-production` |
| 10 | Create a hybrid search RAG (dense + sparse) | embedding-generation, rag, web-search | `rag-hybrid` |
| 11 | Build a multi-document RAG with citations | rag, summarization, document-parsing | `rag-citations` |
| 12 | Create a reranking RAG pipeline | rag, reasoning, embedding-generation | `rag-rerank` |
| 13 | Build a RAG system with source freshness control | rag, web-search, embedding-generation | `rag-freshness` |
| 14 | Create a conversational RAG with memory | rag, memory-injection, short-term-memory | `rag-conversational` |

---

## Category 3 — Multi-Agent Systems (7 goals)

| # | Goal | Core Skills | Blueprint Tag |
|---|---|---|---|
| 15 | Build a sequential multi-agent pipeline | task-decomposition, multi-agent-orchestration, handoff | `multi-agent-sequential` |
| 16 | Create a parallel specialist mesh | multi-agent-orchestration, consensus, reasoning | `multi-agent-mesh` |
| 17 | Build a debate-style multi-agent system | multi-agent-orchestration, reasoning, consensus | `multi-agent-debate` |
| 18 | Create a supervisor-worker agent hierarchy | task-decomposition, multi-agent-orchestration, planning | `supervisor-worker` |
| 19 | Build a self-evaluating agent team | reflection, multi-agent-orchestration, consensus | `self-eval-team` |
| 20 | Create a human-in-the-loop approval system | multi-agent-orchestration, audit-logging, handoff | `hitl-approval` |
| 21 | Build a competitive agent benchmarking system | multi-agent-orchestration, reasoning, audit-logging | `agent-benchmark` |

---

## Category 4 — Research Agents (6 goals)

| # | Goal | Core Skills | Blueprint Tag |
|---|---|---|---|
| 22 | Build a deep research automation agent | web-search, rag, summarization, reasoning | `research-deep` |
| 23 | Create an academic paper synthesis agent | document-parsing, rag, summarization | `paper-synthesis` |
| 24 | Build a competitive intelligence agent | web-search, rag, reasoning, summarization | `competitive-intel` |
| 25 | Create a market research agent | web-search, data-extraction, summarization | `market-research` |
| 26 | Build a fact-checking agent | web-search, rag, reasoning | `fact-check-agent` |
| 27 | Create a literature review agent | rag, summarization, document-parsing, embedding-generation | `literature-review` |

---

## Category 5 — Customer Support Agents (5 goals)

| # | Goal | Core Skills | Blueprint Tag |
|---|---|---|---|
| 28 | Build a personalized support bot | memory-injection, intent-classification, rag | `support-personalized` |
| 29 | Create a ticket triage and routing agent | intent-classification, multi-agent-orchestration, audit-logging | `ticket-triage` |
| 30 | Build an escalation detection agent | intent-classification, reasoning, audit-logging | `escalation-agent` |
| 31 | Create a product knowledge base agent | rag, embedding-generation, summarization | `kb-agent` |
| 32 | Build a sentiment-aware response agent | intent-classification, reasoning, summarization | `sentiment-agent` |

---

## Category 6 — Security Agents (5 goals)

| # | Goal | Core Skills | Blueprint Tag |
|---|---|---|---|
| 33 | Build a secret scanning agent | secret-scanning, audit-logging, code-reading | `secret-scan-agent` |
| 34 | Create a vulnerability triage agent | code-reading, web-search, reasoning, audit-logging | `vuln-triage-agent` |
| 35 | Build a compliance audit agent | audit-logging, reasoning, document-parsing | `compliance-agent` |
| 36 | Create an anomaly detection agent | data-analysis, reasoning, audit-logging | `anomaly-agent` |
| 37 | Build a sandboxed code execution agent | sandboxing, code-generation, input-sanitization | `sandboxed-exec-agent` |

---

## Category 7 — Workflow Automation (7 goals)

| # | Goal | Core Skills | Blueprint Tag |
|---|---|---|---|
| 38 | Build a data pipeline orchestration agent | etl, data-analysis, audit-logging | `data-pipeline-agent` |
| 39 | Create an email triage and response agent | intent-classification, summarization, reasoning | `email-triage-agent` |
| 40 | Build a meeting notes and action item agent | summarization, task-decomposition, document-parsing | `meeting-notes-agent` |
| 41 | Create a report generation agent | rag, summarization, data-analysis | `report-gen-agent` |
| 42 | Build a calendar and scheduling agent | function-calling, reasoning, task-decomposition | `scheduling-agent` |
| 43 | Create a document processing pipeline | document-parsing, etl, rag | `doc-processing-pipeline` |
| 44 | Build a notification routing agent | intent-classification, multi-agent-orchestration, audit-logging | `notification-router` |

---

## Category 8 — Domain-Specific Agents (6 goals)

| # | Goal | Core Skills | Blueprint Tag |
|---|---|---|---|
| 45 | Build a medical triage agent | reasoning, rag, domain-specific-medical | `medical-triage-agent` |
| 46 | Create a legal document review agent | document-parsing, rag, reasoning | `legal-review-agent` |
| 47 | Build a financial analysis agent | data-analysis, rag, reasoning | `financial-analysis-agent` |
| 48 | Create a DevOps incident response agent | code-reading, web-search, audit-logging, rollback | `devops-incident-agent` |
| 49 | Build an educational tutoring agent | rag, reasoning, summarization, memory-injection | `tutoring-agent` |
| 50 | Create a scientific hypothesis agent | rag, reasoning, web-search, summarization | `hypothesis-agent` |

---

## Implementation Notes

- Each goal maps to 3–5 core skills from `SKILLS_GRAPH.json`
- Blueprint tags are used by the Blueprint Generator UI to fetch the matching `blueprints/` file
- Goals without a matching blueprint file become auto-stubs: generated on-demand from skills metadata
- The generator shows the top 3 matching skills for each goal with direct links to skill files
- V2 adds 25 new goals to the existing 25 = **50 total** 

---

## Coverage Metrics

| Category | Goals | Existing Blueprints | Stub Count |
|---|---|---|---|
| Coding Agents | 8 | 2 | 6 |
| RAG Systems | 6 | 1 | 5 |
| Multi-Agent | 7 | 3 | 4 |
| Research Agents | 6 | 1 | 5 |
| Customer Support | 5 | 1 | 4 |
| Security Agents | 5 | 0 | 5 |
| Workflow Automation | 7 | 0 | 7 |
| Domain-Specific | 6 | 0 | 6 |
| **Total** | **50** | **8** | **42** |
