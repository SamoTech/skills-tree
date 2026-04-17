<!-- CATEGORY NOTE (P8 — duplicate prefix fix)
     This directory is numbered 16-infrastructure. The category 16-domain-specific
     also uses prefix 16, creating a collision in sort order and badge key generation.
     Resolution: 16-infrastructure will be renumbered to 17-infrastructure in the
     next schema revision (tracked in meta/glossary.md).
     Until then, both directories coexist. Tools that key on the numeric prefix
     (e.g. export_skills.py, badge pipeline) use the full directory name as the
     key, so there is no functional collision — only a cosmetic ordering issue.
-->

![Dependency Status](https://img.shields.io/endpoint?url=https://samotech.github.io/skills-tree/badges/skills-16-infrastructure-README.json)

# 🏗️ Infrastructure Skills

> **Category number:** `16-infrastructure` (will be renumbered to `17-infrastructure` in next schema revision — see note above)

Infrastructure skills enable agents to **manage, audit, and operate software infrastructure** — dependencies, environments, deployments, and system health.

## Skills in This Category

| Skill | Level | Description |
|---|---|---|
| [Dependency Auditor](dependency-auditor.md) | Advanced | Audit dependencies for vulnerabilities, license issues, and outdated packages |
