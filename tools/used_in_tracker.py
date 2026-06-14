"""Used-In Tracker — Collects 'used-in' labelled GitHub issues and updates README.md.

Called by .github/workflows/used-in-tracker.yml.
Required environment variables:
  GH_TOKEN  — GitHub token with issues:read, contents:write
  REPO      — owner/repo string, e.g. "SamoTech/skills-tree"
"""
import os
import re
import json
import sys
import urllib.request
import urllib.error


def gh_get(url: str, headers: dict) -> list | dict:
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())


def main() -> None:
    repo = os.environ.get("REPO", "")
    token = os.environ.get("GH_TOKEN", "")

    if not repo or not token:
        print("[used-in] ERROR: REPO and GH_TOKEN environment variables must be set.")
        sys.exit(1)

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    issues_url = (
        f"https://api.github.com/repos/{repo}/issues"
        f"?state=open&labels=used-in&per_page=50"
    )
    try:
        used_in_issues = gh_get(issues_url, headers)
    except urllib.error.HTTPError as exc:
        print(f"[used-in] WARNING: GitHub API returned HTTP {exc.code} — skipping update.")
        used_in_issues = []
    except urllib.error.URLError as exc:
        print(f"[used-in] WARNING: Network error — {exc.reason} — skipping update.")
        used_in_issues = []

    entries = []
    for issue in used_in_issues:
        body = issue.get("body") or ""
        url_m = re.search(r'https?://\S+', body)
        if url_m:
            project_url = url_m.group(0).rstrip(')')
            project_name = issue["title"].replace("Used In:", "").strip()
            entries.append(f"- [{project_name}]({project_url})")

    if not entries:
        print("[used-in] No 'used-in' issues found. Skipping README update.")
        return

    block = (
        "<!-- USED_IN_START -->\n"
        "## \U0001f310 Used In\n\n"
        "These projects use Skills Tree skills in production. "
        "[Submit yours](../../issues/new?labels=used-in&title=Used+In:+Your+Project+Name)\n\n"
        + "\n".join(entries) + "\n"
        "<!-- USED_IN_END -->"
    )

    readme_path = "README.md"
    try:
        with open(readme_path) as fh:
            readme = fh.read()
    except OSError as exc:
        print(f"[used-in] ERROR: Cannot read {readme_path}: {exc}")
        sys.exit(1)

    if "<!-- USED_IN_START -->" in readme:
        new_readme = re.sub(
            r'<!-- USED_IN_START -->.*?<!-- USED_IN_END -->',
            block, readme, flags=re.DOTALL
        )
    else:
        new_readme = readme + "\n\n" + block + "\n"

    try:
        with open(readme_path, "w") as fh:
            fh.write(new_readme)
    except OSError as exc:
        print(f"[used-in] ERROR: Cannot write {readme_path}: {exc}")
        sys.exit(1)

    print(f"[used-in] Updated README with {len(entries)} entries.")


if __name__ == "__main__":
    main()
