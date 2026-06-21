# NEXT_TASK_PROMPT.md

> **Status:** READY TO PASTE  
> **Generated:** 2026-06-21 — Autonomous Roadmap Mode Phase 7  
> **For:** New agent session on SamoTech/skills-tree  
> **Task:** TASK-005 — Add core perception skills (`01-perception`)

---

```
=================================================
TASK-005 — ADD CORE PERCEPTION SKILLS
Repository: SamoTech/skills-tree
=================================================

BEFORE DOING ANYTHING — PERFORM FULL REPOSITORY TRUTH CHECK
==========================================================

Step 1: Read these files IN ORDER. Do not skip any.
  1. meta/MEMORY_STATE.md        ← canonical state checkpoint
  2. meta/PROJECT_CONSTITUTION.md ← supreme authority
  3. meta/DECISION_LOG.md        ← append-only history
  4. meta/AGENT_SKILLS_BACKLOG.md ← task registry
  5. data/SKILLS_GRAPH.json      ← the actual graph

Step 2: MEMORY VALIDATION
Verify ALL of the following match MEMORY_STATE.md before proceeding:
  - Total nodes = 47 (±0 tolerance)
  - Total edges = 93 (±0 tolerance)
  - TASK-005 status = OPEN in backlog
  - TASK-003 status = DONE
  - Category 01-perception nodes = 0
  - Phase 1 target = 53 nodes
  - Schema version = 1.3

If any value does not match: STOP. Write meta/TASK_005_SKIP_REPORT.md
explaining the discrepancy. Do NOT proceed.

Step 3: DUPLICATE PROTECTION
Read the complete Existing Node IDs list from meta/MEMORY_STATE.md.
Current 47 nodes (DO NOT duplicate these IDs):
  skill:code-generation, skill:prompt-engineering, skill:function-calling,
  skill:web-scraping, skill:browser-automation, skill:vector-search,
  skill:rag-retrieval, skill:embedding-generation, skill:llm-orchestration,
  skill:multi-agent-coordination, skill:workflow-automation, skill:error-recovery,
  skill:context-management, skill:api-integration, skill:data-extraction,
  skill:react-pattern, skill:cot, skill:tot, skill:reflection-pattern,
  skill:plan-and-execute, skill:rag-pattern, skill:agent-as-tool,
  skill:agent-handoffs, skill:agentic-rag, skill:bootstrapping-pattern,
  skill:constitutional-ai, skill:critic-agent, skill:debate-pattern,
  skill:interruptible-agent-flows, skill:lats, skill:mcts-pattern,
  skill:memory-augmented-agent, skill:mixture-of-agents, skill:rag-pipeline,
  skill:self-play-pattern, skill:subagent-delegation, skill:time-travel-debugging,
  skill:tool-use-loop, skill:self-consistency, skill:step-back-prompting,
  skill:least-to-most, skill:meta-prompting, skill:planning-decomposition,
  skill:hypothesis-generation, skill:goal-decomposition,
  skill:reasoning-under-uncertainty, skill:analogical-reasoning

Before adding each node, check:
  - Exact ID does not appear in the list above
  - No existing node covers the same concept under a different name
  - (cosine similarity > 0.85 on name tokens = potential duplicate)

Step 4: ROADMAP VALIDATION
Verify in meta/NEXT_TASK_RECOMMENDATION.md:
  - Recommended task = TASK-005
  - Recommended category = 01-perception
  - Expected nodes = +6
  - Expected edges = +12 minimum

If NEXT_TASK_RECOMMENDATION.md points to a different task: STOP and
read the recommendation before proceeding. Do not override it.

==========================================================
TASK DEFINITION
==========================================================

Objective: Add exactly 6 production-relevant nodes to the `01-perception`
category in data/SKILLS_GRAPH.json, meeting all constitution requirements.

Phase 1 completion: 47 + 6 = 53 nodes = Phase 1 target REACHED.

REQUIRED NODES (add all 6):

  node_id: skill:ocr
  name: Optical Character Recognition
  category: 01-perception
  stability: stable
  description: Ability to extract machine-readable text from images, PDFs, and
               scanned documents using OCR engines or vision models.
  production_evidence: Used in LangChain document loaders, LlamaIndex PDF
                       readers, Azure Form Recognizer, AWS Textract integrations.

  node_id: skill:screen-parsing
  name: Screen Parsing
  category: 01-perception
  stability: stable
  description: Ability to interpret and extract structured information from
               rendered UI screenshots, DOM trees, or accessibility trees.
  production_evidence: Used in computer-use agents (Claude, GPT-4o), Playwright
                       screenshot-based agents, SWE-agent screen readers.

  node_id: skill:image-understanding
  name: Image Understanding
  category: 01-perception
  stability: evolving
  description: Ability to semantically interpret the content of images —
               objects, scenes, spatial relationships, and contextual meaning —
               using vision-language models.
  production_evidence: GPT-4o vision, Claude 3 vision, LLaVA, Gemini multimodal.

  node_id: skill:document-parsing
  name: Document Parsing
  category: 01-perception
  stability: stable
  description: Ability to extract structured content (tables, headings, sections,
               metadata) from documents (PDF, DOCX, HTML) for downstream
               reasoning or retrieval.
  production_evidence: LlamaIndex document parsers, Unstructured.io, LangChain
                       document loaders, docling, marker.

  node_id: skill:audio-transcription
  name: Audio Transcription
  category: 01-perception
  stability: stable
  description: Ability to convert spoken audio to text using ASR models,
               enabling agents to process voice inputs, meeting recordings,
               and audio logs.
  production_evidence: OpenAI Whisper, Deepgram, AssemblyAI APIs used in
                       production voice agents and meeting-assistant pipelines.

  node_id: skill:multimodal-input
  name: Multimodal Input Processing
  category: 01-perception
  stability: evolving
  description: Ability to jointly process and reason over inputs from multiple
               modalities (text, image, audio, video) within a single agent
               context window.
  production_evidence: GPT-4o, Claude 3.5 Sonnet, Gemini 1.5 Pro multimodal
                       pipelines; LangChain multimodal chains.

REQUIRED EDGES (minimum 2 per node; add all listed):

Note: Every edge must include: source, target, type, confidence (0.0-1.0)
Valid edge types: REQUIRES | RECOMMENDED_WITH | LEARN_BEFORE | SUPPORTS

  skill:ocr → skill:document-parsing          LEARN_BEFORE  0.88
  skill:ocr → skill:data-extraction           SUPPORTS      0.82
  skill:ocr → skill:embedding-generation      RECOMMENDED_WITH 0.75

  skill:screen-parsing → skill:browser-automation  RECOMMENDED_WITH 0.90
  skill:screen-parsing → skill:image-understanding LEARN_BEFORE    0.85
  skill:screen-parsing → skill:data-extraction     SUPPORTS        0.78

  skill:image-understanding → skill:multimodal-input   LEARN_BEFORE     0.88
  skill:image-understanding → skill:prompt-engineering RECOMMENDED_WITH 0.80
  skill:image-understanding → skill:embedding-generation SUPPORTS       0.77

  skill:document-parsing → skill:rag-retrieval         RECOMMENDED_WITH 0.92
  skill:document-parsing → skill:context-management    SUPPORTS         0.85
  skill:document-parsing → skill:embedding-generation  RECOMMENDED_WITH 0.88

  skill:audio-transcription → skill:context-management  SUPPORTS        0.80
  skill:audio-transcription → skill:multimodal-input    LEARN_BEFORE    0.82
  skill:audio-transcription → skill:embedding-generation SUPPORTS       0.73

  skill:multimodal-input → skill:prompt-engineering    REQUIRES         0.85
  skill:multimodal-input → skill:context-management    REQUIRES         0.88
  skill:multimodal-input → skill:llm-orchestration     RECOMMENDED_WITH 0.82

Total new edges: 18 (target: ≥12 — this exceeds minimum safely)

==========================================================
GRAPH VALIDATION
==========================================================

After modifying data/SKILLS_GRAPH.json, verify:

  [ ] Total nodes = 53 exactly
  [ ] Total edges ≥ 111 (93 + 18)
  [ ] All 6 new nodes have category = "01-perception"
  [ ] All new node_ids use pattern skill:kebab-case
  [ ] All new edges have: source, target, type, confidence
  [ ] Edge type is one of: REQUIRES, RECOMMENDED_WITH, LEARN_BEFORE, SUPPORTS
  [ ] No REQUIRES or LEARN_BEFORE cycle created
      (check: new node → existing node only; no existing → new → existing loops)
  [ ] statistics block in JSON updated: total_nodes=53, total_edges=111+
  [ ] Edge/node ratio = 111/53 = 2.094 (must be ≥ 1.978 — P-01 satisfied)

==========================================================
CONSTITUTION VALIDATION
==========================================================

For each principle, verify it is satisfied AFTER your changes:

  P-01 Graph quality over skill count:
       ratio ≥ 1.978 → PASS if edges ≥ 111

  P-02 Relationships first:
       All 6 nodes have edges in same commit → PASS

  P-03 Production skills first:
       All 6 nodes have production_evidence documented → PASS (see above)

  P-04 Real-world utility:
       LangChain, LlamaIndex, OpenAI, Claude — all named → PASS

  P-05 Goal connectivity:
       New nodes connect to goals G03, G05, G06 via ≤ 3 hops → verify manually

  P-06 Zero duplicates:
       All 6 IDs checked against 47-node registry → PASS (if no match)

  P-07 Connect before expand:
       Pre-task: all 47 nodes have ≥ 2 edges (93 total) → PASS

  P-09 Agentic systems primary domain:
       01-perception is in top-8 priority categories → PASS

  P-10 Traversability:
       All edges have type + confidence → PASS

==========================================================
REQUIRED REPORTS
==========================================================

Create ALL of the following files in the same atomic commit:

1. meta/TASK_005_REPORT.md
   Must contain:
   - Task ID: TASK-005
   - Date: (today)
   - Nodes added: 6 (list all 6 IDs)
   - Edges added: 18 (list all 18 source→target)
   - Graph before: 47 nodes, 93 edges
   - Graph after: 53 nodes, 111 edges
   - Phase 1 status: DONE (target reached)
   - Goals unblocked: G03, G05, G06
   - Constitution checks: P-01 through P-10 results
   - Commit SHA: (fill after commit)
   - CI status: (fill after CI runs)

2. meta/DECISION_LOG.md (APPEND ONLY — do not modify existing entries)
   Append this entry:
   ---
   Date: (today)
   Task: TASK-005
   Decision: Added 6 core perception nodes to 01-perception category.
   Nodes: skill:ocr, skill:screen-parsing, skill:image-understanding,
          skill:document-parsing, skill:audio-transcription, skill:multimodal-input
   Edges: 18 new edges connecting to 03-memory, 07-tool-use, 12-data, 15-orchestration
   Phase 1: COMPLETE — 53 nodes reached
   Goals unblocked: G03, G05, G06
   Next task: TASK-006 (now unblocked)
   ---

3. meta/MEMORY_STATE.md (UPDATE — replace entire file with new state)
   Key changes:
   - Total nodes: 47 → 53
   - Total edges: 93 → 111
   - Phase 1 status: In Progress → DONE
   - Current phase: Phase 1 DONE → Phase 2 begins
   - 01-perception: 0 → 6 nodes
   - TASK-005: OPEN → DONE
   - TASK-006: BLOCKED → OPEN
   - Memory State version: 1.2.0 → 1.4.0
   - Add all 6 new node IDs to existing node registry

4. meta/NEXT_TASK_RECOMMENDATION.md (REPLACE with new recommendation)
   After Phase 1 completes, the next task is TASK-006 (document/data perception)
   or TASK-002 (context engineering) — run roadmap analysis to determine.

5. meta/NEXT_TASK_PROMPT.md (REPLACE with next task prompt)
   Generate the next governance-aware, executable prompt for the recommended task.

==========================================================
SELF-REVIEW SECTION
==========================================================

Before committing, answer each question:

  Q1: Does data/SKILLS_GRAPH.json have exactly 53 nodes?
      Expected: YES. If NO: do not commit.

  Q2: Does every new node have ≥ 2 edges in the graph?
      Expected: YES. If NO: add missing edges before committing.

  Q3: Did you read the existing node list and verify zero ID collisions?
      Expected: YES. If NO: re-check every new ID against the 47-node registry.

  Q4: Is meta/DECISION_LOG.md append-only (no existing entries modified)?
      Expected: YES. If NO: revert your DECISION_LOG changes and append correctly.

  Q5: Does meta/MEMORY_STATE.md reflect the new state (53 nodes, Phase 1 DONE)?
      Expected: YES. If NO: update MEMORY_STATE.md before committing.

  Q6: Is the edge/node ratio ≥ 1.978 after your changes?
      Expected: YES (111/53 = 2.094). If NO: add more edges.

  Q7: Did you create meta/TASK_005_REPORT.md?
      Expected: YES. If NO: create it before committing.

  Q8: Are all new edges ACYCLIC for REQUIRES and LEARN_BEFORE types?
      Expected: YES. Trace each REQUIRES/LEARN_BEFORE path to confirm
      no loop returns to the new node.

==========================================================
GOVERNANCE UPDATE SECTION
==========================================================

AFTER TASK COMPLETION, update governance in this order:

  1. meta/MEMORY_STATE.md          — canonical state (47→53 nodes)
  2. meta/DECISION_LOG.md          — append TASK-005 entry
  3. meta/AGENT_SKILLS_BACKLOG.md  — mark TASK-005 DONE, TASK-006 OPEN
  4. meta/TASK_005_REPORT.md       — full task report
  5. meta/NEXT_TASK_RECOMMENDATION.md — update for Phase 2
  6. meta/NEXT_TASK_PROMPT.md         — generate next executable prompt

All 6 files must be in the SAME atomic commit as data/SKILLS_GRAPH.json.

==========================================================
COMMIT FORMAT
==========================================================

graph(01-perception): add 6 core perception nodes — TASK-005 — Phase 1 DONE

Added to data/SKILLS_GRAPH.json:
  + skill:ocr (stable)
  + skill:screen-parsing (stable)
  + skill:image-understanding (evolving)
  + skill:document-parsing (stable)
  + skill:audio-transcription (stable)
  + skill:multimodal-input (evolving)

Edges: +18 (connecting to 03-memory, 07-tool-use, 12-data, 15-orchestration)
Graph: 47 → 53 nodes | 93 → 111 edges
Phase 1: COMPLETE (53/53 nodes)
Goals unblocked: G03, G05, G06
Constitution: P-01 ✅ P-02 ✅ P-03 ✅ P-04 ✅ P-05 ✅ P-06 ✅ P-07 ✅ P-09 ✅ P-10 ✅

Governance:
  - meta/TASK_005_REPORT.md created
  - meta/DECISION_LOG.md appended
  - meta/MEMORY_STATE.md updated to v1.4.0 (Phase 1 DONE)
  - meta/NEXT_TASK_RECOMMENDATION.md updated
  - meta/NEXT_TASK_PROMPT.md regenerated

BREAKING: Phase 1 complete. Phase 2 begins on next task.

==========================================================
ANTI-DRIFT PROTECTION
==========================================================

This prompt was generated from repository state on 2026-06-21.
Node count was 47. If the repository now shows a different node count,
this prompt may be stale. Re-read meta/MEMORY_STATE.md and regenerate
meta/NEXT_TASK_PROMPT.md before executing.

Do not add nodes beyond the 6 specified. Do not add skill files (.md)
without corresponding graph nodes. Do not execute Phase 2 tasks until
meta/MEMORY_STATE.md confirms Phase 1 status = DONE.

If you find 01-perception already has nodes:
  STOP — read meta/MEMORY_STATE.md — write meta/TASK_005_SKIP_REPORT.md.

==========================================================
```

---

*NEXT_TASK_PROMPT v1.3.0 — 2026-06-21 — Autonomous Roadmap Mode Phase 7*
