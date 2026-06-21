# DECISION LOG

**Maintained by:** Governance Recovery R-01  
**Source of truth:** Repository commits, file content, and PROJECT_MEMORY.md only  
**Rule:** Only decisions that can be proven from commits, files, or repository structure are recorded here.  
**Governing document:** `PROJECT_MEMORY.md`

> **⚠️ INTEGRITY NOTICE**
> The previous DECISION_LOG.md was a placeholder (24 bytes). All entries in this
> file are derived exclusively from the commit history and verified file content.
> No decisions from prior agent sessions have been carried forward without commit
> evidence.

---

## FORMAT

Each entry requires:
- **Decision ID** (D-RRXX where RR = recovery round, XX = sequence)
- **Date** (from commit timestamp or file timestamp)
- **Evidence** (commit SHA or file reference — no evidence = not recorded)
- **Decision** and **Rationale**

---

## DECISIONS DERIVED FROM COMMIT HISTORY

---

### D-ARCH-01 — Static Markdown as CMS (PERMANENT)

**Date:** Pre-2026 (foundational)  
**Evidence:** PROJECT_MEMORY.md Section 16 (DO NOT IMPLEMENT)  
**Decision:** Use GitHub-hosted Markdown files as the content layer. No database backend.  
**Rationale:** "The entire value of the project is that content is in Markdown — diffable, clonable, offline-readable. GitHub as CMS is a core design principle."  
**Status:** PERMANENT — do not revisit

---

### D-ARCH-02 — Vanilla HTML/CSS/JS for UI (PERMANENT)

**Date:** Pre-2026 (foundational)  
**Evidence:** PROJECT_MEMORY.md Section 16  
**Decision:** Keep `docs/index.html` as vanilla HTML/CSS/JS. No Next.js, React, or bundler.  
**Rationale:** "Keeps the UI hackable by everyone" — avoids build complexity and contributor friction.  
**Status:** PERMANENT — no framework migration

---

### D-ARCH-03 — No Auto-Merge of AI-Generated Content (PERMANENT)

**Date:** Pre-2026 (foundational)  
**Evidence:** PROJECT_MEMORY.md Section 16  
**Decision:** All AI-generated skill upgrades require human review before merge.  
**Rationale:** "LLMs produce plausible but incorrect code. Auto-merge would destroy content quality."  
**Status:** PERMANENT — non-negotiable quality gate

---

### D-ARCH-04 — Free API Access Forever (PERMANENT)

**Date:** Pre-2026 (foundational)  
**Evidence:** PROJECT_MEMORY.md Section 16  
**Decision:** All API access remains free. Revenue from sponsorship and certification only, never API gates.  
**Rationale:** Paywalled API creates friction for the developer audience the project depends on for growth.  
**Status:** PERMANENT

---

### D-SEC-01 — Least-Privilege Permissions on All Workflows

**Date:** 2026-06-21T08:00:34Z  
**Evidence:** Commit `33af1551709a15922aee9db6b4fa575b8e402f63`  
**Decision:** Added least-privilege `permissions:` blocks to all GitHub Actions workflows. Files affected: `test-coverage.yml`, `build-and-verify.yml`, `clean-install-test.yml`, `verify-taxonomy.yml`.  
**Rationale:** Resolves CodeQL alert: "Workflow does not contain permissions". No functional changes to job logic.  
**Status:** APPLIED

---

### D-GRAPH-01 — Graph JSON Layer Does Not Exist (VERIFIED)

**Date:** 2026-06-21T12:15:13Z  
**Evidence:** Commit `71e93ebabe7aa359a3fff98a2013814eede969b5` (TASK-000A audit)  
**Decision:** `data/SKILLS_GRAPH.json` confirmed as 24-byte placeholder string. No graph has been built. The graph layer starts at zero.  
**Rationale:** Independent audit found SKILLS_GRAPH.json = 24 bytes = literal placeholder string. All prior claims of 47, 53, or 58 nodes are fabricated.  
**Status:** VERIFIED FACT — informs all future graph tasks

---

### D-GOV-01 — PROJECT_CONSTITUTION.md Does Not Exist

**Date:** 2026-06-21T12:15:13Z  
**Evidence:** TASK-000A audit (`meta/VERIFIED_BASELINE_V2.md` Section 8)  
**Decision:** `meta/PROJECT_CONSTITUTION.md` is MISSING from the repository. Until it is created, `PROJECT_MEMORY.md` serves as the governing document.  
**Rationale:** Audit found the file absent. Future tasks referencing the Constitution are referencing a non-existent file.  
**Status:** OPEN — `PROJECT_CONSTITUTION.md` must be created or `PROJECT_MEMORY.md` designated as permanent governing document

---

### D-GOV-02 — Governance Recovery R-01

**Date:** 2026-06-21 (this session)  
**Evidence:** Mission R-01 prompt; VERIFIED_BASELINE_V2.md  
**Decision:** Rebuild all four governance files (MEMORY_STATE, DECISION_LOG, AGENT_SKILLS_MASTER_PLAN, AGENT_SKILLS_BACKLOG) from repository evidence only. Void all prior agent claims.  
**Rationale:** All four files were placeholders. Repository cannot function as a governance artifact without real content in these files.  
**Status:** APPLIED (this commit)

---

### D-DISC-01 — No Discord Until 10+ Monthly Contributors

**Date:** Pre-2026 (foundational)  
**Evidence:** PROJECT_MEMORY.md Section 16  
**Decision:** Do not create a Discord server until monthly contributor count exceeds 10.  
**Rationale:** "An empty Discord is worse than no Discord — it signals abandonment."  
**Status:** PERMANENT DEFERRAL — condition not yet met

---

## DECISIONS PENDING (observed gaps requiring a decision)

These are NOT decisions yet — they are observed gaps that require a decision:

| Gap | Required Decision |
|---|---|
| `data/SKILLS_GRAPH.json` is placeholder | Decide: build graph from scratch using `build-graph.yml` OR write graph JSON manually |
| `meta/PROJECT_CONSTITUTION.md` missing | Decide: create from PROJECT_MEMORY.md OR designate PROJECT_MEMORY.md as permanent |
| `paths/` directory exists but is empty | Decide: execute T-08 (4 learning tracks) as next task |
| Per-category READMEs missing | Decide: execute T-03 (17 README files) |
| 302 v1 stubs remain | Decide: begin T-04 (Stub Upgrade Wave 1) |

---

*This log was rebuilt during Mission R-01 on 2026-06-21.*
*Only add entries that can be proven from commit history, file content, or repository structure.*
