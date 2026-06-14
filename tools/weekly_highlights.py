"""Weekly Highlights — Generates a weekly summary section in README.md.

Called by .github/workflows/weekly-highlights.yml.
Required environment variables:
  GH_TOKEN  — GitHub token with pull_requests:read, contents:write
  REPO      — owner/repo string, e.g. "SamoTech/skills-tree"
  DRY_RUN   — "true" to print output only, skip file write (default: "false")
"""
import os
import re
import json
import sys
import datetime
import urllib.request
import urllib.error


def gh_get(url: str, headers: dict) -> list | dict:
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())


def main() -> None:
    repo = os.environ.get("REPO", "")
    token = os.environ.get("GH_TOKEN", "")
    dry_run = os.environ.get("DRY_RUN", "false").lower() == "true"

    if not repo or not token:
        print("[weekly-highlights] ERROR: REPO and GH_TOKEN must be set.")
        sys.exit(1)

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    today = datetime.date.today()
    week_ago = (today - datetime.timedelta(days=7)).isoformat()

    prs_url = (
        f"https://api.github.com/repos/{repo}/pulls"
        f"?state=closed&base=main&per_page=50&sort=updated&direction=desc"
    )
    try:
        prs = gh_get(prs_url, headers)
    except (urllib.error.HTTPError, urllib.error.URLError) as exc:
        print(f"[weekly-highlights] ERROR: Cannot fetch PRs: {exc}")
        sys.exit(1)

    recent_prs = [
        pr for pr in prs
        if pr.get("merged_at") and pr["merged_at"] >= week_ago + "T00:00:00Z"
    ]

    skill_counts: dict = {}
    for pr in recent_prs:
        files_url = f"https://api.github.com/repos/{repo}/pulls/{pr['number']}/files"
        try:
            files = gh_get(files_url, headers)
            for f in files:
                name = f["filename"]
                if name.startswith("skills/") and name.endswith(".md"):
                    skill_counts[name] = skill_counts.get(name, 0) + 1
        except urllib.error.HTTPError as exc:
            print(f"[weekly-highlights] WARNING: HTTP {exc.code} for PR #{pr['number']} files.")
        except urllib.error.URLError as exc:
            print(f"[weekly-highlights] WARNING: Network error for PR #{pr['number']}: {exc.reason}")
        except Exception as exc:
            print(f"[weekly-highlights] WARNING: Unexpected error for PR #{pr['number']}: {exc}")

    top_skills = sorted(skill_counts.items(), key=lambda x: -x[1])[:5]
    upgrades = [
        pr for pr in recent_prs
        if re.search(r'v1.*v2|v2.*v3|v\d.*v\d', pr.get("title", ""), re.IGNORECASE)
    ]
    new_skills = [
        pr for pr in recent_prs
        if re.search(r'^feat.*skill|^add.*skill|new skill', pr.get("title", ""), re.IGNORECASE)
    ]

    week_str = today.strftime("%B %-d, %Y")
    lines = [
        "<!-- HIGHLIGHTS_START -->",
        f"## \U0001f4c6 This Week's Highlights \u2014 {week_str}",
        "",
    ]

    if top_skills:
        lines.append("### \U0001f525 Most Active Skills")
        for path, count in top_skills:
            skill_name = os.path.splitext(os.path.basename(path))[0].replace("-", " ").title()
            lines.append(f"- **{skill_name}** \u2014 {count} PR{'' if count == 1 else 's'}")
        lines.append("")

    if upgrades:
        lines.append("### \u2b06\ufe0f Skill Upgrades")
        for pr in upgrades[:5]:
            lines.append(f"- [{pr['title']}]({pr['html_url']})")
        lines.append("")

    if new_skills:
        lines.append("### \u2728 New Skills")
        for pr in new_skills[:5]:
            lines.append(f"- [{pr['title']}]({pr['html_url']})")
        lines.append("")

    if not top_skills and not upgrades and not new_skills:
        lines.append("> No skill changes this week. Open a PR to get started!")
        lines.append("")

    lines.append("<!-- HIGHLIGHTS_END -->")
    block = "\n".join(lines)

    if dry_run:
        print(block)
        return

    try:
        with open("README.md") as fh:
            readme = fh.read()
    except OSError as exc:
        print(f"[weekly-highlights] ERROR: Cannot read README.md: {exc}")
        sys.exit(1)

    if "<!-- HIGHLIGHTS_START -->" in readme:
        new_readme = re.sub(
            r'<!-- HIGHLIGHTS_START -->.*?<!-- HIGHLIGHTS_END -->',
            block, readme, flags=re.DOTALL
        )
    else:
        new_readme = re.sub(
            r'(^# .+\n)', r'\1\n' + block + '\n\n', readme, count=1, flags=re.MULTILINE
        )

    try:
        with open("README.md", "w") as fh:
            fh.write(new_readme)
    except OSError as exc:
        print(f"[weekly-highlights] ERROR: Cannot write README.md: {exc}")
        sys.exit(1)

    print("[weekly-highlights] README.md updated.")


if __name__ == "__main__":
    main()
