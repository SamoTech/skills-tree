# MOAT INDEX
## INITIATIVE-020 — Phase 5
**Project:** Skills Tree · **Date:** 2026-06-24

---

## Overview

A knowledge moat is information that exists nowhere else in the same structured, machine-readable, continuously maintained form. This document audits Skills Tree's existing moat, identifies gaps, and proposes what to build to widen it irreversibly.

---

## Section 1 — What Exists Nowhere Else

### 1.1 Structured AI Agent Skills Taxonomy (515+ Skills)

**Uniqueness:** No other public resource provides a machine-readable, graph-structured, semantically versioned taxonomy of AI agent skills. Existing resources are:
- Blog posts (unstructured, not queryable)
- Academic papers (static, not maintained)
- Framework docs (tool-specific, not cross-framework)
- Roadmap.sh AI path (linear, not graph-based, not dependency-mapped)

Skills Tree's graph format — with node IDs, edge relationships, categories, and dependency chains — is unique in the ecosystem.

**Moat strength:** HIGH. Replication requires months of expert curation and continuous maintenance. The graph structure itself is a network effect: each new skill makes all existing skills more valuable by enabling richer dependency paths.

### 1.2 Skill Dependency Graph (774+ Edges)

**Uniqueness:** The dependency graph encodes which skills must be learned before others, which skills co-occur in production systems, and which skills are independent. This is curatorial knowledge that cannot be scraped or auto-generated — it requires expert judgment about how AI engineering actually works.

**Moat strength:** VERY HIGH. This is the most defensible asset. The edges are opinions — informed expert opinions about real-world AI engineering practice — and opinions cannot be copied, only disagreed with.

### 1.3 Blueprint Schema + Goal-to-Architecture Mapping

**Uniqueness:** The Blueprint schema maps a natural-language goal to a structured skill stack. The goal catalog (20+ agent types) with associated skill stacks represents encoded architectural knowledge. No other resource maps "customer support agent" → [specific skill nodes with dependency order].

**Moat strength:** MEDIUM. Grows with each new blueprint. Currently thin (20 blueprints). Target: 200+ blueprints to make the catalog a comprehensive reference.

---

## Section 2 — Gaps (Knowledge That Should Exist Here But Doesn't)

### 2.1 Failure Mode Library

**What it is:** For each agent architecture type, a documented catalog of known failure modes: what breaks, under what conditions, and how to mitigate.

**Why it's a moat:** Failure modes are learned through painful production experience. They are almost never documented publicly. A searchable failure mode index would be uniquely valuable and highly cited.

**Status:** NOT BUILT. Priority: P0.

### 2.2 Benchmark Result Index

**What it is:** A maintained index of benchmark results across agent frameworks, models, and skill categories. Cross-references skills to the benchmarks that measure them.

**Status:** NOT BUILT. Priority: P1.

### 2.3 Skill-to-Framework Compatibility Matrix

**What it is:** A matrix mapping each skill node to the frameworks that implement it best with implementation quality ratings.

**Status:** NOT BUILT. Priority: P1.

### 2.4 Learning Path Templates (Role-Based)

**What it is:** Pre-built learning paths for specific roles: AI Engineer, Agent Architect, LLM Ops Engineer, AI Product Manager.

**Status:** NOT BUILT. Priority: P0 (highest potential reach).

### 2.5 Architecture Template Library

**What it is:** 50+ pre-built agent architecture templates with diagrams, skill stacks, and code scaffolds.

**Status:** Blueprint catalog has 20 entries. Needs to grow to 50+ with diagrams. Priority: P1.

---

## Section 3 — MOAT_INDEX Summary Table

| Knowledge Asset | Uniqueness | Current State | Action Required |
|-----------------|-----------|---------------|----------------|
| Skills Taxonomy (515+ nodes) | HIGH | ✅ Exists | Grow to 600+ |
| Dependency Graph (774+ edges) | VERY HIGH | ✅ Exists | Add failure-mode edges |
| Blueprint Schema | MEDIUM | ✅ Exists | Grow to 50+ blueprints |
| Failure Mode Library | VERY HIGH | ❌ Not built | Build immediately |
| Benchmark Index | HIGH | ❌ Not built | Build in Q4 2026 |
| Framework Compatibility Matrix | HIGH | ❌ Not built | Build in Q4 2026 |
| Role-Based Learning Paths | HIGH | ❌ Not built | Build immediately |
| Architecture Templates | MEDIUM-HIGH | Partial | Expand to 50+ |

---

## Conclusion

Skills Tree's core moat — the dependency graph — is already irreplaceable. The gaps above represent the difference between a well-maintained taxonomy and a platform that is referenced everywhere in AI engineering. The failure mode library and learning paths are the two highest-impact additions: they address pain that developers feel daily and document knowledge that is genuinely not captured anywhere else.
