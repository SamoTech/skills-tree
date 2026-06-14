import json
from pathlib import Path

report_path = Path("osv-report.json")
if not report_path.exists():
    print("No OSV report found.")
    exit(0)

report = json.loads(report_path.read_text())
counts = report.get("counts", {})
vulns = report.get("vulnerabilities", [])

print(f"| State | Count |")
print(f"|-------|-------|")
print(f"| Verified | {counts.get('verified', 0)} |")
print(f"| Advisory | {counts.get('advisory', 0)} |")
print(f"| Critical | {counts.get('critical', 0)} |")
print(f"| Unscanned | {counts.get('unscanned', 0)} |")

if vulns:
    print("\n#### Vulnerabilities Found")
    print("| Skill | Package | Version | State | CVEs |")
    print("|-------|---------|---------|-------|------|")
    for v in vulns:
        cves = ', '.join(v.get('vulns', []))
        print(f"| {v['skill']} | {v['package']} | {v.get('version','?')} | {v['state']} | {cves} |")
