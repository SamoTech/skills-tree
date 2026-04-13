# v1.0.0 — Launch: Living Skills Tree OS

> *The infrastructure is ready. The audit is sealed. The engine is running.*

## 🏁 What's Included

### Layer 1 — Trust (Four-State Model)
- Skill trust states: `verified`, `community`, `draft`, `deprecated`
- Metadata schema enforced across all skill files

### Layer 2 — Ingestion (AST + SBOM)
- `ast_sweep.py`: full AST scan of 555+ skill Markdown files
- Generates badge JSONs, pushes to `badge-data` branch for GitHub Pages serving
- SBOM-style dependency mapping per skill

### Layer 3 — Security (OSV Watchdog)
- `osv_check.py`: real-time OSV vulnerability scanning
- 15-minute SLA from hit to badge update
- GitHub Actions workflow triggers on schedule and push

### Layer 4 — Execution (Recursive Auditor)
- Self-healing audit pipeline
- Metadata validates code; code audits metadata
- Recursive consistency checks across skill graph

## 🔧 New Tools
- `tools/ast_sweep.py` — AST sweep engine
- `tools/osv_check.py` — OSV security watchdog
- `tools/inject_badge_links.py` — Batch badge injection for all skill files
- `tools/bootstrap_badges.py` — Badge bootstrapper
- `tools/write_badge.py` — Badge writer
- `tools/common.py` — Shared utilities

## 🏗 Infrastructure
- `badge-data` branch: GitHub Pages source for live shields.io badge endpoints
- `.github/workflows/`: Full CI/CD pipeline (sweep, OSV, audit)
- `SECURITY.md`: Security policy and vulnerability reporting
- `CONTRIBUTING.md`: Contributor guide

## 🚀 Getting Started

```bash
git clone https://github.com/SamoTech/skills-tree
cd skills-tree
python tools/ast_sweep.py --skills-root skills
python tools/inject_badge_links.py
```

---

*Built by [@OsamaHashim](https://github.com/OsamaHashim). The world is ready for it.* 🚀
