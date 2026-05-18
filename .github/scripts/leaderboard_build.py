# leaderboard_build.py
# Called by leaderboard.yml — Build leaderboard data and write leaderboard_data.json
import os, json
from datetime import datetime, timezone, timedelta
from github import Github

g    = Github(os.environ["GH_TOKEN"])
repo = g.get_repo(os.environ["GITHUB_REPOSITORY"])

now            = datetime.now(timezone.utc)
cutoff_30d     = now - timedelta(days=30)
cutoff_90d     = now - timedelta(days=90)
cutoff_alltime = now - timedelta(days=365)

scores_30d     = {}
scores_90d     = {}
scores_alltime = {}

# sort='created' is REQUIRED — the break on cutoff_alltime is only safe
# when PRs are returned in descending creation order. sort='updated' would
# break early when a recently-commented-on old PR appears at the top.
for pr in repo.get_pulls(
    state="closed",
    sort="created",
    direction="desc",
    base="main"
):
    if pr.merged_at is None:
        continue
    if pr.created_at < cutoff_alltime:
        break

    files = [f.filename for f in pr.get_files()]
    if not any(f.startswith("skills/") and f.endswith(".md") for f in files):
        continue

    user = pr.user.login
    scores_alltime[user] = scores_alltime.get(user, 0) + 1
    if pr.created_at >= cutoff_90d:
        scores_90d[user] = scores_90d.get(user, 0) + 1
    if pr.created_at >= cutoff_30d:
        scores_30d[user] = scores_30d.get(user, 0) + 1

data = {
    "generated_at": now.isoformat(),
    "leaderboard_30d":     sorted(scores_30d.items(),     key=lambda x: -x[1]),
    "leaderboard_90d":     sorted(scores_90d.items(),     key=lambda x: -x[1]),
    "leaderboard_alltime": sorted(scores_alltime.items(), key=lambda x: -x[1]),
}
with open("leaderboard_data.json", "w") as f:
    json.dump(data, f, indent=2)
print(f"Top contributors (all-time): {data['leaderboard_alltime'][:5]}")
