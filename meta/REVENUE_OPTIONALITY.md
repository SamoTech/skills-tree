# REVENUE OPTIONALITY
## INITIATIVE-020 — Phase 7
**Project:** Skills Tree · **Date:** 2026-06-24
**Constraint:** Open-source license unchanged. All revenue paths are additive, not extractive.

---

## Overview

Revenue is not the goal of the next 12 months. Traction is. However, revenue optionality must be designed now — before architectural decisions foreclose paths — because the product shape determines what monetization is possible.

---

## Revenue Path Evaluation

### Path 1 — Hosted API

**What it is:** A rate-limited, authenticated REST/GraphQL API over the skills graph.

**Pricing model:**
- Free: 100 req/month, public graph only
- Starter ($29/month): 10,000 req/month, changelog webhooks
- Pro ($99/month): 100,000 req/month, priority support
- Enterprise ($500+/month): private skill namespaces, SLA, SSO

**Open-source alignment:** ✅ Graph data remains MIT-licensed and downloadable.

**Implementation complexity:** MEDIUM

**Revenue ceiling:** $10K–$50K ARR at current scale. Scales to $200K+ ARR with traction.

**Verdict:** Highest near-term revenue potential. Build after MCP launch proves demand.

---

### Path 2 — Team Workspace

**What it is:** Collaborative environment where engineering teams create private skill matrices and run gap analyses.

**Pricing model:**
- Free: 1 workspace, public graph only
- Team ($49/month): 5 users, private skill notes, team gap analysis
- Business ($149/month): unlimited users, custom skill namespaces, export

**Open-source alignment:** ✅ Core graph and blueprints remain public.

**Implementation complexity:** HIGH

**Revenue ceiling:** $50K–$500K ARR with AI engineering team adoption.

**Verdict:** Highest long-term ceiling. Build after 6+ months of traction.

---

### Path 3 — Enterprise Graph

**What it is:** Private, customized instance with enterprise-specific skill nodes and on-premise deployment.

**Pricing model:** Annual contract, $5K–$50K depending on org size.

**Open-source alignment:** ✅ Core schema and tooling remain open.

**Implementation complexity:** MEDIUM-HIGH

**Revenue ceiling:** $100K–$1M ARR with 10–50 enterprise customers.

**Verdict:** Highest ACV. Pursue after public traction validates taxonomy value.

---

### Path 4 — Certification

**What it is:** Skills assessment and certification program — "Certified AI Engineer — Skills Tree Level 1/2/3" with verifiable credentials.

**Pricing model:** $99–$299 per exam. Annual renewal at $49.

**Open-source alignment:** ✅ Curriculum derived from public graph.

**Implementation complexity:** HIGH

**Revenue ceiling:** $50K–$300K ARR. Requires 12+ months of community credibility first.

**Verdict:** Highest brand value per dollar. Build in Year 2.

---

### Path 5 — Architecture Reports

**What it is:** Premium, expert-authored architecture reports for specific use cases (20 pages, skill stack, implementation guide, failure modes, benchmarks).

**Pricing model:** $99–$499 per report. Monthly subscription ($49/month) for library access.

**Open-source alignment:** ✅ Underlying taxonomy and blueprints remain free.

**Implementation complexity:** LOW-MEDIUM — content creation is the bottleneck.

**Revenue ceiling:** $20K–$100K ARR.

**Verdict:** Fastest to first dollar. Begin with 5 reports immediately, no engineering required.

---

## Revenue Roadmap

| Quarter | Action | Revenue Target |
|---------|--------|----------------|
| Q3 2026 | Publish 5 Architecture Reports (manual) | First $500–$2K |
| Q4 2026 | Launch Hosted API (beta, free tier only) | 0 (demand validation) |
| Q1 2027 | Convert API beta to paid tiers | $1K–$5K MRR |
| Q2 2027 | Launch Team Workspace beta | $2K–$10K MRR |
| Q3 2027 | Enterprise Graph pilot (3–5 customers) | $20K–$50K ACV |
| 2028 | Certification program launch | $50K–$300K ARR |

---

## Non-Negotiables

- The full skills graph (SKILLS_GRAPH.json) remains MIT-licensed and downloadable for free forever.
- Blueprint generation remains free for individual developers.
- No skill node is ever paywalled. Knowledge is the public good; infrastructure and collaboration are the services.
