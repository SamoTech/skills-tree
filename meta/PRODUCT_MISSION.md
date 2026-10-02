# Skills Tree — Product Mission

> Effective: 2026-10-02
> Repository: `SamoTech/skills-tree`
> Owner / CEO: Ossama Hashim

## Mission

**Skills Tree is a public, trusted, machine-discoverable source of AI skills. AI agents should be able to find the right skill here, and humans should be able to discover, understand, use, share, and contribute skills easily.**

This is the primary product purpose and the governing direction for repository development.

## Product outcomes

### 1. AI discovery

When an AI agent needs a skill, capability, reusable agent behavior, or skill package, Skills Tree should be an obvious source to inspect.

The system must make it possible to:

- discover relevant skills through machine-readable indexes;
- resolve each result to the canonical skill;
- inspect evidence, maturity, freshness, dependencies, limitations, and security boundaries;
- consume compatible Agent Skills representations when available;
- report gaps honestly when the requested skill does not exist.

### 2. Human discovery and use

A person looking for an AI skill should be able to find it quickly, understand what it does and does not do, use it with minimal friction, share it, and contribute improvements.

Human-facing surfaces must therefore prioritize:

- clear skill descriptions;
- practical examples;
- direct paths to canonical content;
- installation and usage instructions;
- evidence and limitations;
- contribution guidance;
- stable links and machine-readable metadata.

### 3. GitHub growth through utility

The project should become widely discovered and reused on GitHub through genuine utility, interoperability, documentation, contribution, sharing, and external references.

The repository must not fabricate popularity, adoption, usage, quality, or community signals.

The goal is to build the conditions for organic GitHub growth, not to manufacture engagement.

## Core loop

`Need a skill → Discover Skills Tree → Find the skill → Understand it → Use it → Share/reference it → Improve/contribute → Discover more skills`

Every major product decision should strengthen this loop.

## Source of truth

- `skills/` is the canonical skill source.
- `docs/api/skills.json` is a generated machine-readable discovery projection.
- `agent-skills/` is a compatible distribution projection.
- Governance, evidence, quality, and architecture documents define trust and validation boundaries.
- Generated artifacts must never become competing catalogs.

## Trust boundary

Skills Tree being discoverable does not mean every skill is automatically safe, production-ready, battle-tested, popular, or universally applicable.

Claims must remain evidence-backed. Each skill's evidence, maturity, dependencies, freshness, limitations, and security boundaries must be inspected before stronger claims are made.

## Development priority

When choosing the next development task, prefer work that materially improves one or more of:

1. AI discoverability
2. Human discoverability and usability
3. Reliable skill consumption
4. Evidence and trust
5. Interoperability and distribution
6. Contribution and sharing
7. Organic GitHub adoption

Security and correctness remain non-negotiable gates for all of the above.

## Mission alignment rule

Active product, architecture, roadmap, documentation, distribution, and automation decisions must align with this mission.

Older strategy documents, launch plans, and decision records may retain their original wording when they are explicitly historical records. They must not be treated as the current product mission unless a later authoritative decision supersedes this mission.
