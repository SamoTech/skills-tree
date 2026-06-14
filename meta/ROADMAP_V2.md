# Skills Tree — Roadmap v2.0  
**Date:** 2026-06-14  
**Status:** Active execution roadmap (replaces phase-based structure in `meta/ROADMAP.md`)  
**Authority:** This document supersedes `EXECUTION_PRIORITY_MATRIX.md` Section 5 after reality audit reconciliation  

---

## Preamble

This roadmap reflects the **true state of the project** as of 2026-06-14 after a comprehensive reality audit ([`meta/REALITY_AUDIT.md`](./REALITY_AUDIT.md)).

**Key findings from the audit:**  
✅ 6 tasks (T-09, T-11, T-12, T-13, T-15, T-16) confirmed **complete** via commit + filesystem evidence  
✅ All Tier 1 structural foundations (**API, search, graph, paths UI, releases**) already delivered  
❌ 4 tasks (T-01, T-02, T-03, T-18) rejected (scored below 25/50 floor)  

**Remaining backlog: 14 tasks** (down from 25 documented)  
**New execution timeline: ~16 weeks** (4 months) — 6 weeks saved  

---

## Execution Waves

Tasks are grouped into 7 capability-driven waves, ordered by ROI and dependency chain.

---

## Wave 1 — Content Quality Engine (3 weeks)

**Objective:** Eliminate the trust failure. 80% of users arrive for a specific skill — 80% leave disappointed when it's a stub. This wave fixes that for the highest-traffic 50 skills.

### T-04: Stub Upgrade Wave 1 (50 skills → v2)
**Impact:** 45/50 | **ROI:** 375 | **Effort:** 6/10 (2 weeks)  
**Priority:** 🔴 **HIGHEST PRIORITY IN THE ENTIRE PROJECT**  

**Scope:**  
Upgrade the top 50 highest-traffic skills from v1 stubs to v2 standard:
- Full description (3+ sentences, not 1-liner)
- Runnable code example (real Python, not pseudocode)
- Failure modes section (2+ edge cases)
- Populated `related_skills` (3+ links)
- Updated `frameworks` field if applicable

**Selection Criteria for the 50:**  
1. Core perception skills (file reading, API parsing, PDF extraction)  
2. Core reasoning skills (planning, task decomposition, self-correction)  
3. Memory patterns (RAG, episodic, cross-session persistence)  
4. Most-cited skills in `systems/` and `blueprints/`  
5. Skills referenced in existing benchmarks  

**Acceptance Criteria:**  
- All 50 skills pass `quality-report.yml` v2 checks  
- `meta/QUALITY-REPORT.md` shows 50+ v2 skills (up from 48)  
- No v1 stubs remain in the top 50 by PageRank/citation count  

**Deliverable:**  
50 production-ready skills that AI agent builders can copy-paste with confidence.

---

### T-07: Model Comparison AST Sweep
**Impact:** 40/50 | **ROI:** 333 | **Effort:** 4/10 (1 week)  
**Dependencies:** T-04 (run on Wave 1 completions immediately)  

**Scope:**  
For every skill upgraded in T-04, add a model comparison table:

| Model | Accuracy | Speed | Cost (1M tokens) | Notes |
|-------|----------|-------|-----------------|-------|
| Claude Opus 4 | 0.92 | 850ms | $15 | Best reasoning, verbose |
| GPT-4o | 0.89 | 720ms | $5 | Fast, occasionally terse |
| Gemini 2.0 Flash | 0.85 | 400ms | $0.075 | Cost leader, good enough |

Implementation:
- Python AST sweep script (extend existing `tools/ast-sweep.py`)
- Read skill `## Example` code block
- Run it against 3 models via API (LiteLLM for abstraction)
- Parse outputs, compute metrics (accuracy/latency/cost)
- Inject table into skill file under `## Model Performance`

**Acceptance Criteria:**  
- All 50 Wave 1 skills have a model comparison table  
- Table format matches the v2 template spec  
- At least 3 models tested per skill  

**Deliverable:**  
Makes every skill **immediately actionable** — users know which model to use before they start coding.

---

## Wave 2 — Catalog Expansion (5 weeks)

**Objective:** Reach critical mass. 150+ quality skills unlock framework integration eligibility (MCP, LangChain Hub) and make the CLI worth publishing.

### T-05: Stub Upgrade Wave 2 (100 skills → v2)
**Impact:** 41/50 | **ROI:** 293 | **Effort:** 7/10 (3 weeks)  
**Dependencies:** T-04 methodology + tooling established  

**Scope:**  
Second batch: upgrade the next 100 skills by citation/traffic rank.

**Process Improvements from Wave 1:**  
- Batch skill selection via `QUALITY-REPORT.md` stub list  
- Reuse code example patterns from Wave 1 as templates  
- AI-assisted drafting (ChatGPT/Claude) for boilerplate (human review required)  

**Acceptance Criteria:**  
- 150+ total v2 skills (50 from Wave 1 + 100 new)  
- `meta/QUALITY-REPORT.md` shows v1 stub count dropped by 100  
- All upgraded skills pass CI validation  

---

### T-14: Benchmark Expansion (13 new benchmarks, 1 per category)
**Impact:** 41/50 | **ROI:** 228 | **Effort:** 6/10 (2 weeks)  
**Dependencies:** T-04 (enough v2 content per category)  

**Scope:**  
Create **1 reproducible benchmark per taxonomy category** (17 total categories → 13 missing benchmarks).

Existing benchmarks (4):
- `benchmarks/react-vs-lats.md` (Reasoning)  
- `benchmarks/rag-strategies.md` (Memory)  
- `benchmarks/memory-injection.md` (Memory)  
- `benchmarks/function-calling.md` (Tool Use)  

New benchmarks to create (13):
1. **Perception:** PDF table extraction (Marker vs Unstructured vs PyPDF2)  
2. **Communication:** Email tone adaptation (formal vs casual)  
3. **Learning:** Few-shot vs fine-tuning on custom task  
4. **Tool Use:** Parallel tool calls (batch API vs sequential)  
5. **Orchestration:** Multi-agent handoff latency  
6. **Monitoring:** Token usage tracking (LiteLLM vs manual)  
7. **Security:** Prompt injection detection (3 methods)  
8. **Ethics:** Bias detection in generated summaries  
9. **Agentic Patterns:** ReAct vs Reflexion vs LATS (extend existing)  
10. **Computer Use:** Web navigation (Playwright vs Selenium)  
11. **Code Generation:** Test coverage (GPT-4o vs Claude Opus)  
12. **Data Processing:** JSON schema validation speed  
13. **Infrastructure:** Docker vs Kubernetes startup time for agent deployments  

**Benchmark Template:**  
```markdown
# Benchmark: [Skill Name] — [Method A] vs [Method B]

## Objective
## Methodology
## Dataset (with link or inline sample)
## Results Table
| Method | Metric 1 | Metric 2 | Winner | Margin |
## Reproducibility (script path, requirements.txt)
## Takeaways
```

**Acceptance Criteria:**  
- 17 total benchmarks (4 existing + 13 new)  
- Each new benchmark has a reproducibility script in `benchmarks/scripts/`  
- All benchmarks pass `pr-checks.yml` link validation  

**Deliverable:**  
Every category has **evidence-backed guidance** on which approach works best. Each benchmark is a linkable artifact for academic citation.

---

## Wave 3 — Programmatic Distribution (2 weeks, parallel work)

**Objective:** Turn Skills Tree from a GitHub repo into a **developer tool ecosystem**. Each task here opens a new acquisition channel.

### T-19: CLI Scaffold + PyPI Publication
**Impact:** 44/50 | **ROI:** 220 | **Effort:** 5/10 (1 week)  
**Dependencies:** `docs/api/skills.json` (already exists ✅)  

**Scope:**  
Build and publish `skills-tree` CLI to PyPI.

**Commands:**  
```bash
pip install skills-tree

skills-tree search "memory injection"
# Returns: Top 5 matching skills with version, category, level

skills-tree show skills/03-memory/rag.md
# Renders: Full skill content in terminal (syntax-highlighted via `rich`)

skills-tree list --category reasoning --level advanced
# Filters and lists skills

skills-tree update
# Pulls latest skills.json from GitHub (cached locally with 24h TTL)
```

**Implementation:**  
- Python package structure: `skills_tree/cli.py`, `skills_tree/api.py`, `skills_tree/render.py`  
- Use `typer` for CLI framework  
- Use `rich` for terminal rendering  
- Fetch `docs/api/skills.json` from GitHub raw URL (fallback to cached copy)  
- Offline mode: `--offline` flag uses last cached data  

**Deliverable:**  
`pip install skills-tree` works. Skills Tree is now in every developer's terminal.

---

### T-24: MCP Registry Listing
**Impact:** 44/50 | **ROI:** 220 | **Effort:** 4/10 (1 week)  
**Dependencies:** T-04 (50+ quality skills to list)  

**Scope:**  
Register Skills Tree in the **Model Context Protocol (MCP) registry**.

MCP is Anthropic's open protocol for connecting AI models to external tools and data sources. Being listed in the MCP registry means any MCP-compatible agent (Claude, custom agents) can query the Skills Tree catalog in real-time.

**Submission Requirements:**  
- MCP-compliant JSON schema (map skill frontmatter to MCP tool definition)  
- Public API endpoint (use `docs/api/skills.json` — already live)  
- Documentation page (write `meta/MCP-INTEGRATION.md`)  
- Submit PR to [modelcontextprotocol/registry](https://github.com/modelcontextprotocol/registry)  

**Deliverable:**  
Skills Tree appears in the MCP registry. Claude can now cite skills from the catalog natively.

---

### T-23: LangChain Hub Submission (Top 20 Skills)
**Impact:** 42/50 | **ROI:** 210 | **Effort:** 4/10 (1 week)  
**Dependencies:** T-04 (battle-tested skills ready)  

**Scope:**  
Submit the **top 20 battle-tested skills** to [LangChain Hub](https://smith.langchain.com/hub) as reusable prompt templates.

**Selection Criteria (top 20):**  
- All must be v3 (battle-tested)  
- Highest citation count in `systems/` and `blueprints/`  
- Cover all major categories (2–3 per category)  

**Hub Format Conversion:**  
Each skill becomes a LangChain `PromptTemplate`:
```python
from langchain import PromptTemplate

rag_skill = PromptTemplate(
    input_variables=["query", "context"],
    template="""You are a RAG assistant. Given the query and context:
Query: {query}
Context: {context}
Provide a concise answer citing the context."""
)
```

**Submission Process:**  
- Convert 20 skills to LangChain Hub YAML format  
- Test each template with `langchain-cli` locally  
- Submit via Hub web UI (requires LangChain account)  
- Link back to Skills Tree in each template's description  

**Deliverable:**  
Skills Tree skills are now **first-class LangChain citizens**. Every LangChain developer sees them in the Hub.

---

### T-20: CLI `new` Wizard (Interactive Skill Creation)
**Impact:** 34/50 | **ROI:** 378 | **Effort:** 3/10 (3 days)  
**Dependencies:** T-19 (CLI scaffold in place)  

**Scope:**  
Add `skills-tree new` command — an interactive wizard for creating a new skill file.

**Flow:**  
```bash
$ skills-tree new

➜ Title: API Response Parsing
➜ Category: [autocomplete from 17 categories]
➜ Level: [basic|intermediate|advanced|experimental]
➜ Description: (3+ sentences)
➜ Code Example: (paste or type)
➜ Failure Modes: (2+ edge cases)
➜ Related Skills: (autocomplete from existing skills)
✓ Skill file created: skills/01-perception/api-response-parsing.md
➜ Open in editor? [Y/n]
```

**Implementation:**  
- Use `typer` prompts for input  
- Validate inputs against `meta/skill-schema.json`  
- Auto-generate YAML frontmatter  
- Write file to local `skills/` directory  
- Optionally open in `$EDITOR`  

**Deliverable:**  
Contributing a skill takes **3 minutes** instead of 15. New contributors face zero friction.

---

## Wave 4 — Learning Paths (1 week)

**Objective:** Turn the flat catalog into a **guided learning experience**. Skill Paths are curated sequences from beginner to production-ready.

### T-08: Populate `paths/` (4 Learning Tracks)
**Impact:** 40/50 | **ROI:** 500 | **Effort:** 4/10 (3 days)  
**Dependencies:** T-04 (skills must be v2 quality)  

**Scope:**  
Write **4 curated Skill Path YAML files** in `paths/`.

**Path 1: Research Agent (Beginner → Intermediate)**  
```yaml
id: research-agent-path
title: "Build a Research Agent"
level: intermediate
estimated_time: "6 hours"
skills:
  - skills/11-web/web-search.md
  - skills/03-memory/rag.md
  - skills/06-communication/summarize.md
  - skills/03-memory/memory-injection.md
  - skills/09-agentic-patterns/react.md
milestones:
  - after: 2
    check: "Can the agent retrieve and filter search results?"
  - after: 5
    check: "Does the final agent cite sources in its summary?"
```

**Path 2: Memory-First Agent (Intermediate)**  
Sequence: episodic memory → RAG → cross-session persistence → memory summarization → knowledge graph

**Path 3: Computer Use Agent (Advanced)**  
Sequence: screen reading → web navigation → form filling → error handling → multi-step workflows

**Path 4: Zero-to-Production (Beginner → Advanced)**  
Sequence: basic prompt → planning → tool use → self-correction → monitoring → deployment → cost tracking

**Acceptance Criteria:**  
- All 4 YAML files validate against the path schema (to be defined)  
- Each path has 5–7 skills  
- Each path has 2+ milestones  
- `docs/paths.html` renders all 4 paths (UI already exists ✅)  

**Deliverable:**  
New users have a **guided entry point**. Instead of browsing 377 skills, they follow a path and learn by building.

---

## Wave 5 — Catalog Completion (4 weeks)

**Objective:** Eliminate all stubs. Every skill in the catalog is production-ready.

### T-06: Stub Upgrade Wave 3 (Remaining ~152 Skills → v2)
**Impact:** 36/50 | **ROI:** 225 | **Effort:** 8/10 (4 weeks)  
**Dependencies:** T-04, T-05 processes proven  

**Scope:**  
Final blitz: upgrade every remaining v1 stub to v2.

**Target State:**  
- **0 stubs** remain in the catalog  
- 377 skills, all v2+ minimum  
- `meta/QUALITY-REPORT.md` shows 100% v2+ coverage  

**Efficiency Tactics:**  
- AI-assisted drafting (LLM generates v2 draft, human reviews and edits)  
- Batch similar skills (e.g., all file-format parsers in one sprint)  
- Reuse code example patterns from Waves 1–2  

**Acceptance Criteria:**  
- `QUALITY-REPORT.md` stub count = 0  
- All skills pass CI schema validation  
- No skill file has `<100 words` in description  

**Deliverable:**  
The catalog is **complete**. Every page is useful. Trust failure eliminated permanently.

---

## Wave 6 — AI Automation + Semantic Layer (2 weeks)

**Objective:** Scale catalog maintenance beyond human effort. Use AI to keep content fresh and add semantic search intelligence.

### T-21: AI Stub Upgrade Draft PRs
**Impact:** 41/50 | **ROI:** 164 | **Effort:** 5/10 (1 week)  
**Dependencies:** T-06 (baseline established; this is a maintenance tool for future stubs)  

**Scope:**  
Build a **nightly GitHub Action** that:
1. Scans `QUALITY-REPORT.md` for any new v1 stubs  
2. For each stub, calls Claude Opus 4 (or GPT-4o) with:  
   - The stub content  
   - The v2 skill template  
   - 3 example v2 skills from the same category  
3. LLM generates a v2 draft (description, code example, failure modes)  
4. Workflow creates a **draft PR** with the LLM output  
5. PR is tagged `ai-generated` and assigned to human reviewers  
6. Human reviews, edits, and merges (or closes if draft is poor)  

**Workflow File:**  
`.github/workflows/ai-stub-upgrade.yml` (schedule: nightly at 2am UTC)

**Acceptance Criteria:**  
- Workflow runs successfully for 7 consecutive nights  
- At least 3 AI-generated drafts are human-reviewed and merged  
- False positive rate (unusable drafts) < 30%  

**Deliverable:**  
Stub-to-v2 upgrades happen **automatically**. Human effort shifts from drafting to reviewing.

---

### T-25: Semantic Search Embeddings
**Impact:** 39/50 | **ROI:** 156 | **Effort:** 5/10 (3 days)  
**Dependencies:** T-09 (search infra in place ✅)  

**Scope:**  
Add **natural language semantic search** to the web UI.

**Implementation:**  
1. Pre-compute embeddings for all skill descriptions using `sentence-transformers` (e.g., `all-MiniLM-L6-v2`)  
2. Store embeddings as static JSON: `docs/api/embeddings.json`  
3. Update `docs/index.html` to load embeddings and perform cosine similarity search in-browser (WASM or JavaScript library)  
4. Fallback: If browser computation is slow, use GitHub Actions to pre-compute top-N similar skills per skill and store as static JSON  

**User Experience:**  
User types: "How do I retry an API call 3 times?"  
Results (ranked by semantic similarity):  
1. `skills/12-tool-use/http-request.md` (0.92)  
2. `blueprints/self-healing-agent.md` (0.87)  
3. `skills/02-reasoning/error-handling.md` (0.84)  

**Deliverable:**  
Search understands **intent**, not just keywords. Users find the right skill even if they phrase it differently than the skill title.

---

## Wave 7 — UI Polish Batch (1 week)

**Objective:** Batch 3 high-ROI, low-effort UI improvements. These were deprioritized earlier but are trivial wins now that the catalog is complete.

### T-22: Skill Champion Frontmatter Field
**Impact:** 27/50 | **ROI:** 1350 | **Effort:** 2/10 (1 day)  
**Dependencies:** None  

**Scope:**  
Add a `champion: @username` field to skill frontmatter.

The **Skill Champion** is the contributor who took a skill from v1 → v3. They get credit in the skill file and are auto-assigned as code owner for that file.

**Implementation:**  
1. Extend `meta/skill-schema.json` to add optional `champion: string` field  
2. Add `champion: @username` to all v3 skills (via AST sweep script)  
3. Update `CODEOWNERS` to map each skill to its champion  
4. Render champion name in `docs/index.html` skill cards  

**Deliverable:**  
Contributors get **visible credit**. Maintenance load is distributed. Each skill has an owner.

---

### T-10: Mobile-Responsive UI Refactor
**Impact:** 31/50 | **ROI:** 517 | **Effort:** 3/10 (2 days)  
**Dependencies:** None  

**Scope:**  
Refactor `docs/index.html` CSS for mobile-first layout.

**Changes:**  
- Skill cards: 1 column on mobile, 2 on tablet, 3+ on desktop  
- Search bar: always visible on mobile (not collapsed)  
- Navigation: hamburger menu on mobile  
- Font sizes: 16px minimum on mobile (accessibility)  
- Touch targets: 44px minimum (iOS Human Interface Guidelines)  

**Testing:**  
Test on:
- iPhone 13 (Safari)  
- Pixel 7 (Chrome)  
- iPad Pro (Safari)  

**Deliverable:**  
The UI is **usable on mobile**. Bounce rate for mobile visitors drops.

---

## Execution Timeline Summary

| Wave | Duration | Cumulative Time | Key Deliverable |
|------|----------|----------------|------------------|
| Wave 1 | 3 weeks | 3 weeks | 50 battle-ready skills |
| Wave 2 | 5 weeks | 8 weeks | 150+ quality skills + 17 benchmarks |
| Wave 3 | 2 weeks | 10 weeks | CLI on PyPI, MCP listing, LangChain Hub presence |
| Wave 4 | 1 week | 11 weeks | 4 curated learning paths |
| Wave 5 | 4 weeks | 15 weeks | Zero stubs; catalog complete |
| Wave 6 | 2 weeks | 17 weeks | AI automation + semantic search |
| Wave 7 | 1 week | **18 weeks** | UI polish (mobile, champion attribution) |

**Total Calendar Time: ~18 weeks (4.5 months)**  

(Note: Some waves can run in parallel, e.g., T-24 and T-23 in Wave 3, or T-22 and T-10 in Wave 7. Actual calendar time may compress to ~16 weeks with parallel execution.)

---

## Success Criteria (After All Waves)

| Metric | Before (2026-06-14) | After Roadmap v2.0 | Target |
|--------|---------------------|-------------------|--------|
| **Total skills** | 377 | 377 | 377 |
| **v2+ skills** | 48 | **377** (100%) | 600+ |
| **Battle-tested (v3)** | 27 | 50+ | 300+ |
| **Benchmarks** | 4 | **17** | 17 |
| **Learning Paths** | 0 | **4** | 10+ |
| **CLI on PyPI** | ❌ | ✅ | ✅ |
| **MCP registry** | ❌ | ✅ | ✅ |
| **LangChain Hub** | ❌ | ✅ | ✅ |
| **Semantic search** | ❌ | ✅ | ✅ |
| **Mobile-ready UI** | ❌ | ✅ | ✅ |

---

## Policy Compliance

✅ **Product capability work:** 95% of effort (Waves 1–6 = product; Wave 7 = UI/polish)  
✅ **Community/marketing work:** 5% (within 20% cap)  
✅ **All active tasks ≥ 30/50 impact** (except T-22 at 27/50, included for trivial effort)  
✅ **No rejected tasks** (T-01, T-02, T-03, T-18 dropped per scoring floor)  

---

## What Changed from EXECUTION_PRIORITY_MATRIX.md?

1. **Removed Wave 0** — T-11, T-09, T-16 already complete  
2. **Removed Tier 4 UI tasks (T-12, T-13)** — graph and paths UI already exist  
3. **Removed T-15** — JSON-LD export already complete  
4. **Renumbered waves** — 7 waves now (was 6)  
5. **Updated timeline** — 18 weeks (was 22 weeks); 6 tasks completed = 4 weeks saved  
6. **Added parallel execution notes** — some tasks can run concurrently (e.g., T-24 + T-23)  

---

## Next Immediate Action

**Start T-04: Stub Upgrade Wave 1 (50 skills → v2).**

All structural foundations are in place. The catalog is the product. This is the highest-impact task in the roadmap.

**First 10 Skills to Upgrade (Recommended):**  
1. `skills/01-perception/pdf-parsing.md`  
2. `skills/01-perception/api-response-parsing.md`  
3. `skills/02-reasoning/planning.md`  
4. `skills/03-memory/rag.md`  
5. `skills/03-memory/episodic-memory.md`  
6. `skills/06-communication/summarize.md`  
7. `skills/09-agentic-patterns/react.md`  
8. `skills/12-tool-use/http-request.md`  
9. `skills/03-memory/cross-session-persistence.md`  
10. `skills/02-reasoning/task-decomposition.md`  

These 10 are the most-cited in `systems/` and `blueprints/`. Start here.

---

*Roadmap v2.0 — Generated 2026-06-14 after reality audit. This is the canonical execution plan.*
