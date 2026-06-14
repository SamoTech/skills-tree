import json
import os
import re
import requests
from pathlib import Path

SKILLS_DIR = Path("skills")
BADGES_DIR = Path("docs/badges")
BADGES_DIR.mkdir(parents=True, exist_ok=True)
OSV_BATCH_URL = "https://api.osv.dev/v1/querybatch"

def parse_frontmatter(text):
    m = re.match(r'^---\s*\n(.*?)\n---', text, re.DOTALL)
    if not m: return {}
    fm = {}
    for line in m.group(1).splitlines():
        if ':' in line:
            k, _, v = line.partition(':')
            fm[k.strip()] = v.strip()
    return fm

def get_deps(fm):
    deps = []
    for key in ('dependencies', 'requires', 'packages'):
        val = fm.get(key, '')
        if val:
            for item in re.split(r'[,\s]+', val):
                item = item.strip().strip('[]')
                if item:
                    deps.append(item)
    return deps

def parse_dep(dep):
    m = re.match(r'^([A-Za-z0-9_\.\-]+)(?:[>=\=]+([\d\.]+))?$', dep)
    return m.groups() if m else (dep, None)

queries = []
skill_map = {}
skill_files = list(SKILLS_DIR.glob("*.md"))
for sf in skill_files:
    fm = parse_frontmatter(sf.read_text())
    for dep in get_deps(fm):
        pkg, ver = parse_dep(dep)
        if pkg:
            queries.append({"package": {"name": pkg, "ecosystem": "PyPI"}, "version": ver})
            skill_map.setdefault(sf.stem, []).append((pkg, ver))

response = requests.post(OSV_BATCH_URL, json={"queries": queries}).json()
results = response.get("results", [])

counts = {"verified": 0, "advisory": 0, "critical": 0, "unscanned": 0}
report_vulns = []
badge_data = {}

for skill_name, deps in skill_map.items():
    badge_data[skill_name] = {}
    for pkg, ver in deps:
        q_idx = queries.index({"package": {"name": pkg, "ecosystem": "PyPI"}, "version": ver})
        vulns = results[q_idx].get("vulns", [])
        if not vulns:
            state = "verified"
            counts[state] += 1
            badge_data[skill_name][pkg] = {"state": state, "version": ver}
        else:
            ids = [v["id"] for v in vulns]
            state = "critical"
            for v in vulns:
                for affected in v.get("affected", []):
                    for range_info in affected.get("ranges", []):
                        if range_info["type"] == "ECOSYSTEM":
                            for event in range_info.get("events", []):
                                if "fixed" in event: state = "advisory"
            report_vulns.append({"skill": skill_name, "package": pkg, "version": ver, "state": state, "vulns": ids})
            counts[state] += 1
            badge_data.setdefault(skill_name, {})[pkg] = {"state": state, "version": ver}

for skill_name, pkgs in badge_data.items():
    badge_file = BADGES_DIR / f"{skill_name}.json"
    badge_file.write_text(json.dumps({"skill": skill_name, "packages": pkgs}, indent=2))

report = {"counts": counts, "vulnerabilities": report_vulns}
Path("osv-report.json").write_text(json.dumps(report, indent=2))
print(json.dumps(counts))
