import subprocess
from datetime import datetime, timedelta

def git(cmd):
    return subprocess.check_output(cmd, text=True).strip()

# Get commit dates (YYYY-MM-DD)
commit_dates_raw = git([
    "git", "log",
    "--pretty=format:%ad",
    "--date=short"
]).splitlines()

commit_dates = sorted(
    set(datetime.strptime(d, "%Y-%m-%d").date() for d in commit_dates_raw)
)

# Total contributions = total commits
total_contributions = len(commit_dates_raw)

# Calculate longest streak
longest_streak = 0
current_run = 0
prev_day = None

for day in commit_dates:
    if prev_day and day == prev_day + timedelta(days=1):
        current_run += 1
    else:
        current_run = 1
    longest_streak = max(longest_streak, current_run)
    prev_day = day

# Calculate current streak (up to today)
today = datetime.utcnow().date()
commit_set = set(commit_dates)

current_streak = 0
cursor = today
while cursor in commit_set:
    current_streak += 1
    cursor -= timedelta(days=1)

last_updated = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

stats_block = f"""
<table>
  <tr>
    <td align="center" width="33%">
      <h3>🧮 Total Contributions</h3>
      <h1>{total_contributions}</h1>
      <p><sub>All-time contributions</sub></p>
    </td>
    <td align="center" width="33%">
      <h3>🔥 Current Streak</h3>
      <h1>{current_streak} days</h1>
      <p><sub>Consecutive days active</sub></p>
    </td>
    <td align="center" width="33%">
      <h3>🏆 Longest Streak</h3>
      <h1>{longest_streak} days</h1>
      <p><sub>Best consistency achieved</sub></p>
    </td>
  </tr>
</table>

<p align="center">
  <sub>Last updated: {last_updated} (via GitHub Actions)</sub>
</p>
"""

with open("README.md", "r") as f:
    readme = f.read()

before, rest = readme.split("<!-- STATS_START -->")
_, after = rest.split("<!-- STATS_END -->")

new_readme = (
    before
    + "<!-- STATS_START -->\n"
    + stats_block
    + "\n<!-- STATS_END -->"
    + after
)

with open("README.md", "w") as f:
    f.write(new_readme)
