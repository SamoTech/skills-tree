# leaderboard_render.py
# Called by leaderboard.yml — Render leaderboard_data.json to docs/leaderboard.md
import json

with open("leaderboard_data.json") as f:
    data = json.load(f)

def render_table(entries, limit=20):
    if not entries:
        return "_No contributions yet._\n"
    medals = ["\U0001f947", "\U0001f948", "\U0001f949"]
    rows = [
        "| Rank | Contributor | Merged PRs |",
        "|------|-------------|------------|",
    ]
    for i, (user, count) in enumerate(entries[:limit], 1):
        medal = medals[i - 1] if i <= 3 else str(i)
        rows.append(f"| {medal} | [@{user}](https://github.com/{user}) | {count} |")
    return "\n".join(rows) + "\n"

ts  = data["generated_at"][:10]
out = (
    "# \U0001f3c6 Contributors Leaderboard\n\n"
    f"> Last updated: {ts}  \n"
    "> Counts merged PRs that added or improved a skill file.\n\n"
    "## Last 30 days\n"
    + render_table(data["leaderboard_30d"]) + "\n"
    "## Last 90 days\n"
    + render_table(data["leaderboard_90d"]) + "\n"
    "## All time (past 12 months)\n"
    + render_table(data["leaderboard_alltime"])
)

with open("docs/leaderboard.md", "w") as f:
    f.write(out)
print("Leaderboard written to docs/leaderboard.md")
