#!/usr/bin/env python3
"""
build_graph.py

Parses every skill file under skills/**/*.md, extracts cross-skill
"Related Skills" links, and writes a graph payload to docs/api/graph.json.

The JSON format is consumed by docs/graph.html (D3 force-directed graph).

Usage:
    python3 tools/build_graph.py

Output:
    docs/api/graph.json
"""

import os
import re
import glob
import json
import datetime

# ---------------------------------------------------------------------------
# Category metadata (colour palette used by the HTML UI)
# ---------------------------------------------------------------------------

CATEGORY_META = {
    "01-perception":       {"label": "Perception",        "color": "#4f98a3"},
    "02-reasoning":        {"label": "Reasoning",         "color": "#6daa45"},
    "03-memory":           {"label": "Memory",            "color": "#a86fdf"},
    "04-action-execution": {"label": "Action Execution",  "color": "#fdab43"},
    "05-code":             {"label": "Code",              "color": "#5591c7"},
    "06-communication":    {"label": "Communication",     "color": "#dd6974"},
    "07-tool-use":         {"label": "Tool Use",          "color": "#e8af34"},
    "08-multimodal":       {"label": "Multimodal",        "color": "#bb653b"},
    "09-agentic-patterns": {"label": "Agentic Patterns",  "color": "#d163a7"},
    "10-computer-use":     {"label": "Computer Use",      "color": "#01696f"},
    "11-web":              {"label": "Web",               "color": "#437a22"},
    "12-data":             {"label": "Data",              "color": "#006494"},
    "13-creative":         {"label": "Creative",          "color": "#964219"},
    "14-security":         {"label": "Security",          "color": "#a12c7b"},
    "15-orchestration":    {"label": "Orchestration",     "color": "#a13544"},
    "16-domain-specific":  {"label": "Domain-Specific",   "color": "#7a39bb"},
    "16-infrastructure":   {"label": "Infrastructure",    "color": "#da7101"},
}

DEFAULT_COLOR = "#7a7974"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def parse_skill(filepath: str) -> dict:
    """Return {id, name, category_dir, level, version, related_ids}."""
    with open(filepath, encoding="utf-8") as fh:
        content = fh.read()

    skill_id = os.path.splitext(os.path.basename(filepath))[0]

    # Title
    m = re.search(r'^# (.+)$', content, re.MULTILINE)
    name = m.group(1).strip() if m else skill_id

    # Category dir
    parts = filepath.replace("\\", "/").split("/")
    category_dir = parts[1] if len(parts) > 2 else "unknown"

    # Level
    lm = re.search(r'\*\*Skill Level:\*\*\s*`?([^`\n]+)`?', content, re.IGNORECASE)
    level = lm.group(1).strip() if lm else None

    # Version
    vm = re.search(r'\*\*Version:\*\*\s*`?([^`\n]+)`?', content, re.IGNORECASE)
    version = vm.group(1).strip() if vm else "v1"

    # Related skill links — extract filenames from markdown links
    related_raw = re.findall(r'\[.*?\]\(([^)]+\.md)\)', content)
    related_ids = []
    for r in related_raw:
        rid = os.path.splitext(os.path.basename(r))[0]
        if rid != skill_id:
            related_ids.append(rid)

    return {
        "id": skill_id,
        "name": name,
        "path": filepath.replace("\\", "/"),
        "category_dir": category_dir,
        "level": level,
        "version": version,
        "related_ids": list(dict.fromkeys(related_ids)),  # dedupe, preserve order
    }


def build_graph() -> dict:
    """Return {nodes, links, categories, generated, stats}."""
    skills_by_id: dict[str, dict] = {}

    for filepath in sorted(glob.glob("skills/**/*.md", recursive=True)):
        try:
            s = parse_skill(filepath)
            skills_by_id[s["id"]] = s
        except Exception as exc:
            print(f"[graph] WARNING: could not parse {filepath}: {exc}")

    # ---- Nodes ----
    nodes = []
    for s in skills_by_id.values():
        cat = CATEGORY_META.get(s["category_dir"], {})
        nodes.append({
            "id":       s["id"],
            "name":     s["name"],
            "path":     s["path"],
            "category": s["category_dir"],
            "catLabel": cat.get("label", s["category_dir"]),
            "color":    cat.get("color", DEFAULT_COLOR),
            "level":    s["level"],
            "version":  s["version"],
        })

    # ---- Links (directed: source references target) ----
    links = []
    seen_links: set[tuple] = set()
    for s in skills_by_id.values():
        for rid in s["related_ids"]:
            if rid in skills_by_id:
                key = (s["id"], rid)
                if key not in seen_links:
                    seen_links.add(key)
                    links.append({"source": s["id"], "target": rid})

    # ---- Category index ----
    categories = [
        {"id": cid, "label": meta["label"], "color": meta["color"]}
        for cid, meta in CATEGORY_META.items()
    ]

    # ---- Stats ----
    node_count = len(nodes)
    link_count = len(links)
    isolated = sum(1 for n in nodes if not any(
        l["source"] == n["id"] or l["target"] == n["id"] for l in links
    ))

    # Top connected nodes
    degree: dict[str, int] = {}
    for l in links:
        degree[l["source"]] = degree.get(l["source"], 0) + 1
        degree[l["target"]] = degree.get(l["target"], 0) + 1
    top_nodes = sorted(degree.items(), key=lambda x: x[1], reverse=True)[:10]
    top_connected = [
        {"id": nid, "name": skills_by_id[nid]["name"], "degree": deg}
        for nid, deg in top_nodes if nid in skills_by_id
    ]

    return {
        "generated": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "stats": {
            "nodes": node_count,
            "links": link_count,
            "isolated": isolated,
            "top_connected": top_connected,
        },
        "categories": categories,
        "nodes": nodes,
        "links": links,
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    os.makedirs("docs/api", exist_ok=True)
    print("[graph] Scanning skills/ ...")
    graph = build_graph()
    print(f"[graph] {graph['stats']['nodes']} nodes, {graph['stats']['links']} links")
    print(f"[graph] Isolated nodes (no links): {graph['stats']['isolated']}")

    out = "docs/api/graph.json"
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(graph, fh, indent=2, ensure_ascii=False)
    print(f"[graph] Wrote {out} ({os.path.getsize(out):,} bytes)")
    print("[graph] Done.")


if __name__ == "__main__":
    main()
